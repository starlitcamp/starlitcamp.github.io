# -*- coding: utf-8 -*-
"""Builds the Starlit Camp site in 4 languages.

    python3 _src/build.py

Korean pages go to the site root, the others to en/, ja/ and es/.
Text: _src/strings.py and _src/legal/*.html. Game status: games.js
(the live site reads games.js at runtime, so changing a status there takes
effect without rebuilding; rebuilding only refreshes the no-JavaScript defaults).
"""
import html
import json
import os
import re
import sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from strings import LANGS, LANG_NAMES, GROUP_NAME, EMAIL, UI, GAMES  # noqa: E402

SITE = "https://starlitcamp.github.io/"
PAGES = ["index.html", "stellarbloom.html", "wizardtower.html", "privacy.html", "terms.html", "data-deletion.html"]
AUTO_LANG_PAGES = {"index.html", "stellarbloom.html", "wizardtower.html"}
STATUSES = ["soon", "recruiting", "testing", "released"]


def load_config():
    src = open(os.path.join(ROOT, "games.js"), encoding="utf-8").read()
    m = re.search(r"/\*CONFIG\*/(.*?)/\*END\*/", src, re.S)
    cfg = json.loads(m.group(1))
    for k, v in cfg.items():
        assert v["status"] in STATUSES, (k, v["status"])
    return cfg


CFG = load_config()


def esc(s):
    return html.escape(s, quote=True)


def folder(lang):
    return "" if lang == "ko" else lang + "/"


def up(lang):
    return "" if lang == "ko" else "../"


def page_href(page):
    return "./" if page == "index.html" else page


def link_between(src_lang, dst_lang, page):
    target = "" if page == "index.html" else page
    if src_lang == dst_lang:
        return page_href(page)
    return up(src_lang) + folder(dst_lang) + target if (up(src_lang) + folder(dst_lang) + target) else "./"


def url_of(game, kind):
    g = CFG[game]
    return {
        "group": "https://groups.google.com/g/" + g["group"],
        "optin": "https://play.google.com/apps/testing/" + g["package"],
        "store": "https://play.google.com/store/apps/details?id=" + g["package"],
        "appstore": g.get("appStore") or "",
    }[kind]


def when(game, statuses):
    """Attributes for a block shown only while `game` has one of `statuses`."""
    hidden = "" if CFG[game]["status"] in statuses else " hidden"
    return f' data-game="{game}" data-when="{" ".join(statuses)}"{hidden}'


def ahref(game, kind, label, cls="btn"):
    u = url_of(game, kind)
    hidden = "" if u else " hidden"
    return f'<a class="{cls}" data-game="{game}" data-href="{kind}" href="{esc(u or "#")}" rel="noopener"{hidden}>{esc(label)}</a>'


def mailto(subject):
    return f"mailto:{EMAIL}?subject={quote(subject)}"


AUTO_LANG_JS = (
    '<script>(function(){if(/bot|crawl|spider|slurp|preview|lighthouse/i.test(navigator.userAgent))return;'
    'var L=["ko","en","ja","es"],p=null;try{p=localStorage.getItem("sc_lang")}catch(e){}'
    'if(L.indexOf(p)<0){p=null;var n=navigator.languages||[navigator.language||""];'
    'for(var i=0;i<n.length&&!p;i++){var c=String(n[i]).slice(0,2).toLowerCase();if(L.indexOf(c)>=0)p=c}p=p||"en"}'
    'if(p!=="ko")location.replace(p+"/"+location.pathname.split("/").pop()+location.search+location.hash)})();</script>'
)


def head(lang, page, title, desc, og_image=None, extra=""):
    u = up(lang)
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{SITE}{folder(l)}{"" if page == "index.html" else page}">' for l in LANGS
    )
    alts += f'\n<link rel="alternate" hreflang="x-default" href="{SITE}{"" if page == "index.html" else page}">'
    canonical = f'{SITE}{folder(lang)}{"" if page == "index.html" else page}'
    og = ""
    if og_image:
        og = (f'<meta property="og:title" content="{esc(title.split(" | ")[0])}">\n'
              f'<meta property="og:description" content="{esc(desc)}">\n'
              f'<meta property="og:image" content="{SITE}{og_image}">\n')
    auto = AUTO_LANG_JS + "\n" if (lang == "ko" and page in AUTO_LANG_PAGES) else ""
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
{auto}<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
{og}<link rel="canonical" href="{canonical}">
{alts}
<link rel="icon" href="{u}img/favicon.png" type="image/png">
<link rel="stylesheet" href="{u}style.css">
<script src="{u}games.js"></script>
<script src="{u}site.js" defer></script>
{extra}</head>
<body>
<div class="wrap">
"""


def header(lang, page):
    t = UI[lang]
    u = up(lang)
    langs = "".join(
        f'<a href="{link_between(lang, l, page)}" data-setlang="{l}" hreflang="{l}" lang="{l}"'
        + (' aria-current="true"' if l == lang else "") + f">{LANG_NAMES[l]}</a>"
        for l in LANGS
    )
    return f"""  <nav class="langbar" aria-label="Language">{langs}</nav>
  <header class="site">
    <a class="brand" href="./"><img src="{u}img/starlitcamp_icon.png" alt="" style="image-rendering:pixelated;border-radius:8px"><span class="brand-name">Starlit Camp</span></a>
    <nav><a href="./#games">{t['nav_games']}</a><a href="privacy.html">{t['nav_privacy']}</a><a href="terms.html">{t['nav_terms']}</a><a href="./#contact">{t['nav_contact']}</a></nav>
  </header>
