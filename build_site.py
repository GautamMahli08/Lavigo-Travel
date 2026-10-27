"""Build a clean, English-only, offline-runnable copy of the scraped site.

Usage: python -I build_site.py original-scrape site
"""
import base64
import collections
import glob
import json
import os
import posixpath
import re
import shutil
import sys
from urllib.parse import quote, unquote, urlsplit

SRC = os.path.abspath(sys.argv[1])
OUT = os.path.abspath(sys.argv[2])
TRANSLATIONS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "translations")
LIVE = "https://tourisme-sumene-artense.com"

# French words left in English folder names -> English name
with open(os.path.join(TRANSLATIONS, "folder-names.json"), encoding="utf-8") as f:
    FOLDER_NAMES = {k: v for k, v in json.load(f).items() if not k.startswith("_")}

URL_RE = re.compile(
    r"(?:https?:)?//tourisme-sumene-artense\.com(?P<rest>(?:(?!&quot;|&#039;)[^\"'\s<>)\]])*)"
)
CSS_URL_RE = re.compile(r"url\(\s*(['\"]?)(?P<url>[^)'\"]+)\1\s*\)")

ASSET_PREFIXES = [
    ("/wp-content/uploads/", "assets/uploads/"),
    ("/wp-content/themes/otsa/", "assets/theme/"),
    ("/wp-content/cache/autoptimize/css/", "assets/css/"),
    ("/wp-content/cache/autoptimize/js/", "assets/js/"),
    ("/wp-includes/js/", "assets/js/wp/"),
]

missing_assets = collections.Counter()
missing_pages = collections.Counter()
copied_assets = {}  # out rel path -> src file


