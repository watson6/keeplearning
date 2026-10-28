---
title: AOSP 平板屏幕固定模式的自动化测试要点
category: 复盘
tags: [AOSP, Kiosk, ADB, 自动化]
description: 屏幕固定（Kiosk）看起来只是系统里的一个开关，但在自动化里它是最容易让用例连锁失败的一层。
---

## 为什么单独说这个

大屏交互平板常见的部署形态是 Kiosk：开机进固定应用、用户不能退出、不能下拉通知栏。测试里如果不在用例开始前明确"当前设备是否处于固定模式"，后面的操作会以各种奇怪的方式失败——点击不响应、返回键无效、截图黑屏。

问题在于：**失败现象和你以为的原因，往往隔了三层。**

## 关键命令

```bash
# 设置屏幕固定的 PIN（部分机型需要先设置才能启用）
adb shell settings put secure lock_screen_pin 1234

# 启用 / 停用屏幕固定
adb shell am start -a android.settings.SCREEN_PINNING
adb shell settings put global lock_to_app_enabled 1
```

不同 ROM 对 `lock_to_app_enabled` 的支持程度不一致，所以**必须用行为断言验证**，而不是只看 settings 值写成功。

## 用例设计建议

1. **前置状态显式化**：每条 Kiosk 相关用例的第一步是读取并记录当前固定状态，而不是默认它没开。
2. **退出路径单独验证**：正常退出、PIN 错误、连续错误锁定、低电量自动解除，各一条。
3. **用 UI 树而不是坐标**：固定模式下系统栏消失，屏幕可用区域变化，写死坐标的用例必然失败。
4. **截图作为失败凭据**：Kiosk 场景很多问题肉眼才看得出（例如导航栏残留一条 2px 的线）。

## 一个真实的坑

有台设备在固定模式下，`adb shell input keyevent KEYCODE_BACK` 会被系统吞掉——不会报错，也没有任何响应。用例最终以"超时"失败，看起来像是应用卡死。

解法是把"按键无效"当成一种需要断言的**正常状态**，而不是等待它生效：

```python
def is_back_blocked(driver):
    before = driver.current_activity()
    driver.press_keycode(4)
    time.sleep(0.5)
    return driver.current_activity() == before
```

## 小结

> Kiosk 相关的用例，本质上测的不是"功能"，而是"约束"。

约束类用例的通病是：它失败时不告诉你原因。所以每条用例都要自己带现场——状态、截图、当前 Activity，缺一不可。
