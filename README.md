# keeplearning

华生的个人作品集站点 —— Jekyll 静态站点，通过 GitHub Actions 发布到 GitHub Pages。

**线上地址**：https://watson6.github.io/keeplearning/

---

## 快速开始

```bash
./bin/serve          # 安装依赖并启动 http://127.0.0.1:4000/keeplearning/
```

手动方式：

```bash
export PATH="/opt/homebrew/opt/ruby/bin:/opt/homebrew/lib/ruby/gems/4.0.0/bin:$PATH"
bundle install
bundle exec jekyll serve --livereload
```

> 系统自带 Ruby 2.6 装不了现代 gem，必须用 Homebrew Ruby 4.x（已安装）。

---

## 目录结构

```text
_config.yml            站点配置：标题、导航、作者、集合、插件
index.html             首页 front matter（英雄区文案在这里改）
_data/
  ticker.yml           首页滚动的技术关键词
  stats.yml            数据带的四组数字
  capabilities.yml     能力卡片
  testimonials.yml     评价
_projects/             作品集，一个项目一个 Markdown 文件
_posts/                文章，文件名 YYYY-MM-DD-标题.md
_layouts/              页面骨架
  default.html         全站外壳
  home.html            首页
  page.html            普通内页（关于/联系）
  project.html         项目详情
  projects.html        作品索引
  blog.html / post.html 文章列表与正文
_includes/             可复用片段：head / nav / footer / 卡片 / 图标的
assets/css/main.css    全部样式（纯 CSS，无 Sass）
assets/js/main.js      主题切换、移动导航、滚动显现、筛选
bin/gen-art.py         生成封面图与头像（SVG）
bin/serve              本地开发启动脚本
.github/workflows/pages.yml  GitHub Pages 自动部署
```

---

## 新增内容

### 加一个项目

在 `_projects/` 新建 `my-project.md`：

```yaml
---
title: 项目名称
tag: 分类标签          # 显示在封面左上角的胶囊
client: 客户 / 场景
year: "2026"
duration: 项目周期
role_in_project: 你的角色
summary: 一句话说明，显示在详情页标题下
cover: /assets/img/work/my-project.svg
gallery:
  - /assets/img/work/my-project-1.svg
stack: [Python, Pytest, Docker]
outcomes:
  - 关键结果一
  - 关键结果二
featured: true         # true 进首页"精选"，false 进"其他实践"
order: 9               # 排序，数字小的在前
---

## 正文 markdown
```

不需要改任何模板，首页与作品页会自动收录。

### 加一篇文章

在 `_posts/` 新建 `2026-10-01-my-post.md`：

```yaml
---
title: 文章标题
category: 复盘
tags: [标签1, 标签2]
description: 摘要，会出现在列表和 SEO 描述里
---
```

### 换成自己的图片

`assets/img/work/` 里的封面是脚本生成的抽象 SVG。换成真实截图时：

1. 把图片放进 `assets/img/work/`
2. 改 front matter 里的 `cover:` / `gallery:` 路径

重新生成占位图：

```bash
python3 bin/gen-art.py
```

---

## 部署

推送到 `main` 分支即自动部署（`.github/workflows/pages.yml`）：

1. **Settings → Pages → Build and deployment → Source** 选 **GitHub Actions**
2. 推送代码，Actions 自动构建并发布
3. 首次部署完成后，约 1 分钟站点生效

关键配置说明：

- `_config.yml` 的 `baseurl: "/keeplearning"` —— 因为这是普通仓库，不是 `watson6.github.io`
- CI 里用 `--baseurl "${{ steps.pages.outputs.base_path }}"` 由 `configure-pages` 自动注入，
  所以换仓库名也不用改配置
- 若改成用户站点（仓库名 `watson6.github.io`），把 `baseurl` 改成 `""`

### 如果要用自定义域名

1. 在仓库根目录加 `CNAME` 文件，内容写域名
2. `_config.yml` 里 `url` 改成 `https://你的域名`，`baseurl` 改成 `""`
3. DNS 加 CNAME 记录指向 `watson6.github.io`

---

## 设计说明

融合了两套主题的基因：

| 来源 | 借鉴的部分 |
| --- | --- |
| Curate | 超大标题的编辑式排版、宽留白、发丝分隔线、无阴影克制风格、三列文字型日志列表 |
| Avenco | 大圆角卡片、紫粉渐变强调色、胶囊按钮、点阵装饰、封面鲨字叠层 |

技术约束：

- **纯 CSS，不用 Sass** —— 避免 `sass-embedded` 与 GitHub Pages 的版本差异
- **图片全部本地 SVG** —— 无外链依赖，加载快，替换方便
- **无 JS 也能读** —— 滚动动画是渐进增强，`prefers-reduced-motion` 完全尊重
- **深色模式** —— 跟随系统，手动切换结果存 `localStorage`

---

## 待替换

发布前建议改掉这些占位内容：

- `_config.yml`：`author` 信息、`social` 里的链接
- `_data/stats.yml`：四组数字（目前是示例值）
- `_data/testimonials.yml`：评价内容（或删掉整个文件与首页对应区块）
- `_projects/*.md`：项目描述细节
- `assets/img/avatar.svg`：换成真实头像

> 本仓库不含任何邮箱地址 —— 联系方式统一走 GitHub 主页，避免个人信息泄露。
