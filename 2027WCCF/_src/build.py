"""生成网站各页面。

修改内容请编辑 _src/pages/*.html（各页正文）和 _src/footer.html（页脚），
导航、页面标题和横幅图片在下方 PAGES 中设置，然后运行：

    python _src/build.py

生成的 *.html 输出在网站根目录。不要直接改根目录下的 html，下次生成会被覆盖。
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# (文件名, 中文名, 英文名, 横幅图片, 首页卡片简介-中文, 首页卡片简介-英文)
PAGES = [
    ("index.html", "首页", "Home", None, "", ""),
    ("about.html", "简介", "About", "003-opening",
     "文化节的由来、宗旨与影响。", "Our history, mission and impact."),
    ("review.html", "往届回顾", "Past Festivals", "001-opening",
     "第二十三、二十四届精彩回顾与嘉宾贺信。", "Highlights, guests and letters from past years."),
    ("stage.html", "舞台演出", "Stages", "019-stage",
     "第一舞台、第二舞台互动区与文化大游行。", "Main stage, interactive stage and the culture parade."),
    ("experience.html", "文化体验", "Culture", "069-culture",
     "书法、脸谱、捏面人、围棋、太极。", "Calligraphy, opera masks, dough figures, Go and Tai Chi."),
    ("food.html", "美食街", "Food", "080-food",
     "天南海北的“舌尖上的中国”。", "Flavors from every corner of China."),
    ("contests.html", "大赛", "Contests", "092-roaming",
     "摄影大赛、青少年作文大赛与义工。", "Photography contest, youth essay contest and volunteers."),
    ("organizers.html", "主办单位", "Organizers", "005-opening",
     "主办、支持单位与合作伙伴。", "Hosts, supporters and partners."),
    ("join.html", "参与", "Get Involved", "046-interactive",
     "参展、美食、节目、赞助与义工报名。", "Exhibit, vend, perform, sponsor or volunteer."),
    ("gallery.html", "图库", "Gallery", "063-parade",
     "第二十四届摄影组精选100张。", "100 selected photos from the 24th festival."),
]

SITE_ZH = "第二十五届华盛顿中国文化节"
SITE_EN = "25th Washington Chinese Culture Festival"


def read(path):
    with open(path, encoding="utf8") as f:
        return f.read()


def nav(active):
    items = []
    for fn, zh, en, *_ in PAGES[1:]:
        cls = ' class="active" aria-current="page"' if fn == active else ""
        items.append(f'      <li><a href="{fn}"{cls}><span lang="zh">{zh}</span>'
                     f'<span lang="en">{en}</span></a></li>')
    return "\n".join(items)


def tiles():
    out = []
    for i, (fn, zh, en, img, dzh, den) in enumerate(PAGES[1:], 1):
        out.append(
            f'    <a class="tile" href="{fn}">'
            f'<img loading="lazy" src="images/photos/{img}-sm.jpg" alt="">'
            f'<span class="num">{i:02d} / <span lang="zh">{zh}</span><span lang="en">{en}</span></span>'
            f'<h3><span lang="zh">{zh}</span><span lang="en">{en}</span></h3>'
            f'<p class="muted"><span lang="zh">{dzh}</span><span lang="en">{den}</span></p></a>')
    return "\n".join(out)


def banner(body, img):
    """把正文开头的 eyebrow + h2 提到页面首屏里（左文右图）。"""
    m = re.search(r'\s*<p class="eyebrow">(.*?)</p>\s*<h2>(.*?)</h2>', body, re.S)
    eyebrow, title = (m.group(1), m.group(2)) if m else ("", "")
    if m:
        body = body[:m.start()] + body[m.end():]
    html = (f'<section class="page-hero">\n'
            f'  <div class="intro">\n'
            f'    <p class="tag">{eyebrow}</p>\n'
            f'    <h1>{title}</h1>\n'
            f'  </div>\n'
            f'  <div class="art"><img src="images/photos/{img}.jpg" alt=""></div>\n'
            f'</section>\n')
    return html + body


TEMPLATE = """<!doctype html>
<html lang="zh-CN" data-lang="both">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="第二十五届华盛顿中国文化节将于2027年在美国首都华盛顿举行。The 25th Washington Chinese Culture Festival, Washington, D.C., 2027.">
<link rel="icon" href="images/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&family=Noto+Serif+SC:wght@600;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/styles.css">
<script>try{{var l=localStorage.getItem('wccf-lang');if(l)document.documentElement.setAttribute('data-lang',l)}}catch(e){{}}</script>
</head>
<body class="page-{slug}">
<p class="notice"><span lang="zh">2027 第二十五届文化节筹备中，日期与详情将陆续公布。</span><span lang="en">Planning for the 25th festival is underway. Dates and details will be announced.</span></p>

<header class="nav">
  <div class="container">
    <a class="brand" href="index.html">
      <img src="images/logo.png" alt="华盛顿中国文化节标志">
      <span><b>华盛顿中国文化节</b><small>Washington Chinese Culture Festival · 2027</small></span>
    </a>
    <button class="menu-btn" aria-label="菜单 Menu">☰</button>
    <ul class="nav-links">
{nav}
    </ul>
    <div class="lang-switch" role="group" aria-label="语言 Language">
      <button type="button" data-lang-set="zh">中</button><button type="button" data-lang-set="both">中/EN</button><button type="button" data-lang-set="en">EN</button>
    </div>
  </div>
</header>

<main>
{body}
</main>
{footer}"""


def build():
    footer = read(os.path.join(HERE, "footer.html"))
    for fn, zh, en, img, *_ in PAGES:
        body = read(os.path.join(HERE, "pages", fn))
        if fn == "index.html":
            body = body.replace("<!--TILES-->", tiles())
            title = f"{SITE_ZH} · {SITE_EN}"
        else:
            body = banner(body, img)
            title = f"{zh} {en} · {SITE_ZH}"
        if fn != "gallery.html":
            footer_out = footer.replace('<script src="js/gallery-data.js"></script>\n', "")
        else:
            footer_out = footer
        html = TEMPLATE.format(title=title, slug=fn[:-5], nav=nav(fn), body=body.strip("\n"), footer=footer_out)
        with open(os.path.join(ROOT, fn), "w", encoding="utf8", newline="\n") as f:
            f.write(html)
        print("wrote", fn)


if __name__ == "__main__":
    build()