"""


def footer(lang):
    t = UI[lang]
    return f"""
  <footer><span>&copy; 2026 Starlit Camp</span><a href="privacy.html">{t['f_privacy']}</a><a href="terms.html">{t['f_terms']}</a><a href="data-deletion.html">{t['f_deletion']}</a><a href="mailto:{EMAIL}">{EMAIL}</a></footer>
</div>
</body>
</html>
"""


def status_spans(lang, game, prefix=""):
    t = UI[lang]
    return "".join(f'<span{when(game, [s])}>{prefix}{t["st_" + s]}</span>' for s in STATUSES)


# ---------------------------------------------------------------- home
def build_index(lang):
    t = UI[lang]
    u = up(lang)
    out = head(lang, "index.html", t["home_title"], t["home_desc"], "img/starlitcamp_header.png")
    out += header(lang, "index.html")
    out += f"""
  <div class="hero"><img src="{u}img/starlitcamp_header.png" alt="Starlit Camp" style="image-rendering:pixelated"></div>
  <h1>{t['home_h1']}</h1>
  <p class="lead">{t['home_lead']}</p>

  <h2 id="games">{t['games_h2']}</h2>
"""
    for key, g in GAMES.items():
        name = g["name"][lang]
        sub = g["name"]["en"] if lang == "ko" else g["name"]["ko"]
        px = ' style="image-rendering:pixelated"' if g["pixel"] else ""
        out += f"""  <a class="card" href="{g['page']}">
    <img class="icon" src="{u}{g['icon']}" alt="{esc(name)}"{px}>
    <div>
      <h3>{esc(name)} <span class="alt">{esc(sub)}</span> <span class="tag">{status_spans(lang, key, "Android · ")}</span></h3>
      <p>{g['card'][lang]}</p>
    </div>
  </a>
"""
    active = [k for k, v in CFG.items() if v["status"] in ("recruiting", "testing")]
    hidden = "" if active else " hidden"
    btns = "".join(
        f'<a class="btn primary"{when(k, ["recruiting", "testing"])} href="{g["page"]}#join">{esc(t["testers_btn"].format(name=g["name"][lang]))}</a>'
        for k, g in GAMES.items()
    )
    out += f"""
  <section class="callout" data-any="recruiting testing"{hidden}>
    <h2 id="testers">{t['testers_h2']}</h2>
    <p>{t['testers_p']}</p>
    <div class="links">{btns}</div>
  </section>

  <h2 id="contact">{t['contact_h2']}</h2>
  <p>{t['contact_line']}: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
