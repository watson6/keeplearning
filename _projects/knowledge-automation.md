---
title: 文档与知识库自动化
tag: 工程效率
client: 个人 / 团队
year: "2025"
duration: 长期
role_in_project: 独立完成
summary: 让文档跟着代码走：变更即触发、模板化生成、按主题归档，减少"写了没人看、看了是旧的"。
cover: /assets/img/work/knowledge-automation.svg
gallery:
  - /assets/img/work/knowledge-automation-1.svg
  - /assets/img/work/knowledge-automation-2.svg
stack: [Jekyll, Markdown, Obsidian, Python, Git]
outcomes:
  - 文档与代码同仓同版本
  - 模板化结构，减少从零起稿的摩擦
  - 每周自动巡检失效链接与孤立文档
featured: false
order: 6
---

## 问题

文档的敌人不是"不会写"，是**维护成本**。写完那一刻就开始过期。

## 三条规则

1. **同仓同版本**：文档和代码放在同一个仓库，跟着同一个 PR 走。代码改了文档没改，review 时就能看见。
2. **模板先行**：会议记录、接口说明、故障复盘都有固定骨架，写的人只需要填空。
3. **自动巡检**：定时任务检查失效链接、孤立页面、超过 90 天未更新的核心文档，输出一份心跳报告。

## 技术选型

- **Jekyll**：纯静态、构建快、和 GitHub Pages 天然契合
- **Obsidian**：本地知识库，双链组织思路
- **Git**：所有变更留痕，可回溯

## 结果

> 知识库真正的价值，是半年后你还敢相信里面的内容。

- 文档不再是"写完就死"的一次性产物
- 新人可以从一份索引开始，自己找到路径
- 每周一次巡检，把腐化控制在可处理的范围
