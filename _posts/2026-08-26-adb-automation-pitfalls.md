---
title: 用 ADB 做设备自动化的五个高频陷阱
category: 踩坑
tags: [ADB, Python, 设备集群]
description: 设备连不上、命令返回空、多设备串台——这些问题的根因往往不在 ADB 本身。
---

## 陷阱一：以为 `adb devices` 里有就是可用

`device` 状态只代表守护进程在，不代表系统已经启动完成。示例如下：

```bash
adb -s $SN shell getprop sys.boot_completed   # 才是真正的就绪信号
```

等待 `sys.boot_completed=1`，比 `adb wait-for-device` 可靠得多。

## 陷阱二：多设备时忘了 `-s`

机器上一旦挂着两台设备，所有不带 `-s` 的命令都会报 `more than one device`，而某些脚本会静默吞掉这个错误继续往下跑，最后在别处以诡异的方式失败。

建议：**所有封装函数强制要求序列号参数**，不提供默认值。

## 陷阱三：把 `shell` 的输出当结构化数据

`dumpsys` 的输出格式随 Android 版本变化。写解析器时不要依赖固定行号；用正则抓关键字，并且**解析失败要显式抛错**，而不是返回空字典。

## 陷阱四：设备状态漂移

上一条用例改了分辨率、改了语言、装了测试包，下一条用例就踩在前一条的残留上。

```bash
adb shell wm size reset
adb shell settings put system screen_off_timeout 2147483647
adb shell am force-stop com.example.target
```

复位要写成一个函数，在每条用例的 setup 里无条件调用。

## 陷阱五：以为超时是设备慢

大部分"超时"其实是用例在等一个永远不会出现的条件。换成条件轮询 + 短超时 + 明确报错信息，能省下大量误判。

```python
def wait_until(pred, timeout=8, interval=0.3, what="条件"):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if pred():
            return True
        time.sleep(interval)
    raise TimeoutError(f"等待超时：{what}")
```

## 小结

> ADB 本身很稳，不稳的是我们对设备状态的假设。

把假设写出来、变成断言，问题就少了一大半。