def read(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        return f.read()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


# ---------------------------------------------------------------- page map
# English pages: site path ("/en/x/y/") -> output path ("x/y/index.html")
en_pages = {}
for f in glob.glob(os.path.join(SRC, "en", "**", "index.html"), recursive=True):
    rel = os.path.relpath(os.path.dirname(f), os.path.join(SRC, "en")).replace(os.sep, "/")
    if rel in ("feed",):
        continue
    site_path = "/en/" + ("" if rel == "." else rel + "/")
    out_rel = "/".join(FOLDER_NAMES.get(part, part) for part in rel.split("/"))
    out = "index.html" if rel == "home" else out_rel + "/index.html"
    en_pages[site_path] = (f, out)
en_pages.pop("/en/", None)

# French site path -> English site path, from each French page's hreflang links
# French site path -> English site path (taken from the French pages' hreflang links,
# saved before the French pages were removed from the scrape)
with open(os.path.join(TRANSLATIONS, "fr-to-en.json"), encoding="utf-8") as f:
    fr_to_en = json.load(f)

# Pages that only exist in French on the live site, translated by hand.
# English path -> (French path, English page used for header/footer, translated <main>, title)
TRANSLATED_PAGES = {
    "/en/legal-notice/": (
        "/mentions-legales/", "/en/contact/", "legal-notice.html", "Legal notice",
    ),
}
for en_path, (fr_path, *_) in TRANSLATED_PAGES.items():
    en_pages[en_path] = (None, en_path[len("/en/"):] + "index.html")
    fr_to_en[fr_path] = en_path


# ---------------------------------------------------------------- resolvers
def find_asset_source(path, query):
    base = os.path.join(SRC, unquote(path).lstrip("/").replace("/", os.sep))
    candidates = [base]
    if query:
        candidates += [base + "@" + query, base + "@" + query + os.path.splitext(base)[1]]
    candidates += sorted(glob.glob(glob.escape(base) + "@*"))
    for c in candidates:
        if os.path.isfile(c):
            return c
    return None


def map_asset(path, query):
    for prefix, target in ASSET_PREFIXES:
        if path.startswith(prefix):
            src = find_asset_source(path, query)
            if not src:
                return None
            out = target + unquote(path[len(prefix):])
            copied_assets[out] = src
            return out
    return None


def map_page(path, query):
    if path in ("", "/"):
        path = "/en/home/"
    if not path.startswith("/en/"):
        path = fr_to_en.get(path, path)
    if not path.endswith("/") and "." not in posixpath.basename(path):
        path += "/"
    if path == "/en/home/" and "skipintro" in query:
        return "home.html"
    if path in en_pages:
        return en_pages[path][1]
    return None


def rewrite_url(rest, from_out):
    """Return the replacement for a live-site URL referenced from output file `from_out`."""
    parts = urlsplit(rest)
    path, query, frag = parts.path, parts.query, parts.fragment
    target = None
    if path.startswith(("/wp-content/", "/wp-includes/")):
        target = map_asset(path, query.replace("&#038;", "&"))
        if not target:
            missing_assets[path] += 1
    elif path.startswith(("/wp-admin", "/wp-json", "/xmlrpc", "/feed", "/en/feed", "/en/comments")):
        target = None
    else:
        target = map_page(path, query)
        if not target:
            missing_pages[path] += 1
            en_path = fr_to_en.get(path)
            if en_path:  # English page exists online but was not scraped
                return LIVE + en_path + ("#" + frag if frag else "")
    if not target:
        return LIVE + rest
    rel = posixpath.relpath(target, posixpath.dirname(from_out) or ".")
    return quote(rel, safe="/@") + ("#" + frag if frag else "")


# ---------------------------------------------------------------- HTML clean-up
REMOVE_PATTERNS = [
    r'<link rel="alternate"[^>]*hreflang="[^"]*"\s*/?>',
    r'<link rel="alternate"[^>]*(?:oembed|rss\+xml)[^>]*>',
    r'<link rel="pingback"[^>]*>',
    r'<link rel="profile"[^>]*>',
    r'<link rel="https://api\.w\.org/"[^>]*>',
    r'<link rel="EditURI"[^>]*>',
    r'<meta property="og:locale:alternate"[^>]*>',
    r'<noscript><iframe src="https://www\.googletagmanager\.com[^<]*</iframe></noscript>',
    r'<script[^>]*src="https://www\.google\.com/recaptcha[^"]*"[^>]*></script>',
    # language switcher (Fr / En buttons)
    r'<a lang="(?:fr-FR|en-GB)"[^>]*>.*?</a>',
]


def fix_inline_script(m):
    data = base64.b64decode(m.group(1)).decode("utf-8", "replace")
    if "googletagmanager.com/gtm.js" in data:
        return None
    if "AllianceReseaux" in data:
        data = re.sub(r"langue:\s*'fr'", "langue: 'en'", data)
    return base64.b64encode(data.encode("utf-8")).decode("ascii")


def process_html(text, out_rel):
    for pat in REMOVE_PATTERNS:
        text = re.sub(pat, "", text, flags=re.S)

    def inline(m):
        new = fix_inline_script(m)
        return "" if new is None else m.group(0).replace(m.group(1), new)

    text = re.sub(r'<script[^>]*src="data:text/javascript;base64,([^"]+)"[^>]*></script>', inline, text)
    text = text.replace('lang="fr-FR"', 'lang="en-GB"')
    text = text.replace('aria-label="Formulaire de contact"', 'aria-label="Contact form"')
    # forms and search post to the live server (they need a backend)
    text = re.sub(r'action="/', 'action="' + LIVE + "/", text)
    text = URL_RE.sub(lambda m: rewrite_url(m.group("rest"), out_rel), text)
    return text


def process_css(text, out_rel):
    def repl(m):
        url = m.group("url")
        um = URL_RE.fullmatch(url.split("?")[0]) or URL_RE.fullmatch(url)
        if not um:
            return m.group(0)
        frag = "#" + url.split("#", 1)[1] if "#" in url else ""
        new = rewrite_url(um.group("rest").split("#")[0], out_rel)
        return "url(" + new + frag + ")"

    return CSS_URL_RE.sub(repl, text)


# ---------------------------------------------------------------- build
os.makedirs(OUT, exist_ok=True)
for entry in os.listdir(OUT):
    p = os.path.join(OUT, entry)
    shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

pages = list(en_pages.values())
skip_src = os.path.join(SRC, "en", "home", "index.html@skipintro.html")
if os.path.isfile(skip_src):
    pages.append((skip_src, "home.html"))

def build_translated(en_path):
    """Wrap a hand-translated <main> in the header/footer of an existing English page."""
    fr_path, template_path, main_file, title = TRANSLATED_PAGES[en_path]
    text = read(en_pages[template_path][0])
    main = read(os.path.join(TRANSLATIONS, main_file))
    text = text[:text.find("<main")] + main.strip() + text[text.find("</main>") + len("</main>"):]
    text = re.sub(r"<title>.*?</title>", f"<title>{title} - Tourisme Sumène Artense</title>", text)
    text = re.sub(r'(<meta property="og:title" content=")[^"]*', rf"\g<1>{title} - Tourisme Sumène Artense", text)
    text = re.sub(r'<body class="[^"]*"', '<body class="page-template-default page wp-theme-otsa"', text)
    for tag in ('<link rel="canonical" href="', '<meta property="og:url" content="'):
        text = text.replace(tag + LIVE + template_path, tag + LIVE + en_path)
    return text


for src, out in pages:
    if src is None:
        en_path = next(p for p, (s, o) in en_pages.items() if o == out)
        text = build_translated(en_path)
    else:
        text = read(src)
    write(os.path.join(OUT, out), process_html(text, out))

done = set()
while len(done) < len(copied_assets):
    for out, src in list(copied_assets.items()):
        if out in done:
            continue
        done.add(out)
        dst = os.path.join(OUT, out)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if out.endswith(".css"):
            write(dst, process_css(read(src), out))
        else:
            shutil.copyfile(src, dst)

print(f"pages written : {len(pages)}")
print(f"assets copied : {len(copied_assets)}")
print(f"links to pages not scraped (left pointing to live site): {len(missing_pages)}")
for p, n in missing_pages.most_common(15):
    print(f"   {n:4d}  {p}")
print(f"assets not scraped (left pointing to live site): {len(missing_assets)}")
for p, n in missing_assets.most_common(15):
    print(f"   {n:4d}  {p}")
