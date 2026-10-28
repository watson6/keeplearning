---
title: 构建与测试流水线改造
tag: 工程效率
client: 平台研发
year: "2025"
duration: 约 6 周
role_in_project: 流水线设计
summary: 从"本地打包、手工上传、口头通知"改成提交即构建、构建即测试、失败即通知。
cover: /assets/img/work/ci-pipeline.svg
gallery:
  - /assets/img/work/ci-pipeline-1.svg
  - /assets/img/work/ci-pipeline-2.svg
stack: [GitLab CI, Docker, Shell, Python]
outcomes:
  - 构建产物可追溯到 commit
  - 冒烟测试自动触发，失败阻断合入
  - 一次配置，多分支复用
featured: false
order: 3
---

## 改造前

打包靠某台机器上的脚本，传包靠聊天工具，测试靠口头通知。结果是：**没人能说清线上那个包到底是哪次提交打的。**

## 改造后

一条流水线四个阶段，每个阶段都有明确的输入输出：

| 阶段 | 做什么 | 失败时 |
| --- | --- | --- |
| build | 编译、产出 apk / 镜像 | 阻断，通知提交者 |
| smoke | 关键路径冒烟测试 | 阻断合入 |
| package | 版本号注入、归档 | 重试一次 |
| publish | 上传制品库、写 changelog | 通知值班 |

## 关键点

- **版本号自动注入**：从 commit 与 tag 推导，杜绝手工填错
- **缓存**：Docker 层缓存 + 依赖目录缓存，构建时间从 11 分钟降到 4 分钟
- **幂等**：同一 commit 重跑，产物完全一致（可验证的校验和）
- **失败要吵**：只通知该被通知的人，避免"群里全是红叉"导致的集体麻木

## 收获

> CI 的意义不是"自动化跑脚本"，而是把「这次改动到底行不行」变成一个有据可查的事实。
