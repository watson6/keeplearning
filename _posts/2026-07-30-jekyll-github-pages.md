---
title: Jekyll + GitHub Pages：零成本的个人站点方案
category: 方法
tags: [Jekyll, GitHub Pages, 静态站点]
description: 为什么用 Jekyll 而不是别的？因为内容应该比工具活得久。
---

## 选择的标准

给个人站点选技术栈，我只看三条：

1. **内容能带走**：Markdown 文件必须能脱离工具存在
2. **构建可复现**：三年后回来还能构建出一样的结果
3. **维护成本接近零**：不租服务器、不修安全补丁

Jekyll + GitHub Pages 三条都满足。Markdown 是纯文本，构建是静态的，托管是免费的。

## 这套站点的结构

```text
_config.yml      全局配置（站点信息、导航、集合）
_data/           结构化数据（能力、评价、统计）
_projects/       作品集，每个项目一个 Markdown
_posts/          文章，文件名自带日期
_layouts/        页面骨架
_includes/       可复用片段（导航、页脚、卡片）
assets/          样式、脚本、图片
```

需要新增一个项目时，只需要在 `_projects/` 里丢一个 Markdown 文件，填好 front matter：

```yaml
---
title: 项目名称
tag: 分类
summary: 一句话说明
cover: /assets/img/work/demo.svg
featured: true
order: 1
---
```

首页会自动挑出 `featured: true` 的项目放在精选区，其余进网格。

## 部署

推送到 `main` 分支，GitHub Actions 自动构建并发布。关键是这一行：

{% raw %}```yaml
run: bundle exec jekyll build --baseurl "${{ steps.pages.outputs.base_path || '' }}"
```{% endraw %}
`configure-pages` 输出当前仓库的 base path：用户站点（`username.github.io`）是空，普通仓库是 `/仓库名`。让 CI 自动注入，就不用在配置里手改。

## 本地预览

```bash
bundle exec jekyll serve --livereload
```

改文件自动刷新，地址 `http://127.0.0.1:4000`。

## 一点提醒

> 静态站点最大的好处不是快，而是**你不会因为工具停止维护而丢掉内容**。

所以我宁愿手写一点 HTML/CSS，也不愿把内容锁进某个随时会变的服务里。
