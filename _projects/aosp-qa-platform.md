---
title: AOSP 大屏平板自动化测试体系
tag: 测试体系
client: 大屏智能交互平板产线
year: "2026"
duration: 持续迭代
role_in_project: 方案设计与主要实现
summary: 把依赖人工点按的整机验收，改造成分层自动化：设备层稳定、用例层可读、报告层可追溯。
cover: /assets/img/work/aosp-qa-platform.svg
gallery:
  - /assets/img/work/aosp-qa-platform-1.svg
  - /assets/img/work/aosp-qa-platform-2.svg
stack: [Python, Pytest, Appium, ADB, AOSP, Allure]
outcomes:
  - 回归执行时间从半天级压到十几分钟
  - 每条失败用例自动附带截图与 logcat
  - 用例与需求编号双向可追溯
featured: true
order: 1
---

## 背景

大屏交互平板的验收流程过去高度依赖人工：一个人对着测试清单，一台台机器点按、拍照、记录。问题不在于慢，而在于**结论不可复现**——同一条用例，不同的人、不同的机器、不同的系统版本，答案可能不同。

改造的目标很明确：让每一条验收结论都能被机器重复验证。

## 分层设计

我把整个体系拆成三层，每层只关心一件事：

1. **设备层**：设备的发现、占用、复位。谁在用哪台机器，用完必须回到干净状态。
2. **用例层**：只描述"做什么、期望什么"，不关心设备怎么来的。
3. **报告层**：结构化输出。失败必须自带现场，而不是只留一句 `assert False`。

这样拆的好处是：换设备、换框架、换报告工具，都只需要动其中一层。

## 关键决策

### 用 ADB 直连，而不是套一层厚厚的封装

AOSP 设备本身开放了足够的控制面（`adb shell`、`uiautomator`、`settings`、`am`）。直接走这些接口，比引入庞大框架更可控，出问题也更容易定位到具体命令。

```bash
# 设备状态归位 —— 每条用例执行前必跑
adb shell settings put global stay_on_while_plugged_in 3
adb shell wm size reset
adb shell am force-stop com.example.target
adb shell pm clear com.example.target
```

### 失败即现场

我在 fixture 里统一挂钩子：用例失败自动抓取截图、dump 当前界面树、导出最近 500 行 logcat，一并塞进报告。

```python
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.failed:
        attach_screenshot(item)
        attach_ui_dump(item)
        attach_logcat(item, lines=500)
```

带来的变化很直观：以前失败要复现一次才能查，现在看报告就能定位到哪一步、哪个控件、什么异常。

### 屏幕固定模式的特殊处理

大屏平板常跑 Kiosk 场景，系统层面的屏幕固定会拦截部分操作。这块单独做了一组用例，覆盖进入/退出固定、PIN 校验、异常退出恢复等路径。

## 结果

> 最重要的不是省了几个小时，而是团队开始相信"测试结果"这件事本身。

- 回归从半天级降到十几分钟，可以挂在每次提交后自动跑
- 失败定位平均耗时从"复现 + 排查"变成"看报告"
- 用例编号与需求单挂钩，验收会议不再靠回忆

## 踩过的坑

- **设备状态漂移**：最常见的失败原因不是被测功能坏了，而是上一轮用例留下的状态。所以复位必须无条件执行。
- **等待策略**：`sleep` 是最贵的代码。全部换成基于条件的轮询（元素出现、Activity 切换、日志关键字），稳定性立刻上一个台阶。
- **版本一致性**：固件、测试脚本、用例集三者版本必须一起记录，否则结论无法回溯。
