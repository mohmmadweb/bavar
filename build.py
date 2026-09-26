#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""سازنده‌ی سایت ایستای صندوق باور.

اجرا:  python3 build.py            → خروجی در dist/
       python3 build.py --serve    → ساخت و اجرای سرور محلی روی پورت 8797

همه‌ی لینک‌ها نسبی ساخته می‌شوند تا سایت هم روی ریشه‌ی دامنه و هم زیر
یک زیرمسیر (مثل github.io/bavar/) درست کار کند.
"""
import html
import shutil
import sys
from pathlib import Path

from content import (APPLY_DOCS, CLUB_EVENTS, CLUB_PROGRAMS, FUND, HERO, NAV,
                     NEWS, NEWS_TYPE_LABEL, NEWS_TYPES, PORTFOLIO, PROCESS,
                     SECTOR, SECTORS, SERVICES, STAGES, STATS, STORIES, ZARBAN)

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
DIST = ROOT / "dist"
ASSET_VERSION = "1"

FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def fa(n):
    return str(n).translate(FA_DIGITS)


def e(s):
    return html.escape(str(s), quote=True)


# ---------------------------------------------------------------- icons
_I = {
    "arrow": '<path d="M19 12H5"/><path d="M11 6l-6 6 6 6"/>',
    "chev-l": '<path d="M15 6l-6 6 6 6"/>',
    "chev-r": '<path d="M9 6l6 6-6 6"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7"/>',
    "pause": '<path d="M9 6v12"/><path d="M15 6v12"/>',
    "play": '<path d="M8 5.5v13l11-6.5z"/>',
    "close": '<path d="M6 6l12 12"/><path d="M18 6L6 18"/>',
    "menu": '<path d="M4 7h16"/><path d="M4 12h16"/><path d="M4 17h10"/>',
    "phone": '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 005 5L15 13l5 2v4a1 1 0 01-1 1A16 16 0 014 5a1 1 0 011-1z"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/>',
    "pin": '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0114 0C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
    "post": '<path d="M4 10a4 4 0 018 0v9H4z"/><path d="M12 19h8v-9a4 4 0 00-4-4H8"/><path d="M15 6V3h3"/>',
    "upload": '<path d="M12 16V4"/><path d="M7 9l5-5 5 5"/><path d="M4 16v3a1 1 0 001 1h14a1 1 0 001-1v-3"/>',
    "doc": '<path d="M14 3H6a1 1 0 00-1 1v16a1 1 0 001 1h12a1 1 0 001-1V8z"/><path d="M14 3v5h5"/><path d="M8.5 13h7M8.5 17h5"/>',
    "filter": '<path d="M4 5h16l-6 7.5V19l-4 2v-8.5z"/>',
    "chart": '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
    "search": '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
    "coins": '<ellipse cx="9" cy="7" rx="5" ry="2.5"/><path d="M4 7v4c0 1.4 2.2 2.5 5 2.5s5-1.1 5-2.5V7"/><path d="M10 15.4c.9 1.3 2.9 2.1 5 2.1 2.8 0 5-1.1 5-2.5v-4c0-1.2-1.6-2.2-3.8-2.4"/>',
    "seal": '<circle cx="12" cy="10" r="6"/><path d="M9 15.5L7.5 21l4.5-2 4.5 2-1.5-5.5"/><path d="M9.5 10l1.8 1.8L14.8 8.3"/>',
    "handshake": '<path d="M3 11l4-4 4 2 3-2 7 4"/><path d="M7 7v0M3 11l6 6a1.5 1.5 0 002.1 0l.4-.4M21 11l-5 5.5a1.5 1.5 0 01-2.1 0L10 12.6"/><path d="M13.5 15l1.5 1.5"/>',
    "calendar": '<rect x="4" y="5" width="16" height="15" rx="1.5"/><path d="M4 10h16"/><path d="M9 3v4M15 3v4"/>',
    "compass": '<circle cx="12" cy="12" r="8.5"/><path d="M15.5 8.5l-2 5-5 2 2-5z"/>',
    "helmet": '<path d="M4 17h16"/><path d="M5 17a7 7 0 0114 0"/><path d="M10 10V6.5h4V10"/><path d="M3 17v2h18v-2"/>',
    "cap": '<path d="M2.5 9.5L12 5l9.5 4.5L12 14z"/><path d="M6.5 11.5v4.5c1.5 1.3 3.3 2 5.5 2s4-.7 5.5-2v-4.5"/><path d="M21.5 9.5v5"/>',
    "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 19c.6-3.3 3-5 6-5s5.4 1.7 6 5"/><path d="M15.5 5.2a3.2 3.2 0 010 5.6M17.5 14.3c1.8.7 3 2.3 3.5 4.7"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
    "target": '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.5"/><circle cx="12" cy="12" r="1"/>',
    "flag": '<path d="M5 21V4"/><path d="M5 4h11l-2 4 2 4H5"/>',
    "quote": '<path d="M10 8H6.5A1.5 1.5 0 005 9.5V13h4v4H5"/><path d="M19 8h-3.5A1.5 1.5 0 0014 9.5V13h4v4h-4"/>',
    # sectors
    "mining": '<path d="M7 4h10l4 5-9 11L3 9z"/><path d="M3 9h18"/><path d="M10 4l2 5 2-5"/><path d="M12 9v11"/>',
    "transport": '<path d="M3 6.5h11v9.5H3z"/><path d="M14 10h4l3 3v3h-7"/><circle cx="7" cy="17.5" r="1.8"/><circle cx="17" cy="17.5" r="1.8"/>',
    "agri": '<path d="M12 20v-8"/><path d="M12 12c0-4 3-6.5 7-6.5 0 4-3 6.5-7 6.5z"/><path d="M12 14.5c0-3-2.5-5.5-6-5.5 0 3.5 2.5 5.5 6 5.5z"/><path d="M5 20h14"/>',
    "steel": '<path d="M5 4h14v3h-5v10h5v3H5v-3h5V7H5z"/>',
    "energy": '<path d="M13 3L5 14h6l-1 7 8-11h-6z"/>',
    "ai": '<rect x="7" y="7" width="10" height="10" rx="1.5"/><path d="M10 10h4v4h-4z"/><path d="M10 3v4M14 3v4M10 17v4M14 17v4M3 10h4M3 14h4M17 10h4M17 14h4"/>',
    "construction": '<path d="M3 21h18"/><path d="M7 21V3.5"/><path d="M4 6.5h16"/><path d="M7 10.5l4-4"/><path d="M17 6.5v4"/><path d="M15 10.5h4v3h-4z"/><path d="M10 21v-5h4v5"/>',
}


def icon(name, cls="ic"):
    return (f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{_I[name]}</svg>')


# ---------------------------------------------------------------- page shell
class Page:
    def __init__(self, path, title, desc, nav=None):
        self.path = path.strip("/")          # "" for home, "news/x" etc.
        self.depth = 0 if not self.path else self.path.count("/") + 1
        self.title = title
        self.desc = desc
        self.nav = nav

    def u(self, target=""):
        """relative URL from this page to a site path like 'news/', '#id' or 'assets/x.css'."""
        return ("../" * self.depth + target) or "./"

    def img(self, name):
        return self.u(f"assets/img/{name}.webp")


def picture(page, name, alt, cls="", w=1200, h=800, eager=False, sizes=None):
    loading = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return (f'<img class="{cls}" src="{page.img(name)}" alt="{e(alt)}" width="{w}" height="{h}" {loading}>')


def header(page):
    items = []
    for key, label, href in NAV:
        cur = ' aria-current="page"' if page.nav == key else ""
        items.append(f'<li><a href="{page.u(href)}"{cur}>{label}</a></li>')
    cta_cur = ' aria-current="page"' if page.nav == "apply" else ""
    return f'''<a class="skip" href="#main">رفتن به محتوای اصلی</a>
<header class="site-header" data-header>
  <div class="wrap header-in">
    <a class="brand" href="{page.u('')}" aria-label="صندوق باور — صفحه‌ی اصلی">
      <img src="{page.u('assets/brand/logo.png')}" alt="صندوق باور" width="72" height="69">
    </a>
    <nav class="main-nav" id="main-nav" aria-label="منوی اصلی">
      <ul>{"".join(items)}</ul>
      <a class="btn btn-primary nav-cta" href="{page.u('apply/')}"{cta_cur}>ارسال طرح / جذب سرمایه</a>
    </nav>
    <a class="btn btn-primary header-cta" href="{page.u('apply/')}"{cta_cur}>ارسال طرح / جذب سرمایه</a>
    <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="باز کردن منو">
      {icon("menu")}{icon("close", "ic ic-close")}
    </button>
  </div>
</header>'''


def partner_marks(page, light=True):
    logo = "logo-light.png" if light else "logo.png"
    return f'''<ul class="partners" aria-label="حامیان صندوق">
        <li><span class="pmark pmark-uni">{icon("cap")}</span><span>دانشگاه</span></li>
        <li><img src="{page.u('assets/brand/' + logo)}" alt="صندوق باور" width="56" height="54"><span>صندوق باور</span></li>
        <li><span class="pmark pmark-found">بنیاد</span><span>بنیاد</span></li>
      </ul>'''


def footer(page):
    services = "".join(f"<li>{s[0]}</li>" for s in SERVICES)
    return f'''<footer class="site-footer">
  <div class="wrap footer-grid">
    <section class="f-col">
      <h2>سرمایه‌گذاری هدفمند در صندوق باور</h2>
      <ul class="f-list">{services}</ul>
      <a class="f-link" href="{page.u('apply/')}">ارسال طرح و ثبت‌نام اولیه {icon("arrow")}</a>
    </section>
    <section class="f-col f-about">
      <h2>معرفی صندوق</h2>
      <p>{FUND["about_short"]}</p>
      {partner_marks(page)}
    </section>
    <section class="f-col">
      <h2>ارتباط با ما</h2>
      <ul class="f-contact">
        <li>{icon("pin")}<span>{FUND["address"]}</span></li>
        <li>{icon("phone")}<a href="tel:{FUND["phone_href"]}" dir="ltr">{FUND["phone"]}</a></li>
        <li>{icon("post")}<span>کد پستی: {FUND["postal"]}</span></li>
        <li>{icon("mail")}<a href="mailto:{FUND["email"]}" dir="ltr">{FUND["email"]}</a></li>
      </ul>
    </section>
  </div>
  <div class="wrap f-bottom">
    <p>© {fa(1405)} صندوق باور. همه‌ی حقوق محفوظ است.</p>
    <p class="demo-note">نسخه‌ی نمایشی — نام‌ها، آمار و اخبار نمونه هستند.</p>
  </div>
</footer>'''


def shell(page, body, extra_head="", base=""):
    title = page.title if page.path == "" else f"{page.title} | صندوق باور"
    return f'''<!doctype html>
<html lang="fa" dir="rtl">
<head>
<meta charset="utf-8">
{base}<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(page.desc)}">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#14331C">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(page.desc)}">
<meta property="og:locale" content="fa_IR">
<link rel="icon" type="image/png" href="{page.u('assets/brand/logo-mark.png')}">
<link rel="preload" href="{page.u('assets/fonts/Estedad-wght.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{page.u('assets/css/site.css')}?v={ASSET_VERSION}">
{extra_head}</head>
<body>
{header(page)}
<main id="main">
{body}
</main>
{footer(page)}
<script src="{page.u('assets/js/site.js')}?v={ASSET_VERSION}" defer></script>
</body>
</html>
'''


def section_head(title, desc=None, link=None, hid=None, light=False):
    hid_attr = f' id="{hid}"' if hid else ""
    d = f'<p class="sec-desc">{desc}</p>' if desc else ""
    l = f'<a class="sec-link" href="{link[1]}">{link[0]} {icon("arrow")}</a>' if link else ""
    return f'''<div class="sec-head{' is-light' if light else ''}">
      <div class="sec-titles"><h2{hid_attr}>{title}</h2>{d}</div>{l}
    </div>'''


def page_head(page, title, intro, crumbs=None, img=None, kicker=None):
    crumbs = crumbs or []
    trail = [f'<a href="{page.u("")}">خانه</a>'] + [
        (f'<a href="{page.u(h)}">{t}</a>' if h else f'<span aria-current="page">{t}</span>') for t, h in crumbs]
    k = f'<p class="ph-kicker">{kicker}</p>' if kicker else ""
    media = ""
    if img:
        media = f'<div class="ph-media">{picture(page, img, "", "ph-img", 1600, 900, eager=True)}</div>'
    return f'''<section class="page-head{' has-media' if img else ''}">
  <div class="wrap ph-in">
    <div class="ph-text">
      <nav class="crumbs" aria-label="مسیر صفحه">{' <span class="sep">/</span> '.join(trail)}</nav>
      {k}<h1>{title}</h1>
      <p class="ph-intro">{intro}</p>
    </div>
    {media}
  </div>
</section>'''


# ---------------------------------------------------------------- components
def sector_card(page, s, wide=False):
    return f'''<article class="sector-card{' is-wide' if wide else ''}">
        <span class="leaf-chip">{icon(s["icon"])}</span>
        <h3><a class="stretch" href="{page.u('sectors/' + s['slug'] + '/')}">{s["title"]}</a></h3>
        <p>{s["short"]}</p>
        <span class="more">مشاهده‌ی محور {icon("arrow")}</span>
      </article>'''


def company_card(page, c, with_dialog=True):
    s = SECTOR[c["sector"]]
    btn = (f'<button class="card-more" type="button" data-open="co-{c["slug"]}">جزئیات همکاری {icon("arrow")}</button>'
           if with_dialog else "")
    return f'''<article class="co-card" data-sector="{c["sector"]}">
        <div class="co-media">{picture(page, c["img"], "", "co-img", 1200, 800)}</div>
        <div class="co-body">
          <p class="co-sector">{s["title"].split("،")[0]}</p>
          <h3>{c["name"]}</h3>
          <p class="co-line">{c["desc"]}</p>
          <dl class="co-meta"><div><dt>ورود باور</dt><dd>{c["since"]}</dd></div><div><dt>مرحله</dt><dd>{c["stage"]}</dd></div></dl>
          {btn}
        </div>
      </article>'''


def company_dialog(page, c):
    s = SECTOR[c["sector"]]
    return f'''<dialog class="modal" id="co-{c["slug"]}" aria-labelledby="co-{c["slug"]}-t">
  <div class="modal-in">
    <button class="modal-x" type="button" data-close aria-label="بستن">{icon("close")}</button>
    <div class="modal-media">{picture(page, c["img"], "", "", 1200, 800)}</div>
    <div class="modal-body">
      <p class="co-sector">{s["title"]}</p>
      <h2 id="co-{c["slug"]}-t">{c["name"]}</h2>
      <p class="modal-lead">{c["line"]}</p>
      <p>{c["desc"]}</p>
      <h3>نقش باور</h3>
      <p>{c["role"]}</p>
      <dl class="co-meta"><div><dt>ورود باور</dt><dd>{c["since"]}</dd></div><div><dt>مرحله</dt><dd>{c["stage"]}</dd></div></dl>
      <a class="text-link" href="{page.u('sectors/' + s['slug'] + '/')}">محور {s["title"].split("،")[0]} {icon("arrow")}</a>
    </div>
  </div>
</dialog>'''


def story_card(page, i, st):
    co = next(c for c in PORTFOLIO if c["slug"] == st["company"])
    return f'''<article class="story-card">
        <figure class="story-fig">{picture(page, st["img"], st["name"], "story-img", 800, 1000)}
          <figcaption>{co["name"]}</figcaption></figure>
        <blockquote><p>«{st["quote"]}»</p></blockquote>
        <p class="story-by"><strong>{st["name"]}</strong><span>{st["role"]}، {co["name"]}</span></p>
        <button class="card-more" type="button" data-open="story-{i}">خواندن روایت کامل {icon("arrow")}</button>
      </article>'''


def story_dialog(page, i, st):
    co = next(c for c in PORTFOLIO if c["slug"] == st["company"])
    paras = "".join(f"<p>{p}</p>" for p in st["story"])
    return f'''<dialog class="modal modal-story" id="story-{i}" aria-labelledby="story-{i}-t">
  <div class="modal-in">
    <button class="modal-x" type="button" data-close aria-label="بستن">{icon("close")}</button>
    <div class="modal-media">{picture(page, st["img"], st["name"], "", 800, 1000)}</div>
    <div class="modal-body">
      <p class="co-sector">{co["name"]}، {SECTOR[co["sector"]]["title"].split("،")[0]}</p>
      <h2 id="story-{i}-t">«{st["quote"]}»</h2>
      {paras}
      <p class="story-by"><strong>{st["name"]}</strong><span>{st["role"]}، {co["name"]}</span></p>
    </div>
  </div>
</dialog>'''


def news_card(page, n, big=False):
    return f'''<article class="news-card{' is-big' if big else ''}" data-type="{n["type"]}">
        <div class="news-media">{picture(page, n["img"], "", "news-img", 1200, 750)}
          <span class="badge">{NEWS_TYPE_LABEL[n["type"]]}</span></div>
        <div class="news-body">
          <time>{n["date"]}</time>
          <h3><a class="stretch" href="{page.u('news/' + n['slug'] + '/')}">{n["title"]}</a></h3>
          <p>{n["lead"]}</p>
        </div>
      </article>'''


def news_tabs(target):
    tabs = "".join(
        f'<button type="button" role="tab" aria-selected="{"true" if k == "all" else "false"}" data-filter="{k}">{v}</button>'
        for k, v in NEWS_TYPES)
    return f'<div class="tabs" role="tablist" aria-label="نوع مطلب" data-filter-group="{target}">{tabs}</div>'


def dot_matrix():
    cols, total = 30, STATS["received"]
    rows = -(-total // cols)
    gap = 16
    out = []
    for i in range(total):
        r, c = divmod(i, cols)
        x = (cols - 1 - c) * gap + gap / 2
        y = r * gap + gap / 2
        cls = "d-act" if i < STATS["active"] else ("d-eval" if i < STATS["active"] + STATS["evaluating"] else "d")
        out.append(f'<circle class="{cls}" cx="{x:g}" cy="{y:g}" r="4.4" style="--i:{r}"/>')
    return (f'<svg class="dots" viewBox="0 0 {cols*gap} {rows*gap}" role="img" '
            f'aria-label="{fa(total)} طرح دریافت‌شده؛ {fa(STATS["evaluating"])} طرح در حال ارزیابی و {fa(STATS["active"])} سرمایه‌گذاری جاری">'
            + "".join(out) + "</svg>")


# ---------------------------------------------------------------- pages
def home():
    p = Page("", "صندوق باور | سرمایه‌گذاری خطرپذیر در فناوری‌های صنایع پایه",
             "صندوق باور در فناوری‌های معدن، فولاد، انرژی، حمل‌ونقل، کشاورزی، ساختمان و هوشمندسازی صنعتی سرمایه‌گذاری می‌کند.")

    slides, tabs = [], []
    for i, h in enumerate(HERO):
        tag = "h1" if i == 0 else "h2"
        cta = f'<a class="btn btn-light" href="{p.u(h["cta"][1]) if not h["cta"][1].startswith("#") else h["cta"][1]}">{h["cta"][0]} {icon("arrow")}</a>'
        cta2 = ""
        if h["cta2"]:
            href = h["cta2"][1] if h["cta2"][1].startswith("#") else p.u(h["cta2"][1])
            cta2 = f'<a class="btn btn-ghost-light" href="{href}">{h["cta2"][0]}</a>'
        slides.append(f'''<div class="slide{' is-active' if i == 0 else ''}" id="slide-{i}" role="tabpanel" aria-roledescription="اسلاید" aria-label="{fa(i+1)} از {fa(len(HERO))}"{'' if i == 0 else ' hidden'}>
        {picture(p, h["img"], "", "slide-img", 1920, 1080, eager=(i == 0))}
        <div class="wrap slide-in">
          <div class="slide-text">
            <p class="slide-kind">{h["kind"]}</p>
            <{tag} class="slide-title">{h["title"]}</{tag}>
            <p class="slide-lead">{h["text"]}</p>
            <div class="slide-cta">{cta}{cta2}</div>
          </div>
        </div>
      </div>''')
        tabs.append(f'<button type="button" role="tab" aria-controls="slide-{i}" aria-selected="{"true" if i == 0 else "false"}" data-slide="{i}"><span class="bar"><i></i></span><span class="t">{h["title"] if i else h["kind"]}</span></button>')

    hero = f'''<section class="hero" aria-roledescription="اسلایدر" aria-label="بنر اصلی" data-slider>
  <div class="slides">{"".join(slides)}</div>
  <div class="wrap hero-nav">
    <div class="hero-tabs" role="tablist" aria-label="انتخاب اسلاید">{"".join(tabs)}</div>
    <button class="hero-pause" type="button" data-pause aria-label="توقف نمایش خودکار">{icon("pause", "ic ic-pause")}{icon("play", "ic ic-play")}</button>
  </div>
</section>'''

    row1 = "".join(sector_card(p, s) for s in SECTORS[:4])
    row2 = "".join(sector_card(p, s, wide=True) for s in SECTORS[4:])
    sectors = f'''<section class="sec sec-paper" aria-labelledby="sectors">
  <div class="wrap">
    {section_head("محورهای سرمایه‌گذاری", "هفت حوزه‌ای که در آن‌ها طرح می‌پذیریم؛ هر محور با مسائل اولویت‌دار صنایع همکار تعریف شده است.", hid="sectors")}
    <div class="sector-grid">{row1}{row2}</div>
  </div>
</section>'''

    st = STATS
    pct = round(st["active"] * 100 / st["received"], 1)
    status = f'''<section class="sec sec-forest status" aria-labelledby="status-t" data-status>
  <div class="wrap status-in">
    <div class="status-text">
      <h2 id="status-t">وضعیت پروژه‌ها</h2>
      <p class="sec-desc">آمار و ارقام قیف ارزیابی صندوق از آغاز فعالیت تا {FUND["updated"]}. هر نقطه یک طرح دریافت‌شده است.</p>
      <ul class="stat-list">
        <li class="st-act"><span class="sw"></span><span class="lbl">جاری {icon("check", "ic ic-sm")}</span><strong data-count="{st["active"]}">{fa(st["active"])}</strong><span class="note">سرمایه‌گذاری فعال در شرکت‌های فناور صنعتی</span></li>
        <li class="st-eval"><span class="sw"></span><span class="lbl">در حال ارزیابی</span><strong data-count="{st["evaluating"]}">{fa(st["evaluating"])}</strong><span class="note">طرح در مراحل ارزیابی فنی، مالی و حقوقی</span></li>
        <li class="st-rec"><span class="sw"></span><span class="lbl">طرح‌های دریافت‌شده</span><strong data-count="{st["received"]}" data-plus>{fa(st["received"])}+</strong><span class="note">طرح فناورانه و صنعتی ثبت‌شده در سامانه</span></li>
      </ul>
    </div>
    <figure class="status-fig">
      {dot_matrix()}
      <figcaption>از هر صد طرح دریافتی، حدود {fa(str(pct).replace(".", "٫"))} طرح به سرمایه‌گذاری رسیده است.</figcaption>
    </figure>
  </div>
</section>'''

    steps = "".join(f'''<li class="step" style="--s:{i}">
        <div class="step-top"><span class="step-n">{fa(i+1)}</span>{icon(s["icon"])}</div>
        <h3>{s["title"]}</h3>
        <p>{s["text"]}</p>
        <span class="step-time">{icon("clock", "ic ic-sm")}{s["time"]}</span>
      </li>''' for i, s in enumerate(PROCESS))
    process = f'''<section class="sec" aria-labelledby="process">
  <div class="wrap">
    {section_head("فرایند پذیرش طرح", "مسیر شفاف از ثبت طرح تا قرارداد؛ زمان‌ها تقریبی است و به کامل‌بودن مدارک بستگی دارد.", ("ارسال طرح", p.u("apply/")), hid="process")}
    <ol class="steps">{steps}</ol>
  </div>
</section>'''

    feat = [c for c in PORTFOLIO if c["featured"]]
    portfolio = f'''<section class="sec sec-paper" aria-labelledby="pf-t">
  <div class="wrap">
    {section_head("پرتفوی منتخب", "نمونه‌ای از شرکت‌هایی که در محورهای مختلف سرمایه‌گذاری با آن‌ها همراه شده‌ایم.", ("همه‌ی شرکت‌ها", p.u("portfolio/")), hid="pf-t")}
    <div class="co-grid">{"".join(company_card(p, c) for c in feat)}</div>
  </div>
</section>'''

    stories = f'''<section class="sec" aria-labelledby="stories-t">
  <div class="wrap">
    {section_head("روایت باور", "تجربه‌ی همکاری از زبان بنیان‌گذاران.", hid="stories-t")}
    <div class="story-grid">{"".join(story_card(p, i, s) for i, s in enumerate(STORIES))}</div>
  </div>
</section>'''

    news = f'''<section class="sec sec-paper" aria-labelledby="news-t">
  <div class="wrap">
    {section_head("اخبار و رویدادها", "مقالات، اخبار و گزارش‌های صندوق.", ("همه‌ی مطالب", p.u("news/")), hid="news-t")}
    {news_tabs("home-news")}
    <div class="news-grid" id="home-news" data-limit="4">{"".join(news_card(p, n) for n in NEWS)}</div>
    <p class="empty" hidden>در این دسته هنوز مطلبی منتشر نشده است. <a href="{p.u('news/')}">همه‌ی مطالب را ببینید</a>.</p>
  </div>
</section>'''

    dialogs = "".join(company_dialog(p, c) for c in feat) + "".join(story_dialog(p, i, s) for i, s in enumerate(STORIES))
    body = hero + sectors + status + process + portfolio + stories + news + cta_band(p) + dialogs
    return p, shell(p, body)


def cta_band(p, title="ارسال طرح و مدارک جهت جذب سرمایه", text=None):
    text = text or "طرح خود را در یکی از هفت محور سرمایه‌گذاری ثبت کنید. پیش از شروع، این مدارک را آماده داشته باشید:"
    docs = "".join(f"<li>{icon('check', 'ic ic-sm')}{d}</li>" for d in APPLY_DOCS)
    return f'''<section class="cta-wrap" aria-labelledby="cta-t">
  <div class="wrap">
    <div class="cta">
      <img class="cta-mark" src="{p.u('assets/brand/logo-mark.png')}" alt="" width="328" height="327" loading="lazy">
      <div class="cta-text">
        <h2 id="cta-t">{title}</h2>
        <p>{text}</p>
        <ul class="cta-docs">{docs}</ul>
      </div>
      <a class="btn btn-light btn-lg" href="{p.u('apply/')}">ارسال طرح و ثبت‌نام اولیه {icon("arrow")}</a>
    </div>
  </div>
</section>'''


def portfolio_page():
    p = Page("portfolio", "پرتفولیو", "شرکت‌های فناوری که صندوق باور در آن‌ها سرمایه‌گذاری کرده است.", nav="portfolio")
    chips = ['<button type="button" role="tab" aria-selected="true" data-filter="all">همه</button>'] + [
        f'<button type="button" role="tab" aria-selected="false" data-filter="{s["slug"]}">{s["title"].split("،")[0]}</button>'
        for s in SECTORS if any(c["sector"] == s["slug"] for c in PORTFOLIO)]
    body = page_head(p, "پرتفولیو", "شرکت‌هایی که با سرمایه و شبکه‌ی صنعتی باور از آزمایشگاه به خط تولید رسیده‌اند.",
                     [("پرتفولیو", None)])
    body += f'''<section class="sec">
  <div class="wrap">
    <ul class="kpis">
      <li><strong>{fa(STATS["active"])}</strong><span>سرمایه‌گذاری جاری</span></li>
      <li><strong>{fa(7)}</strong><span>محور سرمایه‌گذاری</span></li>
      <li><strong>{fa(STATS["evaluating"])}</strong><span>طرح در حال ارزیابی</span></li>
    </ul>
    <div class="tabs" role="tablist" aria-label="فیلتر بر اساس محور" data-filter-group="pf-all" data-attr="sector">{"".join(chips)}</div>
    <div class="co-grid co-grid-all" id="pf-all">{"".join(company_card(p, c) for c in PORTFOLIO)}</div>
  </div>
</section>
<section class="sec sec-paper" aria-labelledby="stories-t">
  <div class="wrap">
    {section_head("روایت باور", "تجربه‌ی همکاری از زبان بنیان‌گذاران.", hid="stories-t")}
    <div class="story-grid">{"".join(story_card(p, i, s) for i, s in enumerate(STORIES))}</div>
  </div>
</section>'''
    body += cta_band(p)
    body += "".join(company_dialog(p, c) for c in PORTFOLIO) + "".join(story_dialog(p, i, s) for i, s in enumerate(STORIES))
    return p, shell(p, body)


def sector_page(s):
    p = Page(f"sectors/{s['slug']}", s["title"], s["short"], nav=None)
    focus = "".join(f"<li>{icon('target', 'ic')}<span>{f}</span></li>" for f in s["focus"])
    cos = [c for c in PORTFOLIO if c["sector"] == s["slug"]]
    co_html = ""
    if cos:
        co_html = f'''<section class="sec sec-paper" aria-labelledby="sc-t">
  <div class="wrap">
    {section_head("شرکت‌های این محور", None, ("همه‌ی پرتفولیو", p.u("portfolio/")), hid="sc-t")}
    <div class="co-grid">{"".join(company_card(p, c) for c in cos)}</div>
  </div>
</section>''' + "".join(company_dialog(p, c) for c in cos)
    others = "".join(
        f'<li><a href="{p.u("sectors/" + o["slug"] + "/")}"><span class="leaf-chip sm">{icon(o["icon"])}</span>{o["title"]}</a></li>'
        for o in SECTORS if o["slug"] != s["slug"])
    body = page_head(p, s["title"], s["short"], [("محورهای سرمایه‌گذاری", "#sectors"), (s["title"].split("،")[0], None)],
                     img=s["img"], kicker="محور سرمایه‌گذاری")
    body += f'''<section class="sec">
  <div class="wrap two-col">
    <div>
      <h2 class="h2">مسائل اولویت‌دار</h2>
      <p class="muted">طرح‌هایی که یکی از این مسائل را حل می‌کنند، در غربالگری اولویت دارند.</p>
      <ul class="focus-list">{focus}</ul>
    </div>
    <aside class="side-card">
      <h2 class="h3">معیارهای پذیرش در این محور</h2>
      <ul class="check-list">
        <li>{icon("check", "ic ic-sm")}دست‌کم نمونه‌ی آزمایشگاهی (TRL ۴ به بالا)</li>
        <li>{icon("check", "ic ic-sm")}مسئله‌ی مشخص در یک صنعت یا کارخانه</li>
        <li>{icon("check", "ic ic-sm")}تیم متعهد با تجربه‌ی فنی مرتبط</li>
        <li>{icon("check", "ic ic-sm")}مسیر روشن تا استقرار و فروش صنعتی</li>
      </ul>
      <a class="btn btn-primary" href="{p.u('apply/')}?sector={s['slug']}">ارسال طرح در این محور {icon("arrow")}</a>
    </aside>
  </div>
</section>''' + co_html + f'''<section class="sec">
  <div class="wrap">
    {section_head("سایر محورها")}
    <ul class="other-sectors">{others}</ul>
  </div>
</section>'''
    return p, shell(p, body)


def news_index():
    p = Page("news", "اخبار و رویدادها", "اخبار، مقالات، گزارش‌ها و رویدادهای صندوق باور.", nav="news")
    body = page_head(p, "اخبار و رویدادها", "اخبار صندوق، مقالات تحلیلی، گزارش‌ها و رویدادهای پیش‌رو.", [("اخبار", None)])
    body += f'''<section class="sec">
  <div class="wrap">
    {news_tabs("news-all")}
    <div class="news-grid news-grid-all" id="news-all">{news_card(p, NEWS[0], big=True)}{"".join(news_card(p, n) for n in NEWS[1:])}</div>
    <p class="empty" hidden>در این دسته هنوز مطلبی منتشر نشده است.</p>
  </div>
</section>'''
    return p, shell(p, body)


def news_article(n):
    p = Page(f"news/{n['slug']}", n["title"], n["lead"], nav="news")
    paras = "".join(f"<p>{x}</p>" for x in n["body"])
    related = [x for x in NEWS if x["slug"] != n["slug"]][:3]
    body = f'''<article class="article">
  <header class="wrap article-head">
    <nav class="crumbs" aria-label="مسیر صفحه"><a href="{p.u('')}">خانه</a> <span class="sep">/</span> <a href="{p.u('news/')}">اخبار</a></nav>
    <p class="article-meta"><span class="badge badge-soft">{NEWS_TYPE_LABEL[n["type"]]}</span><time>{n["date"]}</time></p>
    <h1>{n["title"]}</h1>
    <p class="article-lead">{n["lead"]}</p>
  </header>
  <div class="wrap article-media">{picture(p, n["img"], "", "", 1200, 750, eager=True)}</div>
  <div class="wrap article-body">{paras}
    <p class="demo-inline">این متن نمونه است و در نسخه‌ی نهایی با خبر واقعی جایگزین می‌شود.</p>
  </div>
</article>
<section class="sec sec-paper" aria-labelledby="rel-t">
  <div class="wrap">
    {section_head("مطالب دیگر", None, ("همه‌ی مطالب", p.u("news/")), hid="rel-t")}
    <div class="news-grid news-grid-3">{"".join(news_card(p, x) for x in related)}</div>
  </div>
</section>'''
    return p, shell(p, body)


def about_page():
    p = Page("about", "درباره ما", FUND["about_short"], nav="about")
    services = "".join(f'''<li><span class="leaf-chip">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></li>''' for t, d, ic in
                       [("سرمایه‌ی مرحله‌ای", "تزریق سرمایه متناسب با دستاوردهای فنی و تجاری هر مرحله.", "coins")] + SERVICES)
    principles = [
        ("مسئله‌ی واقعی صنعت", "طرحی را می‌پذیریم که مشتری صنعتی مشخص و مسئله‌ی قابل‌اندازه‌گیری داشته باشد."),
        ("تیم پیش از ایده", "تیمی که بتواند محصول را به خط تولید برساند، از ایده‌ی درخشان مهم‌تر است."),
        ("همراهی تا استقرار", "کار ما با امضای قرارداد تمام نمی‌شود؛ تا نخستین استقرار صنعتی کنار تیم می‌مانیم."),
    ]
    pr = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in principles)
    body = page_head(p, "درباره‌ی صندوق باور", FUND["about_short"], [("درباره ما", None)], img="hero-call")
    body += f'''<section class="sec">
  <div class="wrap">
    {section_head("آنچه به تیم‌ها می‌دهیم", "سرمایه تنها بخشی از همکاری است؛ بخش مهم‌تر، دسترسی به صنعت است.")}
    <ul class="service-grid">{services}</ul>
  </div>
</section>
<section class="sec sec-forest">
  <div class="wrap">
    {section_head("اصول سرمایه‌گذاری", None, light=True)}
    <ol class="principles">{pr}</ol>
  </div>
</section>
<section class="sec">
  <div class="wrap two-col">
    <div>
      <h2 class="h2">پشتوانه‌ی صندوق</h2>
      <p class="muted">صندوق باور با همراهی بنیاد و دانشگاه تأسیس شده تا پیوند میان پژوهش دانشگاهی و نیاز صنایع بزرگ کشور را کوتاه‌تر کند.</p>
      <div class="backers">{partner_marks(p, light=False)}</div>
    </div>
    <aside class="side-card" id="contact">
      <h2 class="h3">ارتباط با ما</h2>
      <ul class="f-contact dark">
        <li>{icon("pin")}<span>{FUND["address"]}</span></li>
        <li>{icon("phone")}<a href="tel:{FUND["phone_href"]}" dir="ltr">{FUND["phone"]}</a></li>
        <li>{icon("post")}<span>کد پستی: {FUND["postal"]}</span></li>
        <li>{icon("mail")}<a href="mailto:{FUND["email"]}" dir="ltr">{FUND["email"]}</a></li>
      </ul>
    </aside>
  </div>
</section>''' + cta_band(p)
    return p, shell(p, body)


def club_page():
    p = Page("club", "باشگاه فن باور", "باشگاه دانشجویان، پژوهشگران و مهندسان علاقه‌مند به حل مسائل صنعت.", nav="club")
    progs = "".join(f'<li><span class="leaf-chip">{icon(ic)}</span><h3>{t}</h3><p>{d}</p></li>' for t, d, ic in CLUB_PROGRAMS)
    events = "".join(f'''<li><time>{d}</time><span class="badge badge-soft">{k}</span><h3>{t}</h3><p>{icon("pin", "ic ic-sm")}{where}</p></li>'''
                     for d, k, t, where in CLUB_EVENTS)
    body = page_head(p, "باشگاه فن باور", "جایی برای دانشجویان، پژوهشگران و مهندسانی که می‌خواهند مسئله‌ی صنعت را از نزدیک ببینند و راه‌حل خود را به محصول برسانند.",
                     [("باشگاه فن باور", None)], img="hero-club")
    body += f'''<section class="sec">
  <div class="wrap">
    {section_head("برنامه‌های باشگاه", "عضویت رایگان است و با ثبت‌نام، برنامه‌های هر ماه برایتان ارسال می‌شود.")}
    <ul class="service-grid">{progs}</ul>
  </div>
</section>
<section class="sec sec-paper">
  <div class="wrap two-col">
    <div>
      <h2 class="h2">برنامه‌های پیش‌رو</h2>
      <ul class="event-list">{events}</ul>
    </div>
    <aside class="side-card" id="join">
      <h2 class="h3">عضویت در باشگاه</h2>
      <form class="form" data-demo-form novalidate>
        <div class="field"><label for="c-name">نام و نام خانوادگی</label><input id="c-name" name="name" required autocomplete="name"></div>
        <div class="field"><label for="c-mail">ایمیل</label><input id="c-mail" name="email" type="email" dir="ltr" required autocomplete="email"></div>
        <div class="field"><label for="c-role">شما</label>
          <select id="c-role" name="role" required><option value="">انتخاب کنید</option><option>دانشجوی کارشناسی</option><option>دانشجوی تحصیلات تکمیلی</option><option>پژوهشگر یا عضو هیئت علمی</option><option>مهندس یا کارشناس صنعت</option></select></div>
        <div class="field"><label for="c-field">رشته یا حوزه‌ی کاری</label><input id="c-field" name="field"></div>
        <button class="btn btn-primary btn-block" type="submit">عضو می‌شوم</button>
        <p class="form-ok" role="status" hidden>{icon("check", "ic ic-sm")} عضویت شما ثبت شد. برنامه‌ی ماه بعد به ایمیلتان ارسال می‌شود.</p>
      </form>
    </aside>
  </div>
</section>'''
    return p, shell(p, body)


def zarban_page():
    z = ZARBAN
    p = Page("zarban", "رویداد ملی ضربان", "رقابت ملی تیم‌های فناور برای حل چالش‌های واقعی صنایع.", nav="zarban")
    steps = "".join(f'<li><span class="zs-n">{fa(i+1)}</span><div><h3>{t}</h3><time>{d}</time><p>{x}</p></div></li>'
                    for i, (t, d, x) in enumerate(z["steps"]))
    ch = "".join(f"<li>{icon('flag', 'ic')}<span>{c}</span></li>" for c in z["challenges"])
    sup = "".join(f"<li><h3>{t}</h3><p>{d}</p></li>" for t, d in z["support"])
    faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in z["faq"])
    body = f'''<section class="z-hero">
  {picture(p, "hero-zarban", "", "z-hero-img", 1920, 1080, eager=True)}
  <div class="wrap z-hero-in">
    <nav class="crumbs" aria-label="مسیر صفحه"><a href="{p.u('')}">خانه</a> <span class="sep">/</span> <span aria-current="page">رویداد ملی ضربان</span></nav>
    <p class="ph-kicker">{z["edition"]}، {z["theme"]}</p>
    <h1>رویداد ملی ضربان</h1>
    <p class="ph-intro">رقابت ملی تیم‌های فناور برای حل چالش‌های واقعی صنعت؛ این دوره با محوریت {z["theme"]}.</p>
    <dl class="z-facts">
      <div><dt>مهلت ثبت‌نام</dt><dd>{z["reg_deadline"]}</dd></div>
      <div><dt>روز ارائه</dt><dd>{z["final_date"]}</dd></div>
      <div><dt>محل برگزاری</dt><dd>{z["place"]}</dd></div>
    </dl>
    <a class="btn btn-light btn-lg" href="{p.u('apply/')}?from=zarban">ثبت‌نام تیم در ضربان {icon("arrow")}</a>
  </div>
</section>
<section class="sec">
  <div class="wrap two-col">
    <div>
      <h2 class="h2">چالش‌های این دوره</h2>
      <p class="muted">چالش‌ها را واحدهای صنعتی همکار مطرح کرده‌اند و داده‌ی لازم برای کار روی آن‌ها در بوت‌کمپ در اختیار تیم‌ها قرار می‌گیرد.</p>
      <ul class="focus-list">{ch}</ul>
    </div>
    <aside class="side-card">
      <h2 class="h3">برای تیم‌های برگزیده</h2>
      <ul class="support-list">{sup}</ul>
    </aside>
  </div>
</section>
<section class="sec sec-paper">
  <div class="wrap">
    {section_head("زمان‌بندی رویداد")}
    <ol class="z-steps">{steps}</ol>
  </div>
</section>
<section class="sec">
  <div class="wrap faq-wrap">
    <h2 class="h2">پرسش‌های پرتکرار</h2>
    <div class="faq">{faq}</div>
  </div>
</section>''' + cta_band(p, "طرح شما به چالش‌های ضربان نمی‌خورد؟",
                         "می‌توانید طرح را مستقیم در یکی از هفت محور سرمایه‌گذاری ثبت کنید. پیش از شروع، این مدارک را آماده داشته باشید:")
    return p, shell(p, body)


def apply_page():
    p = Page("apply", "ارسال طرح و ثبت‌نام اولیه", "طرح فناورانه‌ی خود را برای ارزیابی و جذب سرمایه به صندوق باور ارسال کنید.", nav="apply")
    sector_opts = "".join(f'<option value="{s["slug"]}">{s["title"]}</option>' for s in SECTORS)
    stage_opts = "".join(
        f'<label class="radio-card"><input type="radio" name="stage" value="{k}" required><span><strong>{t}</strong><small>{trl}</small></span></label>'
        for k, t, trl in STAGES)
    docs = "".join(f"<li>{icon('check', 'ic ic-sm')}{d}</li>" for d in APPLY_DOCS)
    steps_side = "".join(f"<li><span>{fa(i+1)}</span>{s['title']}<small>{s['time']}</small></li>" for i, s in enumerate(PROCESS))
    body = page_head(p, "ارسال طرح و ثبت‌نام اولیه",
                     "فرم را در چهار گام کامل کنید. تا ارسال نهایی، پیش‌نویس روی همین مرورگر ذخیره می‌شود.",
                     [("ارسال طرح", None)])
    body += f'''<section class="sec">
  <div class="wrap apply-grid">
    <form class="form apply-form" id="apply-form" data-apply novalidate>
      <ol class="stepper" aria-label="گام‌های فرم">
        <li class="is-current" data-step-ind="0"><span>۱</span>متقاضی</li>
        <li data-step-ind="1"><span>۲</span>طرح</li>
        <li data-step-ind="2"><span>۳</span>تیم</li>
        <li data-step-ind="3"><span>۴</span>مدارک</li>
      </ol>

      <fieldset class="fstep" data-step="0">
        <legend>اطلاعات متقاضی</legend>
        <div class="grid-2">
          <div class="field"><label for="a-name">نام و نام خانوادگی</label><input id="a-name" name="name" required autocomplete="name"></div>
          <div class="field"><label for="a-role">سمت در تیم</label><input id="a-role" name="role" placeholder="مثلاً مدیرعامل یا هم‌بنیان‌گذار"></div>
          <div class="field"><label for="a-mobile">شماره‌ی همراه</label><input id="a-mobile" name="mobile" dir="ltr" inputmode="tel" required pattern="^(\\+98|0)?9\\d{{9}}$" placeholder="09xxxxxxxxx" autocomplete="tel"><small class="err">شماره را به شکل ۰۹۱۲۳۴۵۶۷۸۹ وارد کنید.</small></div>
          <div class="field"><label for="a-email">ایمیل</label><input id="a-email" name="email" type="email" dir="ltr" required autocomplete="email"><small class="err">یک ایمیل معتبر وارد کنید.</small></div>
        </div>
        <div class="field"><span class="label">نوع متقاضی</span>
          <div class="seg">
            <label><input type="radio" name="kind" value="team" required checked><span>تیم (بدون شرکت)</span></label>
            <label><input type="radio" name="kind" value="startup"><span>شرکت نوپا</span></label>
            <label><input type="radio" name="kind" value="kb"><span>شرکت دانش‌بنیان</span></label>
          </div>
        </div>
      </fieldset>

      <fieldset class="fstep" data-step="1" hidden>
        <legend>معرفی طرح</legend>
        <div class="field"><label for="a-title">عنوان طرح</label><input id="a-title" name="title" required></div>
        <div class="field"><label for="a-sector">محور سرمایه‌گذاری</label><select id="a-sector" name="sector" required><option value="">انتخاب کنید</option>{sector_opts}</select></div>
        <div class="field"><span class="label">مرحله‌ی فعلی طرح</span><div class="radio-cards">{stage_opts}</div><small class="err">مرحله‌ی طرح را انتخاب کنید.</small></div>
        <div class="field"><label for="a-summary">خلاصه‌ی طرح</label>
          <textarea id="a-summary" name="summary" rows="5" maxlength="800" required placeholder="چه مسئله‌ای را در کدام صنعت حل می‌کنید و راه‌حل شما چه تفاوتی با راه‌حل‌های موجود دارد؟"></textarea>
          <small class="hint"><span data-counter="a-summary">۰</span> از ۸۰۰ نویسه</small></div>
        <div class="field"><label for="a-need">سرمایه‌ی مورد نیاز (میلیارد ریال)</label><input id="a-need" name="need" inputmode="numeric" dir="ltr" placeholder="مثلاً 50"></div>
      </fieldset>

      <fieldset class="fstep" data-step="2" hidden>
        <legend>تیم</legend>
        <div class="grid-2">
          <div class="field"><label for="a-size">تعداد اعضای تمام‌وقت</label><input id="a-size" name="size" type="number" min="1" max="200" dir="ltr" required></div>
          <div class="field"><label for="a-city">شهر</label><input id="a-city" name="city"></div>
        </div>
        <div class="field"><label for="a-team">معرفی اعضای کلیدی</label>
          <textarea id="a-team" name="team" rows="5" required placeholder="نام، نقش و سابقه‌ی مرتبط هر یک از اعضای کلیدی"></textarea></div>
        <div class="field"><label for="a-link">لینک وب‌سایت یا صفحه‌ی معرفی (اختیاری)</label><input id="a-link" name="link" type="url" dir="ltr" placeholder="https://"></div>
      </fieldset>

      <fieldset class="fstep" data-step="3" hidden>
        <legend>بارگذاری مدارک</legend>
        <div class="field"><span class="label">ارائه‌ی طرح (Pitch deck) — PDF، حداکثر ۲۰ مگابایت</span>
          <label class="drop"><input type="file" name="deck" accept="application/pdf" required>{icon("upload")}<span class="drop-t">فایل را انتخاب کنید یا اینجا رها کنید</span></label>
          <small class="err">بارگذاری ارائه‌ی طرح الزامی است.</small></div>
        <div class="field"><span class="label">طرح کسب‌وکار یا مستندات فنی (اختیاری)</span>
          <label class="drop"><input type="file" name="extra" accept=".pdf,.doc,.docx,.xlsx">{icon("doc")}<span class="drop-t">فایل را انتخاب کنید</span></label></div>
        <label class="check"><input type="checkbox" name="agree" required><span>تأیید می‌کنم اطلاعات واردشده درست است و صندوق باور می‌تواند برای ارزیابی با من تماس بگیرد.</span></label>
        <div class="review" data-review></div>
      </fieldset>

      <div class="form-nav">
        <button class="btn btn-ghost" type="button" data-prev hidden>{icon("chev-r", "ic ic-sm")} گام قبل</button>
        <span class="draft" data-draft role="status"></span>
        <button class="btn btn-primary" type="button" data-next>گام بعد {icon("chev-l", "ic ic-sm")}</button>
        <button class="btn btn-primary" type="submit" data-submit hidden>ارسال طرح {icon("arrow")}</button>
      </div>
    </form>

    <div class="apply-done" data-done hidden tabindex="-1">
      <span class="done-ic">{icon("check")}</span>
      <h2>طرح شما ثبت شد</h2>
      <p>کد پیگیری: <strong dir="ltr" data-code></strong></p>
      <p class="muted">نتیجه‌ی غربالگری حداکثر دو هفته بعد به ایمیل و شماره‌ی همراه شما اعلام می‌شود.</p>
      <p class="demo-inline">این نسخه‌ی نمایشی است و اطلاعات فرم به جایی ارسال نمی‌شود.</p>
      <a class="btn btn-ghost" href="{p.u('')}">بازگشت به صفحه‌ی اصلی</a>
    </div>

    <aside class="apply-side">
      <div class="side-card">
        <h2 class="h3">پیش از شروع آماده کنید</h2>
        <ul class="check-list">{docs}</ul>
      </div>
      <div class="side-card">
        <h2 class="h3">پس از ارسال چه می‌شود؟</h2>
        <ol class="mini-steps">{steps_side}</ol>
      </div>
      <p class="side-help">پرسشی دارید؟ <a href="tel:{FUND["phone_href"]}" dir="ltr">{FUND["phone"]}</a></p>
    </aside>
  </div>
</section>'''
    return p, shell(p, body)


def not_found():
    p = Page("", "صفحه پیدا نشد", "صفحه‌ی مورد نظر پیدا نشد.")
    # 404.html sits at the root but may be served for any depth → use absolute-from-root links via <base>
    body = f'''<section class="sec nf">
  <div class="wrap">
    <h1>این صفحه پیدا نشد</h1>
    <p class="muted">نشانی را بررسی کنید یا از صفحه‌ی اصلی ادامه دهید.</p>
    <a class="btn btn-primary" href="./">صفحه‌ی اصلی</a>
  </div>
</section>'''
    base = '<script>(function(){var p=location.pathname.split("/");var b=(location.hostname.endsWith("github.io")&&p[1])?"/"+p[1]+"/":"/";document.write(\'<base href="\'+b+\'">\');})();</script>\n'
    return shell(p, body, base=base)


# ---------------------------------------------------------------- build
def write(page_path, html_text):
    out = DIST / page_path / "index.html" if page_path else DIST / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html_text, encoding="utf-8")


def build():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(SRC, DIST)
    pages = [home(), portfolio_page(), news_index(), about_page(), club_page(), zarban_page(), apply_page()]
    pages += [sector_page(s) for s in SECTORS]
    pages += [news_article(n) for n in NEWS]
    for p, text in pages:
        write(p.path, text)
    (DIST / "404.html").write_text(not_found(), encoding="utf-8")
    (DIST / "robots.txt").write_text("User-agent: *\nDisallow: /\n", encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    # drop non-site files that live in src/
    for junk in DIST.rglob("CREDITS.json"):
        junk.unlink()
    print(f"built {len(pages) + 1} pages → {DIST}")


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        import http.server
        import functools
        port = 8797
        handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(DIST))
        print(f"serving http://127.0.0.1:{port}")
        http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()
