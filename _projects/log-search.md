---
title: 生产日志检索工具
tag: 后端
client: 运维团队
year: "2024"
duration: 约 5 周
role_in_project: 独立开发
summary: grep 十万行日志要等半分钟？做一层轻量索引，把"找一条报错"变成两秒钟的事。
cover: /assets/img/work/log-search.svg
gallery:
  - /assets/img/work/log-search-1.svg
  - /assets/img/work/log-search-2.svg
stack: [Python, SQLite, FTS5, FastAPI]
outcomes:
  - 检索响应从 30 秒级降到 2 秒内
  - 支持按时间、级别、关键字组合过滤
  - 完全离线，不需要额外基础设施
featured: false
order: 8
---

## 背景

排查线上问题时，最常见的第一步是"找日志"。当时的做法是 `ssh` 上去、`grep`、`less` 翻页，一次搜索动辄几十秒，而且没法按时间和级别组合过滤。

引入 ELK 当然可以，但对中小规模（每天几百 MB）来说，运维成本和收益不成比例。

## 方案：SQLite FTS5

选它的理由是**零运维**：单文件、无需服务端、全文索引性能足够。

```sql
CREATE VIRTUAL TABLE logs USING fts5(
  ts, level, service, message,
  tokenize = 'unicode61'
);
```

入库时按服务分表，按天分区；查询时先按时间范围裁剪，再走全文索引。

### 关键设计

- **时间优先裁剪**：绝大多数查询都带时间范围，先过滤时间再检索，能砍掉 95% 的扫描量
- **结构化 + 全文并存**：`level`、`service` 是精确匹配列，`message` 走分词
- **错误聚类**：对同一 pattern 的错误自动归组，避免一万条相同报错刷屏

## 效果

- 检索从 30 秒级降到 2 秒内
- 常用查询固化成按钮，值班同事不需要记语法
- 整个工具就是一个 Python 脚本 + 一个 SQLite 文件，拷走就能用

## 一点体会

> 不是所有问题都需要"上系统"。先问清楚数据量级，很多场景单机工具就够了。
