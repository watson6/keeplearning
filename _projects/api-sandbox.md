---
title: 接口联调沙箱
tag: 后端
client: 前后端联调
year: "2024"
duration: 约 4 周
role_in_project: 独立开发
summary: 后端没就绪时前端干等？用一份契约生成可用的 Mock 服务，字段、错误码、延迟都可配。
cover: /assets/img/work/api-sandbox.svg
gallery:
  - /assets/img/work/api-sandbox-1.svg
  - /assets/img/work/api-sandbox-2.svg
stack: [Python, FastAPI, OpenAPI, Docker]
outcomes:
  - 前端不再因后端排期阻塞
  - 契约变更有 diff 提示
  - 错误分支可在沙箱里手动触发
featured: false
order: 5
---

## 起因

联调阶段最常见的等待：前端等接口。等的不只是"有没有"，还有各种边界情况——超时、空列表、权限不足。

## 方案

以 OpenAPI 契约为唯一事实源，做三件事：

1. **生成**：从契约自动生成可跑的 Mock 服务，含合理示例数据
2. **注入**：支持按 header / query 触发指定错误码与延迟
3. **比对**：契约变更时输出字段级 diff，避免"悄悄改了个字段"

```bash
# 指定场景：模拟 500 + 800ms 延迟
curl -H "X-Mock-Scenario: server_error" \
     -H "X-Mock-Delay: 800" \
     http://localhost:8080/api/v1/orders
```

## 效果

- 前端可以在后端接口真正可用前完成 80% 的页面逻辑
- 异常分支被真实验证过，而不是上线后才发现
- 契约变更成为一次显式的、有记录的评审动作

## 一点体会

> 把"等"变成"可以并行"，是工程里性价比最高的优化之一。
