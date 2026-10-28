---
title: AOSP 设备批量刷机与初始化
tag: 自动化
client: 产线与测试
year: "2025"
duration: 约 3 周
role_in_project: 脚本设计与实现
summary: 一台台手动刷机、改设置、装测试包？把整条链路脚本化，插上线就开始跑。
cover: /assets/img/work/flash-toolchain.svg
gallery:
  - /assets/img/work/flash-toolchain-1.svg
  - /assets/img/work/flash-toolchain-2.svg
stack: [Shell, Python, fastboot, ADB, AOSP]
outcomes:
  - 单台设备初始化从 20 分钟降到 4 分钟
  - 支持多台并行，失败自动重试
  - 刷机结果自动落库可追溯
featured: false
order: 7
---

## 痛点

新设备到货、固件升级、测试环境重建——每次都要重复同一串操作：`fastboot flash` 各个分区、重启、跳过开机向导、连 WiFi、改语言、关闭自动更新、装测试包。**手动做十台，一定会漏。**

## 做法

把流程拆成四个幂等阶段，任一阶段失败都可单独重跑：

```bash
./flash.sh --serial $SN stage=image     # 刷系统镜像
./flash.sh --serial $SN stage=boot      # 首启与向导跳过
./flash.sh --serial $SN stage=config    # 语言/时间/开发者选项
./flash.sh --serial $SN stage=verify    # 校验关键属性
```

### 跳过开机向导

不同 Android 版本方式不同，用 `settings` 组合比改 `build.prop` 更安全：

```bash
adb shell settings put secure user_setup_complete 1
adb shell settings put global device_provisioned 1
adb shell am start -a com.android.setupwizard.EXIT
```

### 并行与重试

用设备池调度，每台一个子进程；失败自动重试一次，仍失败则标记并在报告里附上最后 200 行日志。

## 结果

- 单台初始化 20 分钟 → 4 分钟
- 十台并行，一个午休时间全部就绪
- 每台设备的刷机记录（镜像版本、时间、操作者）可查

## 教训

> 刷机脚本最怕的不是写错命令，而是**半成功**。

刷了一半、设备卡在 fastboot 的机器如果被当成"可用"分配出去，排查成本远高于重刷。所以状态机必须显式：`待刷 → 刷写中 → 待校验 → 可用 / 需返修`。
