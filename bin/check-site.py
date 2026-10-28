#!/usr/bin/env python3
"""站点构建产物自检：断链、必需要素、SEO 标签、页面清单。"""
import os
import re
import sys
import urllib.parse

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_site")
BASEURL = "/keeplearning"


def pages():
    out = []
    for dirpath, _, files in os.walk(ROOT):
        for f in sorted(files):
            if f.endswith(".html"):
                out.append(os.path.join(dirpath, f))
    return out


def url_of(path):
    rel = "/" + os.path.relpath(path, ROOT).replace(os.sep, "/")
    if rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
    return rel


def check_links():
    broken, checked = [], 0
    for page in pages():
        html = open(page, encoding="utf-8").read()
        for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
            u = m.group(1)
            if not u or u.startswith(("http://", "https://", "mailto:", "#", "data:", "//")):
                continue
            path = urllib.parse.urlparse(u).path
            if not path:
                continue
            if path.startswith(BASEURL):
                path = path[len(BASEURL):] or "/"
            if not path.startswith("/"):
                base = url_of(page)
                path = os.path.normpath(os.path.join(base, path))
            target = os.path.join(ROOT, path.lstrip("/"))
            checked += 1
            cands = [target, target + ".html", os.path.join(target, "index.html")]
            if not any(os.path.exists(c) for c in cands):
                broken.append((url_of(page), u))
    return checked, broken


def check_required():
    problems = []
    for page in pages():
        html = open(page, encoding="utf-8").read()
        u = url_of(page)
        for needle, label in [
            ('<link rel="stylesheet"', "缺 stylesheet"),
            ('rel="canonical"', "缺 canonical"),
            ("og:title", "缺 og:title"),
            ("main.css", "缺 main.css 引用"),
        ]:
            if needle not in html:
                problems.append((u, label))
        # 未替换的 Liquid / 模板残留（{{ steps.* }} 是文章里故意展示的 CI 片段）
        for bad in ("{%", "Liquid error", "YOURNAME"):
            if bad in html:
                problems.append((u, f"残留 {bad!r}"))
        if re.search(r"\{\{(?!\s*steps\.)", html):
            problems.append((u, "残留未渲染的 '{{'"))
        # 空 href
        if re.search(r'href=""', html):
            problems.append((u, "存在空 href"))
    return problems


def main():
    ps = pages()
    print(f"页面总数: {len(ps)}")
    for p in ps:
        print("  ", url_of(p))

    checked, broken = check_links()
    print(f"\n内部链接检查: {checked} 条, 断链 {len(broken)} 条")
    for b in broken:
        print("   BROKEN", b)

    problems = check_required()
    print(f"结构/残留问题: {len(problems)} 项")
    for p in problems:
        print("   PROBLEM", p)

    extra = ["sitemap.xml", "feed.xml", "robots.txt", "assets/css/main.css",
             "assets/js/main.js", "assets/img/avatar.svg", "assets/img/favicon.svg",
             "404.html"]
    print("\n附属文件:")
    for e in extra:
        ok = os.path.exists(os.path.join(ROOT, e))
        print(f"   {'OK ' if ok else 'MISS'} {e}")

    return 0 if not broken and not problems else 1


if __name__ == "__main__":
    sys.exit(main())
