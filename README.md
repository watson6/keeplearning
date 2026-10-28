# keeplearning

华生的个人站点 —— 记录 AOSP 大屏交互平板测试自动化、运维工程与后端开发的实践与复盘。

**线上地址**：https://watson6.github.io/keeplearning/

---

## 这个站点在讲什么

一个工程师的作品与思考归档。不做简历式的技能罗列，而是把做过的事拆开讲清楚：

- **怎么发现问题** —— 现状是什么、卡在哪里
- **怎么做的决定** —— 为什么选这条路，放弃了什么
- **结果如何** —— 具体数字，不是形容词
- **踩了什么坑** —— 失败的部分比成功的部分更有信息量

主线是「把复杂的工程，做成可复现的流程」：设备层稳定、用例层可读、报告层可追溯。

---

## 主题

自建 Jekyll 主题，融合两种设计语言：

| 来源 | 提供的质感 |
| --- | --- |
| Curate | 超大标题的编辑式排版、宽留白、发丝分隔线、无阴影的克制风格、三列文字型文章列表 |
| Avenco | 大圆角卡片、紫粉渐变强调、胶囊按钮、点阵装饰 |

具体表现：

- **版式**：左对齐强网格，标题 clamp 到 5.15rem，行高 0.98 的紧凑大字
- **色彩**：暖白底 `#fdfcf9` + 深墨 `#0d042b`，强调色紫→粉渐变 `#6C4CF1 → #E15A8C`
- **字体**：DM Sans（拉丁）+ Noto Sans SC（中文），JetBrains Mono 用于标签与元信息
- **细节**：马克笔高亮、滚动显现、数字递增、封面编号叠字
- **深色模式**：跟随系统，也可手动切换，选择记在 `localStorage`

---

## 板块与内容

| 板块 | 路径 | 承载什么 |
| --- | --- | --- |
| 首页 | `/` | 定位一句话 + 精选项目 + 其他实践 + 能力 + 评价 + 最新文章 |
| 作品 | `/projects/` | 全部项目，支持按标签筛选 |
| 项目详情 | `/projects/<name>/` | 背景、关键决策、结果、踩过的坑，附技术栈与关键结果 |
| 文章 | `/blog/` | 工程笔记、踩坑复盘、方法论 |
| 关于 | `/about/` | 我是谁、判断标准、技术栈、工作方式 |
| 联系 | `/contact/` | 能帮什么、沟通前该想清楚什么、信件模板 |

首页的英雄区文案在 `index.html` 的 front matter 里改；滚动关键词、数据带、能力卡、评价分别在 `_data/` 下的四个 YAML 文件。

---

## 写一个项目

在 `_projects/` 新建 Markdown 文件即可，首页与作品页自动收录，不用碰模板。

```yaml
---
title: 项目名称
tag: 测试体系                    # 封面左上角的分类胶囊
client: 大屏智能交互平板产线       # 客户 / 场景
year: "2026"
duration: 持续迭代
role_in_project: 方案设计与主要实现
summary: 一句话说清这个项目解决了什么
cover: /assets/img/work/xxx.svg
gallery:                        # 详情页的过程图，可省
  - /assets/img/work/xxx-1.svg
stack: [Python, Pytest, ADB]    # 侧栏技术栈
outcomes:                       # 侧栏关键结果
  - 回归时间从半天级压到十几分钟
  - 失败用例自动附带截图与 logcat
featured: true                  # true 进「精选项目」，false 进「其他实践」
order: 1                        # 数字小的在前
---
```

正文建议按「背景 → 关键决策 → 结果 → 踩过的坑」的顺序写。**结果给数字，坑给细节。**

## 写一篇文章

在 `_posts/` 新建，文件名必须是 `YYYY-MM-DD-标题.md`：

```yaml
---
title: 文章标题
category: 复盘                  # 复盘 / 踩坑 / 方法
tags: [AOSP, ADB]              # 显示在正文页侧栏
description: 摘要，用于列表页与 SEO
---
```

`category` 与 `tags` 会出现在文章头部，`description` 决定分享时的摘要质量。

## 换图片

`assets/img/work/` 里的是脚本生成的抽象 SVG 占位图。换成真实截图：把图片放进该目录，改 front matter 里的 `cover:` / `gallery:` 路径即可。头像在 `assets/img/avatar.svg`。

---

## 依赖组件

| 组件 | 版本 | 作用 |
| --- | --- | --- |
| Jekyll | 4.4.1 | 静态站点生成 |
| Ruby | 3.3 | 运行时（`sass-embedded` 要求 ≥ 3.2） |
| jekyll-seo-tag | 2.9 | 自动生成 meta / OG / Twitter 卡片 |
| jekyll-feed | 0.18 | 生成 `/feed.xml` |
| jekyll-sitemap | 1.4 | 生成 `/sitemap.xml` 与 `/robots.txt` |
| DM Sans / Noto Sans SC / JetBrains Mono | Google Fonts | 字体 |
| GitHub Actions | — | 推送 `main` 自动构建并发布 |

样式是纯 CSS（`assets/css/main.css`），**没有 Sass 编译步骤** —— 减少一层版本风险。交互是 100 行原生 JS（`assets/js/main.js`），无 jQuery、无框架。所有图片素材在本地，**不依赖任何外部图床**。

---

## 本地预览

```bash
./bin/serve     # → http://127.0.0.1:4000/keeplearning/
```

要求 Homebrew Ruby（`brew install ruby`），系统自带的 Ruby 2.6 装不了现代 gem。

## 发布

推送 `main` 分支即自动部署到 GitHub Pages。首次使用需在仓库 **Settings → Pages → Source** 选择 **GitHub Actions**。

站点路径是子目录 `/keeplearning/`（这是普通仓库，不是 `watson6.github.io` 用户站点），该路径由 CI 的 `configure-pages` 自动注入，换仓库名无需改配置。