"""
    out += footer(lang)
    return out


# ---------------------------------------------------------------- game pages
def join_section(lang, key):
    t = UI[lang]
    g = GAMES[key]
    name = g["name"][lang]
    group = esc(GROUP_NAME)
    fb = mailto(t["feedback_subject"].format(name=name))

    def step(title, desc, buttons=""):
        links = f'<div class="links">{buttons}</div>' if buttons else ""
        return f"      <li><b class=\"t\">{title}</b>{desc}{links}</li>\n"

    s1 = step(t["j1_t"], t["j1_d"].format(group=group), ahref(key, "group", t["j1_b"], "btn primary"))
    testing = (f'    <div{when(key, ["testing"])}>\n      <h2>{t["j_test_h"]}</h2>\n      <p>{t["j_test_p"].format(name=esc(name))}</p>\n'
               f'    <ol class="steps">\n{s1}'
               + step(t["j2_t"], t["j2_d"], ahref(key, "optin", t["j2_b"], "btn primary"))
               + step(t["j3_t"], t["j3_d"], ahref(key, "store", t["b_play"]))
               + step(t["j4_t"], t["j4_d"], f'<a class="btn" href="{esc(fb)}">{t["j4_b"]}</a>')
               + f'    </ol>\n      <p class="note">{t["j_test_note"]}</p>\n    </div>\n')
    recruiting = (f'    <div{when(key, ["recruiting"])}>\n      <h2>{t["j_rec_h"]}</h2>\n      <p>{t["j_rec_p"].format(name=esc(name))}</p>\n'
                  f'    <ol class="steps">\n{s1}'
                  + step(t["r2_t"], t["r2_d"])
                  + step(t["j4_t"], t["r3_d"])
                  + f'    </ol>\n      <p class="note">{t["j_rec_note"]}</p>\n    </div>\n')
    released = (f'    <div{when(key, ["released"])}>\n      <h2>{t["j_rel_h"]}</h2>\n      <p>{t["j_rel_p"].format(name=esc(name))}</p>\n'
                f'      <div class="links">{ahref(key, "store", t["b_play"], "btn primary")}{ahref(key, "appstore", t["b_appstore"], "btn primary")}</div>\n'
                f'      <p class="note">{t["j_rel_thanks"]}</p>\n    </div>\n')
    soon = (f'    <div{when(key, ["soon"])}>\n      <h2>{t["j_soon_h"]}</h2>\n      <p>{t["j_soon_p"].format(name=esc(name))}</p>\n    </div>\n')
    return f'  <section id="join" class="join">\n{testing}{recruiting}{released}{soon}  </section>\n'


def build_game(lang, key):
    t = UI[lang]
    g = GAMES[key]
    u = up(lang)
    name = g["name"][lang]
    title = f"{name} ({g['alt_name']}) | Starlit Camp" if lang == "ko" else f"{name} | Starlit Camp"
    extra = "<style>.pixel img{image-rendering:pixelated}</style>\n" if g["pixel"] else ""
    out = head(lang, g["page"], title, g["desc"][lang], g["feature"], extra)
    out += header(lang, g["page"])
    px = " pixel" if g["pixel"] else ""
    sub = (g["alt_name"] + " · ") if lang == "ko" else ""
    out += f"""
  <div class="gamehead{px}">
    <img src="{u}{g['icon']}" alt="{esc(name)}">
    <div>
      <h1>{esc(name)}</h1>
      <p class="sub">{sub}Android · {status_spans(lang, key)}</p>
    </div>
  </div>
  <div class="hero{px}"><img src="{u}{g['feature']}" alt="{esc(g['hero_alt'][lang])}"></div>

  <p class="lead">{g['lead'][lang]}</p>
  <div class="links">
    <a class="btn primary"{when(key, ["recruiting", "testing"])} href="#join">{t['cta_join']}</a>
    <span{when(key, ["released"])}>{ahref(key, "store", t["b_play"], "btn primary")}</span>
  </div>
"""
    shots = g["shots"][lang] if isinstance(g["shots"], dict) else g["shots"]   # localized store shots per language
    if shots:
        imgs = "\n".join(f'    <img src="{u}{s}" alt="{esc(a)}" loading="lazy">' for s, a in zip(shots, g["shot_alts"][lang]))
        out += f'\n  <div class="shots{px}">\n{imgs}\n  </div>\n'
    feats = "\n".join(f"    <li><b>{a}</b>{b}</li>" for a, b in g["features"][lang])
    out += f"""
  <h2>{t['features_h2']}</h2>
  <ul class="features">
{feats}
  </ul>

{join_section(lang, key)}
  <h2>{t['support_h2']}</h2>
  <div class="links">
    <a class="btn" href="{esc(mailto(t['contact_subject'].format(name=name)))}">{t['b_contact']}</a>
    <a class="btn" href="privacy.html">{t['b_privacy']}</a>
    <a class="btn" href="terms.html">{t['b_terms']}</a>
    <a class="btn" href="data-deletion.html">{t['b_deletion']}</a>
  </div>
  <p class="note">{g['note'][lang]}</p>
"""
    out += footer(lang)
    return out


# ---------------------------------------------------------------- legal
def build_legal(lang, page):
    t = UI[lang]
    base = page[:-5]
    h, meta, scope = {
        "privacy": (t["privacy_h"], t["privacy_meta"], t["privacy_scope"]),
        "terms": (t["terms_h"], t["terms_meta"], t["terms_scope"]),
        "data-deletion": (t["deletion_h"], "", t["deletion_scope"]),
    }[base]
    body = open(os.path.join(HERE, "legal", f"{base}.{lang}.html"), encoding="utf-8").read().rstrip()
    body = "\n".join(("  " + l) if l else l for l in body.split("\n"))
    out = head(lang, page, f"{h} | Starlit Camp", f"Starlit Camp - {h}")
    out += header(lang, page)
    out += f"\n  <h1>{h}</h1>\n"
    if t["translation_note"]:
        out += f'  <p class="note">{t["translation_note"]} <a href="{link_between(lang, "ko", page)}" data-setlang="ko" lang="ko">한국어 원문</a></p>\n'
    if meta:
        out += f"  <p>{meta}</p>\n"
    out += f"  <p>{scope}</p>\n\n{body}\n"
    out += footer(lang)
    return out


def main():
    written = []
    for lang in LANGS:
        d = os.path.join(ROOT, folder(lang))
        os.makedirs(d, exist_ok=True)
        for page in PAGES:
            if page == "index.html":
                s = build_index(lang)
            elif page[:-5] in GAMES:
                s = build_game(lang, page[:-5])
            else:
                s = build_legal(lang, page)
            p = os.path.join(d, page)
            with open(p, "w", encoding="utf-8", newline="\n") as f:
                f.write(s)
            written.append(os.path.relpath(p, ROOT))
    print("built", len(written), "pages:", " ".join(written))


if __name__ == "__main__":
    main()
