---
title: 测试设备集群与远程调试平台
tag: 基础设施
client: 内部研发团队
year: "2025"
duration: 约 3 个月
role_in_project: 架构与实现
summary: 十几台平板散落在工位上、谁在用什么没人清楚——把它变成一个可查询、可预约、可远程连接的小型设备云。
cover: /assets/img/work/device-farm.svg
gallery:
  - /assets/img/work/device-farm-1.svg
  - /assets/img/work/device-farm-2.svg
stack: [Python, FastAPI, ADB, Docker, Nginx, SQLite]
outcomes:
  - 设备闲置率从约 50% 降到 10% 以内
  - 支持浏览器内远程投屏与操作
  - 设备固件版本一屏可见
featured: true
order: 2
---

## 背景

团队有十几台测试平板，分散在不同工位。真实情况是：想用的时候找不到空闲设备，找到了不知道是什么系统版本，跑出问题想让人帮忙看一眼，还得跑过去。

这本质上是**资源不可见**的问题，不是设备不够的问题。

## 设计

### 设备注册与心跳

每台设备上跑一个极轻的 agent，定时上报：序列号、IP、Android 版本、固件构建号、电量、当前占用者。服务端只存最新状态，不做历史堆积（历史另有采集）。

```bash
# agent 的核心就几行
adb -s $SN shell getprop ro.build.display.id
adb -s $SN shell getprop ro.build.version.release
adb -s $SN shell dumpsys battery | grep level
```

### 预约与占用

设备被占用时加锁，超时自动释放。加锁这一层刻意做得"笨"——数据库行锁 + 过期时间，不引入消息队列。**十台设备的规模，复杂度就是负债。**

### 浏览器远程投屏

用 `adb exec-out screencap` 做画面流，前端按帧刷新；操作通过坐标注入回传。延迟不追求极致，够做「远程看一眼、点一下」就够。

## 结果

- 找空闲设备从"群里问一圈"变成"打开页面看一眼"
- 版本混乱导致的"我这复现不了"显著减少
- 新人上手只需要一个网址

## 复盘

> 内部工具的价值不在功能多，而在于**它比原来的做法省的那一步**。

最初我做了不少统计报表，实际几乎没人看。后来砍掉大半，只保留"设备列表 + 版本 + 谁在用"，使用率反而上去了。
