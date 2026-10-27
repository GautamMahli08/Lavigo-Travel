"""Build the LAVIGO website from the English base pages, keeping the original design.

Usage:
    python build_lavigo.py                 # builds the English base from original-scrape/, then the LAVIGO site into site/
    python build_lavigo.py <base_dir> site # use an existing English base (output of build_site.py)

Texts:   lavigo-content/content.py
Photos:  lavigo-content/images/<name>.jpg  (+ credits.json)
Logo:    lavigo-content/brand/
Map:     lavigo-content/map/
"""
import copy
import html
import importlib.util
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import quote, unquote

from bs4 import BeautifulSoup, Comment, NavigableString, Tag

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(ROOT, "lavigo-content")

spec = importlib.util.spec_from_file_location("content", os.path.join(CONTENT_DIR, "content.py"))
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)

CREDITS = json.load(open(os.path.join(CONTENT_DIR, "images", "credits.json"), encoding="utf-8"))
MAP = json.load(open(os.path.join(CONTENT_DIR, "map", "map.json"), encoding="utf-8"))
DEST = {d["slug"]: d for d in C.DESTINATIONS}

# ---------------------------------------------------------------- output layout
PAGES = {
    "home": "index.html",
    "home_skip": "home.html",
    "destinations": "destinations/index.html",
    "contact": "contact/index.html",
    "legal": "legal-notice/index.html",
}
for d in C.DESTINATIONS:
    PAGES["dest:" + d["slug"]] = f"destinations/{d['slug']}/index.html"
for b in C.BLOG:
    PAGES["blog:" + b["slug"]] = f"blog/{b['slug']}/index.html"
PAGES["trips"] = "trips/index.html"
PAGES["about"] = "about/index.html"
for t in C.TRIPS:
    PAGES["trip:" + t["slug"]] = f"trips/{t['slug']}/index.html"

WHATSAPP_ICON = ('<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true"><path d="M17.47 14.38c-.3-.15'
                 '-1.75-.86-2.02-.96-.27-.1-.47-.15-.67.15-.2.3-.77.96-.94 1.16-.17.2-.35.22-.65.07-.3-.15-1.25-.46-2.38-1.47-.88-'
                 '.78-1.47-1.75-1.64-2.05-.17-.3-.02-.46.13-.61.13-.13.3-.35.45-.52.15-.17.2-.3.3-.5.1-.2.05-.37-.02-.52-.08-.15-'
                 '.67-1.62-.92-2.22-.24-.58-.49-.5-.67-.51h-.57c-.2 0-.52.07-.8.37-.27.3-1.04 1.02-1.04 2.48s1.07 2.88 1.22 3.08c.15'
                 '.2 2.1 3.2 5.08 4.49.71.31 1.27.49 1.7.63.72.23 1.37.2 1.88.12.57-.09 1.75-.72 2-1.41.25-.69.25-1.29.17-1.41-.07'
                 '-.12-.27-.2-.57-.35zM12.05 21.8h-.01a9.8 9.8 0 0 1-5-1.37l-.36-.21-3.72.97 1-3.62-.24-.37a9.78 9.78 0 0 1-1.5-5.21'
                 'c0-5.41 4.41-9.81 9.83-9.81 2.62 0 5.09 1.02 6.94 2.88a9.75 9.75 0 0 1 2.87 6.94c0 5.41-4.41 9.8-9.81 9.8zm8.36-18.'
                 '16A11.74 11.74 0 0 0 12.05 0C5.5 0 .17 5.33.16 11.88c0 2.09.55 4.14 1.59 5.94L.06 24l6.33-1.66a11.83 11.83 0 0 0 '
                 '5.65 1.44h.01c6.55 0 11.88-5.33 11.89-11.89a11.82 11.82 0 0 0-3.53-8.4z"/></svg>')


def money(n):
    """Indian digit grouping: 124999 -> ₹1,24,999"""
    s = str(int(n))
    if len(s) > 3:
        head, tail = s[:-3], s[-3:]
        head = ",".join([head[max(0, i - 2):i] for i in range(len(head), 0, -2)][::-1])
        s = head + "," + tail
    return C.CURRENCY + s


def nice_date(iso):
    import datetime
    return datetime.date.fromisoformat(iso).strftime("%a %d %b %Y")


def wa_link(text):
    return f"https://wa.me/{C.CONTACT['whatsapp']}?text={quote(text)}"


def rel(from_out, target):
    """Relative URL from output page `from_out` to site path `target` (e.g. 'assets/images/x.jpg')."""
    frag = ""
    if "#" in target:
        target, frag = target.split("#", 1)
        frag = "#" + frag
    r = posixpath.relpath(target, posixpath.dirname(from_out) or ".")
    return quote(r, safe="/@") + frag


def img_path(key):
    if not os.path.exists(os.path.join(CONTENT_DIR, "images", key + ".jpg")):
        raise SystemExit(f"Missing image: lavigo-content/images/{key}.jpg")
    return f"assets/images/{key}.jpg"


def credit(key):
    c = CREDITS.get(key, {})
    author = re.sub(r"\s+", " ", c.get("author", "")).strip()
    author = re.sub(r"https?://\S+", "", author)
    author = re.split(r"\s\d{4}-\d{2}-\d{2}|\sThis is\s", author)[0].strip() or "Wikimedia Commons"
    return author[:60]


def credit_title(key):
    t = CREDITS[key]["article"]
    if t.startswith("File:"):
        t = os.path.splitext(t[5:])[0].replace("_", " ")
    return t


# ---------------------------------------------------------------- soup helpers
def load(path):
    with open(path, encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")


def load_as(base, template_rel, out_rel):
    """Load a template page and rebase its relative links when the output page sits at a different depth."""
    soup = load(os.path.join(base, template_rel))
    if posixpath.dirname(template_rel).count("/") == posixpath.dirname(out_rel).count("/") and \
            bool(posixpath.dirname(template_rel)) == bool(posixpath.dirname(out_rel)):
        return soup
    skip = re.compile(r"^(?:[a-z]+:|//|#|/)", re.I)

    def fix(u):
        if not u or skip.match(u):
            return u
        path, _, rest = u.partition("#")
        target = posixpath.normpath(posixpath.join(posixpath.dirname(template_rel), unquote(path)))
        return rel(out_rel, target) + ("#" + rest if rest else "")

    for t in soup.find_all(True):
        for a in ("href", "src"):
            if t.get(a):
                t[a] = fix(t[a])
        if "url(" in t.get("style", ""):
            t["style"] = re.sub(r"url\('([^']*)'\)", lambda m: f"url('{fix(m.group(1))}')", t["style"])
    return soup


def frag(markup):
    return BeautifulSoup(markup, "html.parser")


def set_text(tag, text):
    tag.clear()
    tag.append(NavigableString(text))


def text_el(tag):
    """Innermost element that directly holds the visible text."""
    for t in tag.find_all(True):
        if t.string and t.string.strip() and not t.find(True):
            return t
    return tag


def set_heading(tag, line1, line2):
    set_text(tag.select_one(".t-title-1"), line1)
    set_text(tag.select_one(".t-title-2"), line2)


def set_bg(tag, url):
    tag["style"] = re.sub(r"background-image:\s*url\([^)]*\)", f"background-image:url('{url}')", tag.get("style", ""))


def bg_tags(root):
    return [t for t in root.find_all(style=True) if "background-image" in t["style"]]


def captions(root):
    return root.select(".media-caption-value")


def add_class(tag, cls):
    classes = tag.get("class", [])
    if cls not in classes:
        tag["class"] = classes + [cls]


def remove_class(tag, cls):
    tag["class"] = [c for c in tag.get("class", []) if c != cls]


def renumber(tag, old, new):
    """Deep-copy `tag` replacing every occurrence of the id fragment `old` with `new`."""
    return frag(str(tag).replace(old, new)).contents[0]


def fill_list(container, items, fill, templates=None):
    """Make `container` hold one child per item, cloned from its existing children, and fill each one."""
    kids = [k for k in container.children if isinstance(k, Tag)]
    templates = templates or kids
    for k in kids:
        k.extract()
    out = []
    for i, item in enumerate(items):
        node = copy.copy(templates[min(i, len(templates) - 1)])
        container.append(node)
        fill(node, item, i)
        out.append(node)
    return out


def rich(container, paragraphs):
    container.clear()
    for p in paragraphs:
        t = frag(f"<p>{html.escape(p)}</p>")
        container.append(t)


# ---------------------------------------------------------------- shared page chrome
LOGO_SLOTS = {"0 0 86 90", "0 0 117 121", "0 0 110 45", "0 0 82 84"}
SEARCH_INDEX = [(d["slug"], [d["name"].lower(), d["slug"]] + [p["name"].lower() for p in d["places"]]) for d in C.DESTINATIONS]


def logo_img(out_rel, dark, height):
    src = rel(out_rel, "assets/brand/lavigo-logo-dark.png" if dark else "assets/brand/lavigo-logo.png")
    return frag(f'<img src="{src}" alt="{C.COMPANY}" class="lavigo-logo" '
                f'style="height:{height};width:auto;max-width:none;display:block;">').contents[0]


def replace_logos(soup, out_rel, dark_logo=False):
    for sv in soup.find_all("svg"):
        vb = sv.get("viewbox") or sv.get("viewBox")
        if vb not in LOGO_SLOTS:
            continue
        parent = sv.parent
        pcls = " ".join(parent.get("class", []))
        in_footer = parent.find_parent("footer") is not None
        page_emblem = vb == "0 0 82 84" or (vb == "0 0 110 45" and "only-mobile" in pcls) or (
            vb == "0 0 86 90" and "hide-mobile" in pcls and not in_footer)
        light_bg = page_emblem and dark_logo
        heights = {"0 0 86 90": "2.6em", "0 0 82 84": "2.6em", "0 0 117 121": "3.4em", "0 0 110 45": "100%"}
        h = heights[vb]
        if "height-12em" in pcls:  # intro splash
            h = "4.5em"
        if "only-mobile" in pcls:
            h = "2.2em"
        remove_class(parent, "left-margin--2-5")
        if vb == "0 0 117 121":
            parent["style"] = "display:flex;justify-content:center;"
        sv.replace_with(logo_img(out_rel, light_bg, h))


def site_url():
    """The real website address, or '' while it is still the placeholder."""
    u = C.SITE.get("url", "").rstrip("/")
    return "" if (not u or "your-domain" in u) else u


def absolute(path):
    return site_url() + "/" + quote(path, safe="/@")


def write_sitemap(out):
    base = site_url() or C.SITE.get("url", "").rstrip("/")
    import datetime
    today = datetime.date.today().isoformat()
    urls = []
    for key, path in PAGES.items():
        if key == "home_skip":
            continue
        loc = base + "/" + path.replace("index.html", "")
        prio = "1.0" if key == "home" else "0.9" if key.startswith("trip") else "0.7"
        urls.append(f"  <url><loc>{html.escape(loc)}</loc><lastmod>{today}</lastmod><priority>{prio}</priority></url>")
    nl = "\n"
    with open(os.path.join(out, "sitemap.xml"), "w", encoding="utf-8", newline=nl) as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>' + nl
                + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + nl
                + nl.join(urls) + nl + "</urlset>" + nl)
    with open(os.path.join(out, "robots.txt"), "w", encoding="utf-8", newline=nl) as f:
        f.write("User-agent: *" + nl + "Allow: /" + nl + nl + f"Sitemap: {base}/sitemap.xml" + nl)


def agency_jsonld(out_rel):
    """Business information for Google (TravelAgency)."""
    K = C.CONTACT
    data = {"@context": "https://schema.org", "@type": "TravelAgency", "name": C.COMPANY, "description": C.HERO["description"],
            "areaServed": ["Nepal", "Sikkim", "Darjeeling", "Himachal Pradesh", "Bhutan"]}
    real = lambda v: v and not v.startswith("[") and v != "#"
    if real(K.get("phone")):
        data["telephone"] = K["phone"]
    if real(K.get("email")):
        data["email"] = K["email"]
    if all(real(x) for x in K.get("address_lines", [])):
        data["address"] = {"@type": "PostalAddress", "streetAddress": ", ".join(K["address_lines"])}
    same = [u for u in (K.get("facebook"), K.get("instagram"), C.SITE.get("google_reviews")) if real(u)]
    if same:
        data["sameAs"] = same
    if site_url():
        data["url"] = site_url() + "/"
        data["logo"] = absolute("assets/brand/lavigo-logo-dark.png")
        data["image"] = absolute(img_path(C.HERO["image"]))
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


def clean_head(soup, out_rel, title, description, image_key):
    head = soup.head
    for sel in ['link[rel="canonical"]', 'script[type="application/ld+json"]', 'meta[property="article:publisher"]',
                'meta[property="article:modified_time"]', 'meta[name="twitter:card"]', 'meta[name^="twitter:"]',
                'link[rel="icon"]', 'link[rel="apple-touch-icon"]', 'meta[name="msapplication-TileImage"]',
                'meta[property="og:image"]', 'meta[property="og:image:width"]', 'meta[property="og:image:height"]',
                'meta[property="og:image:type"]']:
        for t in head.select(sel):
            t.decompose()
    full_title = title if title == C.COMPANY else f"{title} - {C.COMPANY}"
    head.title.string = full_title
    for t in head.select('meta[name="description"], meta[name="author"], meta[property^="article:"], link[href*="wp-json"]'):
        t.decompose()
    head.title.insert_after(frag(f'<meta name="description" content="{html.escape(description)}"/>'
                                 f'<meta name="author" content="{C.COMPANY}"/>'))
    for c in soup.find_all(string=lambda x: isinstance(x, Comment)):
        if "tourisme-sumene" in c or "html5.js" in c:
            c.extract()
    for im in soup.find_all("img", alt="Nuages"):
        im["alt"] = ""
    page_url = absolute(out_rel.replace("index.html", "")) if site_url() else out_rel
    for prop, value in (("og:title", full_title), ("og:description", description), ("og:site_name", C.COMPANY),
                        ("og:url", page_url)):
        tag = head.find("meta", property=prop)
        if not tag:
            tag = soup.new_tag("meta", attrs={"property": prop})
            head.append(tag)
        tag["content"] = value
    image_url = absolute(img_path(image_key)) if site_url() else rel(out_rel, img_path(image_key))
    head.append(frag(f'<meta property="og:image" content="{image_url}" />'))
    if site_url():
        head.append(frag(f'<link rel="canonical" href="{page_url}" />'))
    if C.SITE.get("google_site_verification"):
        head.append(frag(f'<meta name="google-site-verification" content="{html.escape(C.SITE["google_site_verification"])}" />'))
    head.append(frag(f'<link rel="icon" href="{rel(out_rel, "assets/brand/favicon.png")}" sizes="64x64" />'))
    head.append(frag(f'<link rel="apple-touch-icon" href="{rel(out_rel, "assets/brand/favicon-180.png")}" />'))


THIRD_PARTY = ("axept", "AllianceReseaux", "open-system", "addock", "googletagmanager", "recaptcha", "wpcf7",
               "contact-form-7", "wp-emoji", "html5.js", "swv")


def clean_scripts(soup):
    import base64
    for s in soup.find_all("script"):
        src = s.get("src", "")
        body = s.string or ""
        if src.startswith("data:text/javascript;base64,"):
            body = base64.b64decode(src.split(",", 1)[1]).decode("utf-8", "replace")
        sid = s.get("id", "")
        blob = " ".join([src, body, sid])
        if any(k in blob for k in THIRD_PARTY):
            s.decompose()
            continue
        if "ajaxurl" in body and src.startswith("data:"):
            s["src"] = "data:text/javascript;base64," + base64.b64encode(
                b'var ajaxurl=[""];var siteurl=[""];var themeurl=[""];').decode()
    for sel in ["#widget-panier", ".cart", "#popin-panier", 'link[href*="open-system"]', 'link[id^="contact-form-7"]']:
        for t in soup.select(sel):
            t.decompose()
    # forms posting to the old server
    for f in soup.find_all("form"):
        f["action"] = "#"
        f["method"] = "get"
    for t in soup.select('input[name="_wpcf7_locale"]'):
        t["value"] = "en_GB"


def build_menu(soup, out_rel):
    root_layer = soup.select_one("#menu-layer-root > div")
    if not root_layer:
        return
    items = {}
    styles = {}
    for el in list(root_layer.children):
        if not isinstance(el, Tag):
            continue
        if el.get("id", "").startswith("menu-layer-root-item-"):
            n = int(el["id"].rsplit("-", 1)[1])
            items[n] = el
            st = el.find_next_sibling()
            if st is not None and st.name == "style":
                styles[n] = st
    anchor_tpl, layer_tpl = items[1], items[3]

    def root_item(pos, label, href=None, layer=None):
        tpl = anchor_tpl if href else layer_tpl
        node = copy.copy(tpl)
        node["id"] = f"menu-layer-root-item-{pos}"
        if href:
            node["href"] = href
        else:
            node["data-target"] = layer
        set_text(text_el(node), label)
        st = copy.copy(styles[pos])
        st.string = (st.string or "").replace(f"menu-layer-root-item-{pos}", f"menu-layer-root-item-{pos}")
        return [node, st]

    new = []
    new += root_item(1, "Home", href=rel(out_rel, "index.html"))
    new += root_item(2, "Destinations", layer="menu-layer-2")
    new += root_item(3, "Trips", layer="menu-layer-3")
    new += root_item(4, "Travel stories", layer="menu-layer-4")
    new += root_item(5, "About us", href=rel(out_rel, PAGES["about"]))
    new += root_item(6, "Contact", href=rel(out_rel, PAGES["contact"]))
    root_layer.clear()
    for n in new:
        root_layer.append(n)

    # sub-layers: reuse menu-layer-2's markup for both
    layer2 = soup.select_one("#menu-layer-2")
    sub_items, sub_styles = [], []
    for el in layer2.select_one("div").children:
        if isinstance(el, Tag) and el.get("id", "").startswith("menu-layer-2-item-"):
            sub_items.append(el)
            st = el.find_next_sibling()
            sub_styles.append(st if st is not None and st.name == "style" else None)

    def make_layer(layer_id, entries):
        layer = copy.copy(layer2)
        layer["id"] = layer_id
        holder = layer.select_one("div")
        holder.clear()
        for i, (label, href) in enumerate(entries):
            node = copy.copy(sub_items[min(i, len(sub_items) - 1)])
            node["id"] = f"{layer_id}-item-{i + 1}"
            node["href"] = href
            set_text(text_el(node), label)
            holder.append(node)
            st = sub_styles[min(i, len(sub_styles) - 1)]
            if st is not None:
                st = copy.copy(st)
                st.string = re.sub(r"menu-layer-2-item-\d+", f"{layer_id}-item-{i + 1}", st.string or "")
                holder.append(st)
        return layer

    dest_entries = [("All destinations", rel(out_rel, PAGES["destinations"]))] + [
        (d["name"], rel(out_rel, PAGES["dest:" + d["slug"]])) for d in C.DESTINATIONS]
    blog_entries = [(b["title"], rel(out_rel, PAGES["blog:" + b["slug"]])) for b in C.BLOG]
    trip_entries = [("All trips", rel(out_rel, PAGES["trips"]))] + [
        (t["name"], rel(out_rel, PAGES["trip:" + t["slug"]])) for t in C.TRIPS] + [
        ("Plan a custom trip", rel(out_rel, PAGES["trips"]) + "#custom-trip")]
    l2 = make_layer("menu-layer-2", dest_entries)
    l3 = make_layer("menu-layer-3", trip_entries)
    l4 = make_layer("menu-layer-4", blog_entries)
    container = layer2.parent
    for lay in [k for k in container.children if isinstance(k, Tag)]:
        if lay.get("id", "").startswith("menu-layer-") and lay["id"] != "menu-layer-root":
            lay.decompose()
    first_layer = container.select_one("#menu-layer-root")
    first_layer.insert_after(l2)
    l2.insert_after(l3)
    l3.insert_after(l4)


def search_script(out_rel):
    entries = [{"u": rel(out_rel, PAGES["dest:" + slug]), "k": kws} for slug, kws in SEARCH_INDEX]
    entries += [{"u": rel(out_rel, PAGES["blog:" + b["slug"]]), "k": [w for w in re.findall(r"[a-z]{5,}", b["title"].lower())]}
                for b in C.BLOG]
    entries = [{"u": rel(out_rel, PAGES["trip:" + t["slug"]]), "k": [t["name"].lower()]} for t in C.TRIPS] + entries
    entries += [{"u": rel(out_rel, PAGES["trips"]), "k": ["trip", "tour", "package", "price", "book"]},
                {"u": rel(out_rel, PAGES["about"]), "k": ["about", "lavigo", "team", "company"]},
                {"u": rel(out_rel, PAGES["contact"]), "k": ["contact", "phone", "email", "plan"]}]
    fallback = rel(out_rel, PAGES["destinations"])
    return ("<script>(function(){var P=" + json.dumps(entries) + ",F=" + json.dumps(fallback) + ";"
            "document.querySelectorAll('#global-search,#global-search-mobile').forEach(function(f){"
            "f.addEventListener('submit',function(e){e.preventDefault();"
            "var q=(f.querySelector('input[name=s]').value||'').toLowerCase().trim();if(!q)return;"
            "for(var i=0;i<P.length;i++){for(var j=0;j<P[i].k.length;j++){var k=P[i].k[j];"
            "if(q.indexOf(k)>-1||k.indexOf(q)>-1){location.href=P[i].u;return;}}}location.href=F;});});"
            "})();</script>")


def forms_script():
    """Static site: forms open the visitor's e-mail app (when a mailto: address is set) and show the thank-you layer."""
    email = C.CONTACT["email_link"]
    return ("<script>(function(){var M=" + json.dumps(email) + ";"
            "document.querySelectorAll('form.wpcf7-form').forEach(function(f){f.addEventListener('submit',function(e){"
            "e.preventDefault();var lines=[];f.querySelectorAll('input,select,textarea').forEach(function(i){"
            "if(i.type==='hidden'||i.type==='submit'||!i.name)return;if(i.type==='checkbox'&&!i.checked)return;"
            "lines.push((i.placeholder||i.name)+': '+i.value);});"
            "if(M.indexOf('mailto:')===0){location.href=M+'?subject='+encodeURIComponent('Website enquiry')+'&body='+encodeURIComponent(lines.join('\\n'));}"
            "var box=f.closest('.form-layer')||f.closest('.wpcf7');var p=box?box.parentNode:null;"
            "if(p){p.classList.add('active');p.querySelectorAll('.success-layer,.form-success').forEach(function(s){s.classList.add('active');s.classList.remove('hidden');});"
            "if(box.classList.contains('form-layer')){box.classList.remove('active');}}"
            "f.reset();});});})();</script>")


def build_footer(soup, out_rel):
    footer = soup.find("footer")
    if not footer:
        return
    news = footer.find(string=re.compile("Subscribe to our newsletter"))
    if news:
        title_el = news.parent
        set_text(title_el, C.NEWSLETTER["title"])
        sub = title_el.find_next_sibling()
        if sub:
            set_text(sub, C.NEWSLETTER["text"])
    for inp in footer.select('input[type="email"]'):
        inp["placeholder"] = "Email address"
    for inp in footer.select('input[type="submit"]'):
        inp["value"] = "Subscribe"
    # contact column
    contact_a = footer.find("a", href=re.compile(r"contact/index\.html$|^index\.html$|contact"))
    addr = footer.find("a", href=re.compile(r"google\.com/maps"))
    if addr:
        addr["href"] = C.CONTACT["map_link"]
        addr.clear()
        for i, line in enumerate(C.CONTACT["address_lines"]):
            if i:
                addr.append(soup.new_tag("br"))
            addr.append(NavigableString(" " + line + " "))
    tel = footer.find("a", href=re.compile(r"^tel:"))
    if tel:
        tel["href"] = C.CONTACT["phone_link"]
        set_text(tel, C.CONTACT["phone"])
    for a in footer.find_all("a", href=re.compile("facebook")):
        a["href"] = C.CONTACT["facebook"]
    for a in footer.find_all("a", href=re.compile("instagram")):
        a["href"] = C.CONTACT["instagram"]
    # link column
    links = [("Our trips", PAGES["trips"]), ("Our destinations", PAGES["destinations"]),
             ("Travel stories", PAGES["blog:" + C.BLOG[0]["slug"]]), ("About us", PAGES["about"]),
             ("Plan your trip", PAGES["contact"])]
    heads = footer.select(".menu-head")
    while heads and len(heads) < len(links):
        extra = copy.copy(heads[-1])
        heads[-1].insert_after(extra)
        heads.append(extra)
    for head, (label, target) in zip(heads, links):
        a = head.find("a")
        a["href"] = rel(out_rel, target)
        set_text(a.select_one(".t-small"), label)
    for extra in heads[len(links):]:
        extra.decompose()
    # funding band -> tagline
    band = footer.select_one(".bg-color-midgreen .flexbox")
    if band:
        band.clear()
        band.append(frag(f'<div class="t-credits center-holder width-100">{html.escape(C.FOOTER_TAGLINE)}</div>'))
    # bottom line
    bottom = footer.select_one(".bg-color-green .flexbox")
    if bottom:
        bottom.clear()
        bottom.append(frag(
            f'<div class="t-credits">&copy; {C.COMPANY} {C.YEAR}</div>'
            '<div class="t-credits sep hide-mobile">&nbsp;|&nbsp;</div>'
            f'<div class="t-credits"><a href="{rel(out_rel, PAGES["legal"])}" class="hover-underline">Terms of use</a></div>'
            '<div class="t-credits sep hide-mobile">&nbsp;|&nbsp;</div>'
            f'<div class="t-credits"><a href="{rel(out_rel, PAGES["legal"])}#photo-credits" class="hover-underline">Photo credits</a></div>'))
    _ = contact_a


def chrome(soup, out_rel, title, description, image_key, dark_logo=False):
    clean_head(soup, out_rel, title, description, image_key)
    clean_scripts(soup)
    replace_logos(soup, out_rel, dark_logo)
    build_menu(soup, out_rel)
    build_footer(soup, out_rel)
    for a in soup.find_all("a", href=True):
        if a["href"].endswith("home.html") or a["href"].endswith("home.html#section-blog"):
            a["href"] = rel(out_rel, "home.html" + ("#section-blog" if "#section-blog" in a["href"] else ""))
    soup.body.append(frag(search_script(out_rel)))
    soup.body.append(frag(forms_script()))
    soup.head.append(frag(f'<link rel="stylesheet" href="{rel(out_rel, "assets/css/lavigo.css")}" media="all" />'))
    hello = f"Hello {C.COMPANY}, I would like some information about a trip."
    soup.body.append(frag(f'<a class="lavigo-wa-float" href="{wa_link(hello)}" target="_blank" rel="noopener" '
                          f'aria-label="Chat with {C.COMPANY} on WhatsApp" title="WhatsApp">{WHATSAPP_ICON}</a>'))
    # decorative stag watermark of the old brand
    for sv in soup.find_all("svg"):
        if (sv.get("viewbox") or sv.get("viewBox")) == "0 0 591 605":
            sv.decompose()


# ---------------------------------------------------------------- shared components
def build_gallery(soup, out_rel, first_slug=None):
    sec = soup.select_one("#section-gallery")
    if not sec:
        return
    set_heading(sec.find("h2"), C.GALLERY["line1"], C.GALLERY["line2"])
    order = list(C.DESTINATIONS)
    if first_slug:
        i = [d["slug"] for d in order].index(first_slug)
        order = order[i:] + order[:i]
    car = sec.select_one("#carousel-gallery .carousel-container")
    templates = [k for k in car.children if isinstance(k, Tag)]

    def fill(node, d, i):
        node["id"] = f"carousel-gallery-slide-{i}"
        node["href"] = rel(out_rel, PAGES["dest:" + d["slug"]])
        url = rel(out_rel, img_path(d["card_image"]))
        for t in bg_tags(node):
            set_bg(t, url)
        for c in captions(node):
            set_text(c, credit(d["card_image"]))
        texts = [t for t in node.find_all("div") if t.string and t.string.strip() and not t.get("class", []).count("media-caption-value")]
        texts = [t for t in texts if "media-caption-value" not in t.get("class", [])]
        # title, text, "Find out more"
        set_text(texts[1] if texts[0].string.strip() == "©" else texts[0], d["name"])
        body = [t for t in texts if len(t.string.strip()) > 40]
        if body:
            set_text(body[0], d["card_text"])

    fill_list(car, order, fill, templates)


def popin_json(out_rel, keys):
    return json.dumps([{"full": rel(out_rel, img_path(k)), "copyright": credit(k)} for k in keys])


# ---------------------------------------------------------------- pages
def page_home(base, out_rel, skip_intro):
    soup = load(os.path.join(base, "home.html" if skip_intro else "index.html"))
    chrome(soup, out_rel, C.COMPANY, C.HERO["description"], C.HERO["image"])
    # hero
    intro = soup.select_one("#section-intro")
    for t in bg_tags(intro):
        set_bg(t, rel(out_rel, img_path(C.HERO["image"])))
        # the original filters suited a dark lake photo; tune them for bright snowy pictures
        t["style"] = t["style"].replace("filter:brightness(1.75)", "filter:brightness(1.12) saturate(1.1)")
        t["style"] = t["style"].replace("filter:brightness(0.75)", "filter:brightness(0.8)")
    ring = intro.select_one(".height-38em.squared")
    if ring:
        # darker disc exactly inside the ring's hole (the ring mask starts at 42%) so logo and text read well
        ring.insert(1, frag('<div class="abs width-100 height-100 no-events" style="border-radius:50%;'
                            'background:radial-gradient(circle, rgba(12,22,10,.62) 0%, rgba(12,22,10,.5) 30%, '
                            'rgba(12,22,10,.42) 41.5%, transparent 42%);"></div>').contents[0])
        # thin outlines on both edges of the ring. The mask runs from 42% to 70% of the distance to the
        # box corner (radius = side x 0.7071), i.e. circles of 99% and 59.4% of the box side.
        for size in (99, 59.4):
            ring.insert(2, frag(f'<div class="abs no-events anim onload fade-in delay-1-5" style="width:{size}%;height:{size}%;'
                                f'left:{(100 - size) / 2:.1f}%;top:{(100 - size) / 2:.1f}%;border-radius:50%;'
                                'border:1px solid rgba(255,255,255,.7);box-sizing:border-box;"></div>').contents[0])
    texts = intro.select_one(".color-white.uppercase")
    if texts:
        # slightly smaller text in the circle
        texts["style"] = "text-shadow:0 2px 14px rgba(0,0,0,.55);transform:scale(.85);transform-origin:center top;"
    for im in intro.select("img.lavigo-logo"):
        im["style"] += "filter:drop-shadow(0 2px 10px rgba(0,0,0,.45));"
    set_text(intro.select_one(".t-title-head"), C.HERO["line1"])
    set_text(intro.select_one(".t-title-content"), C.HERO["line2"])
    for c in captions(intro):
        set_text(c, credit(C.HERO["image"]))
    build_map(soup, out_rel)
    build_blog_section(soup, out_rel)
    build_gallery(soup, out_rel)
    build_outro(soup, out_rel)
    reviews = reviews_section(out_rel)
    if reviews:
        soup.select_one("#section-gallery").insert_after(frag(reviews))
    build_cta(soup, out_rel)
    soup.head.append(frag(agency_jsonld(out_rel)))
    tags = [("#section-intro", "Welcome"), ("#section-map", C.MAP["line1"] + " " + C.MAP["line2"]),
            ("#section-blog", "Travel stories"), ("#section-gallery", "Destinations")]
    if reviews:
        tags.append(("#section-reviews", "Reviews"))
    tags += [("#section-outro", "About " + C.COMPANY), ("#section-cta", "Book your trip"), ("footer", "Contact")]
    add_section_tag(soup, tags)
    return soup


def build_cta(soup, out_rel):
    """'What are you waiting for?' block above the footer: trip cards + booking buttons."""
    X = C.HOME_CTA
    cards = "".join(
        f'<a class="lavigo-cta-trip" href="{rel(out_rel, PAGES["trip:" + t["slug"]])}">'
        f'<div class="img" style="background-image:url(&quot;{rel(out_rel, img_path(t["card_image"]))}&quot;);"></div>'
        f'<div class="txt"><div class="t">{html.escape(t["name"])}</div>'
        f'<div class="m">{t["days"]} days · from {money(t["price_adult"])}</div></div></a>'
        for t in [x for slug in X.get("trips", []) for x in C.TRIPS if x["slug"] == slug] or C.TRIPS[:4])
    hello = f"Hello {C.COMPANY}, I would like to book a trip."
    block = (
        '<section class="lavigo-section lavigo-cta bg-color-lightgreen" id="section-cta"><div class="centered-midwide">'
        f'{section_heading(X["small"], X["title"])}'
        f'<div class="t-base lead">{html.escape(X["text"])}</div>'
        f'<div class="lavigo-cta-trips">{cards}</div>'
        '<div class="lavigo-cta-btns">'
        f'<a class="lavigo-wa-btn lavigo-btn-outline" href="{rel(out_rel, PAGES["trips"])}"><span>{html.escape(X["button_trips"])}</span></a>'
        f'<a class="lavigo-wa-btn lavigo-btn-outline" href="{rel(out_rel, PAGES["trips"])}#custom-trip"><span>{html.escape(X["button_custom"])}</span></a>'
        f'<a class="lavigo-wa-btn" href="{wa_link(hello)}" target="_blank" rel="noopener">{WHATSAPP_ICON}'
        f'<span>{html.escape(X["button_book"])}</span></a>'
        '</div></div></section>')
    soup.select_one("#section-outro").insert_after(frag(block))


def add_section_tag(soup, sections):
    """Fixed square tag naming the section currently in view (updates while scrolling)."""
    soup.body.append(frag('<div class="lavigo-tag" aria-hidden="true"><span class="num">01</span><span class="name"></span></div>'))
    soup.body.append(frag(
        "<script>(function(){var S=" + json.dumps(sections) + ",tag=document.querySelector('.lavigo-tag'),"
        "num=tag.querySelector('.num'),name=tag.querySelector('.name'),cur=-1;"
        "function show(i){if(i===cur)return;cur=i;name.classList.add('swap');setTimeout(function(){"
        "num.textContent=(i<9?'0':'')+(i+1);name.textContent=S[i][1];name.classList.remove('swap');},cur<0?0:200);}"
        "function check(){var mid=window.innerHeight/2,best=0;for(var i=0;i<S.length;i++){var el=document.querySelector(S[i][0]);"
        "if(el&&el.getBoundingClientRect().top<=mid)best=i;}"
        "if(window.innerHeight+window.scrollY>=document.documentElement.scrollHeight-4)best=S.length-1;"
        "show(best);tag.classList.add('on');}"
        "window.addEventListener('scroll',check,{passive:true});window.addEventListener('resize',check);"
        "setTimeout(check,1800);})();</script>"))


def build_map(soup, out_rel):
    sec = soup.select_one("#section-map")
    for h in sec.select("h2, .only-mobile .uppercase"):
        if h.select_one(".t-title-1") and h.select_one(".t-title-2"):
            set_heading(h, C.MAP["line1"], C.MAP["line2"])
    dests = C.DESTINATIONS
    icons_src = [k for k in sec.select_one("#carousel-map-icons").children if isinstance(k, Tag)]

    def set_active(node, i):
        (add_class if i == 0 else remove_class)(node, "active")

    def fill_img1(node, d, i):
        set_active(node, i)
        for t in bg_tags(node):
            set_bg(t, rel(out_rel, img_path(d["card_image"])))

    def fill_img2(node, d, i):
        set_active(node, i)
        node["href"] = rel(out_rel, PAGES["dest:" + d["slug"]])
        for t in bg_tags(node):
            set_bg(t, rel(out_rel, img_path(d["card_image"])))
        for c in captions(node):
            set_text(c, credit(d["card_image"]))

    def fill_icon(node, d, i):
        src = icons_src[d["map_icon"]]
        node.clear()
        for k in copy.copy(src).contents:
            node.append(copy.copy(k))
        node.attrs = dict(src.attrs)
        set_active(node, i)
        for t in node.find_all(style=re.compile("background-color")):
            t["style"] = re.sub(r"background-color:[^;]*;", f"background-color:{d['map_color']};", t["style"])

    def fill_content(node, d, i):
        set_active(node, i)
        set_text(node.select_one(".t-title-3"), d["name"])
        body = node.select_one(".t-base")
        set_text(body, d["map_text"])
        node.find("a")["href"] = rel(out_rel, PAGES["dest:" + d["slug"]])
        set_text(node.find("a").select_one(".t-small"), "Discover " + d["name"])

    fill_list(sec.select_one("#carousel-map-images-1"), dests, fill_img1)
    fill_list(sec.select_one("#carousel-map-images-2"), dests, fill_img2)
    fill_list(sec.select_one("#carousel-map-icons"), dests, fill_icon, icons_src)
    fill_list(sec.select_one("#carousel-map-content"), dests, fill_content)

    # the map itself
    old = sec.find("svg", attrs={"viewbox": "0 0 600 482"}) or sec.find("svg", attrs={"viewBox": "0 0 600 482"})
    new_svg = frag(open(os.path.join(CONTENT_DIR, "map", "travel-map.svg"), encoding="utf-8").read()).find("svg")
    old.replace_with(new_svg)
    pointers = sec.select_one("#map-pointers")
    dots = [k for k in pointers.children if isinstance(k, Tag) and "dyn-pointer" not in k.get("class", [])]
    dyn = [k for k in pointers.children if isinstance(k, Tag) and "dyn-pointer" in k.get("class", [])]
    dot_tpl, dyn_tpl = dots[0], dyn[0]
    pointers.clear()
    for name, (x, y) in MAP["towns"].items():
        if name in ("Kathmandu", "Dharamshala", "Pelling"):  # these sit under a destination pin
            continue
        dnode = copy.copy(dot_tpl)
        dnode["style"] = f"left:{x}%; top:{y}%;"
        set_text(dnode.select_one(".t-normal"), name)
        pointers.append(dnode)
    for i, d in enumerate(dests):
        x, y = MAP["pointers"][d["slug"]]
        p = renumber(dyn_tpl, "dyn-pointer-0", f"dyn-pointer-{i}")
        p.attrs["data-target"] = p["data-target"].replace("nth-child(1)", f"nth-child({i + 1})")
        p["style"] = f"left:{x}%; top:{y}%;"
        (add_class if i == 0 else remove_class)(p, "active")
        src_icon = icons_src[d["map_icon"]]
        color = d["map_color"]
        icon_holder = p.select_one(".svg-fit-height")
        icon_holder.clear()
        icon_holder.append(copy.copy(src_icon.find("svg")))
        for t in p.find_all(style=True):
            t["style"] = re.sub(r"#[0-9a-fA-F]{6}", color, t["style"])
        for t in p.find_all("path", fill=True):
            if t["fill"].startswith("#"):
                t["fill"] = color
        pointers.append(p)


def build_blog_section(soup, out_rel):
    sec = soup.select_one("#section-blog")
    set_heading(sec.find("h2"), C.BLOG_SECTION["line1"], C.BLOG_SECTION["line2"])

    def fill_img(node, b, i):
        (add_class if i == 0 else remove_class)(node, "active")
        for t in bg_tags(node):
            set_bg(t, rel(out_rel, img_path(b["image"])))
        for c in captions(node):
            set_text(c, credit(b["image"]))

    def fill_content(node, b, i):
        (add_class if i == 0 else remove_class)(node, "active")
        texts = [t for t in node.find_all("div") if t.string and t.string.strip()]
        set_text(texts[0], b["title"])
        set_text(texts[1], b["excerpt"])
        a = node.find("a")
        a["href"] = rel(out_rel, PAGES["blog:" + b["slug"]])
        set_text(a.select_one(".t-small") or texts[2], "Read more")

    fill_list(sec.select_one("#carousel-blog-images"), C.BLOG, fill_img)
    fill_list(sec.select_one("#carousel-blog-content"), C.BLOG, fill_content)
    # section background (photo behind the carousel)
    big = [t for t in bg_tags(sec) if not t.find_parent(id="carousel-blog-images")]
    for t in big:
        set_bg(t, rel(out_rel, img_path("lachen-teesta")))
    for c in captions(sec):
        if not c.find_parent(id="carousel-blog-images"):
            set_text(c, credit("lachen-teesta"))


def build_outro(soup, out_rel):
    sec = soup.select_one("#section-outro")
    for t in bg_tags(sec):
        set_bg(t, rel(out_rel, img_path(C.OUTRO["image"])))
    set_text(sec.select_one(".t-title-1"), C.OUTRO["line1"])
    set_text(sec.select_one(".t-title-2"), C.OUTRO["line2"])
    for c in captions(sec):
        set_text(c, credit(C.OUTRO["image"]))
    # context map
    ctx = MAP["context"]
    cmap = sec.select_one("#context-map")
    box = cmap.select_one(".squared")
    country = box.find("svg", attrs={"viewbox": "0 0 112 117"}) or box.find("svg")
    country.replace_with(frag(open(os.path.join(CONTENT_DIR, "map", "context-country.svg"), encoding="utf-8").read()).find("svg"))
    regions = [d for d in box.find_all("div", recursive=False) if "left:" in d.get("style", "")]
    files = ["context-region.svg", "context-region-zoom.svg"]
    cx, cy = ctx["region_center_pct"]
    for d, fname in zip(regions, files):
        d["style"] = f"height:{ctx['region_height_pct']}%; left:{cx}%; top:{cy}%;"
        old = d.find("svg")
        old.replace_with(frag(open(os.path.join(CONTENT_DIR, "map", fname), encoding="utf-8").read()).find("svg"))
    # zoom so the region fills ~90% of the frame (the original used a fixed 9x for a smaller region)
    region_w_em = ctx["region_height_pct"] / 100 * 15 * ctx["region_aspect"]
    zoom = round(22 / region_w_em, 2)  # zoomed region ~22em wide inside the 30em circle
    unzoom = round(1 / zoom, 4)
    dots_holder = regions[0].select_one(".scaled-0-125")
    if dots_holder:
        tpl = dots_holder.find("div", recursive=False)
        dots_holder.clear()
        for name, (x, y) in ctx["zoom_dots"].items():
            n = copy.copy(tpl)
            # the holder is shrunk by 1/zoom around its centre, so spread positions by zoom
            n["style"] = f"left:{50 + (x - 50) * zoom:.1f}%; top:{50 + (y - 50) * zoom:.1f}%;"
            set_text(n.select_one(".t-ssmall"), name)
            dots_holder.append(n)
        remove_class(dots_holder, "scaled-0-125")
        add_class(dots_holder, "lavigo-unzoom")
    # move the 15em country box so the region sits near the centre of the 30em circle, and zoom from there
    ox, oy = 50.0, 52.0
    box["style"] = f"left:{ox - cx * 0.5:.2f}%; top:{oy - cy * 0.5:.2f}%;"
    for c in ("top-20", "left-15"):
        remove_class(box, c)
    set_text(sec.select_one("#region-title .t-cantal"), C.OUTRO["region"])
    for st in sec.find_all("style"):
        if "context-map" in (st.string or ""):
            st.string = (f"#context-map {{ transform-origin:{ox:.2f}% {oy:.2f}%;}} #region-title {{ left:{ox:.2f}%;}} "
                         f".spe-parent.active .lavigo-zoom {{ transform:scale({zoom}); }} .lavigo-unzoom {{ transform:scale({unzoom}); }} "
                         "@media screen and (max-width: 900px) { #context-map { transform-origin:50% 50%;} #region-title { left:50%;} }")
    for t in [cmap] + cmap.select(".active-spe-parent-scaled-9"):
        if "active-spe-parent-scaled-9" in t.get("class", []):
            remove_class(t, "active-spe-parent-scaled-9")
            add_class(t, "lavigo-zoom")
    style = None
    _ = style


def detail_intro(soup, out_rel, hero, back, label, title, paragraphs):
    """Fill the photo header + intro of the destination-page template."""
    intro = soup.select_one("#section-intro")
    for t in bg_tags(intro):
        set_bg(t, rel(out_rel, img_path(hero)))
    intro.find("a")["href"] = rel(out_rel, back)
    old = intro.find(string=re.compile("Discover the destination"))
    if old:
        old.replace_with(label)
    parts = intro.find("h1").find_all("div")
    set_text(parts[0], title[0])
    set_text(parts[1], title[1])
    rich(intro.select_one(".rich-content"), paragraphs)
    return intro


def fill_places(soup, out_rel, places, heading=None):
    """Alternating circular photo galleries (#section-locations of the destination template)."""
    sec = soup.select_one("#section-locations")
    even = sec.select_one("#location-0")
    odd = sec.select_one("#location-1")
    for loc in sec.find_all(id=re.compile(r"^location-\d+$")):
        loc.extract()
    if heading:
        sec.append(frag(section_heading(*heading)))
    for i, place in enumerate(places):
        tpl, old_i = (even, 0) if i % 2 == 0 else (odd, 1)
        node = frag(str(tpl).replace(f"location-{old_i}", f"location-{i}")).contents[0]
        sec.append(node)
        car = node.select_one(f"#carousel-location-{i}")
        keys = place["images"]
        pj = popin_json(out_rel, keys)

        def fill(slide, key, j, pj=pj):
            (add_class if j == 0 else remove_class)(slide, "active")
            sw = slide.select_one(".popin-switch")
            sw["data-popin-initial"] = str(j)
            sw["data-popin-imgs"] = pj
            for t in bg_tags(slide):
                set_bg(t, rel(out_rel, img_path(key)))

        fill_list(car, keys, fill)
        counter = node.find(id=f"carousel-location-{i}-current")
        total = counter.parent
        total.clear()
        total.append(counter)
        set_text(counter, "1")
        total.append(NavigableString(f" / {len(keys)}"))
        if len(keys) == 1:
            nav = total.find_parent(class_="flexbox")
            if nav:
                nav["style"] = "visibility:hidden;"
        hp = node.find("h2").find_all("div")
        set_text(hp[0], place["label"])
        set_text(hp[1], place["name"])
        rich(node.select_one(".rich-content"), place["text"])
    return sec


def section_heading(small, big, color="color-green"):
    """Heading in the style of the place titles (small label + big uppercase title)."""
    return (f'<div class="lavigo-heading"><h2 class="uppercase {color}"><div class="t-normal">{html.escape(small)}</div>'
            f'<div class="t-title-2">{html.escape(big)}</div></h2></div>')


def page_destination(base, out_rel, d):
    soup = load(os.path.join(base, "discover-the-destination/land-of-lakes/index.html"))
    chrome(soup, out_rel, d["name"], d["card_text"], d["hero"])
    detail_intro(soup, out_rel, d["hero"], PAGES["destinations"], "Destinations", d["title"], d["intro"])
    fill_places(soup, out_rel, d["places"])
    trips = [t for t in C.TRIPS if d["slug"] in trip_destinations(t)]
    if trips:
        soup.select_one("#section-locations").insert_after(frag(trips_teaser(out_rel, trips, d["name"])))
    build_gallery(soup, out_rel, d["slug"])
    return soup


def trip_destinations(t):
    """Destination slugs a trip goes to (from the images it uses)."""
    keys = [t["hero"], t["card_image"]] + [k for p in t["places"] for k in p["images"]]
    found = []
    for d in C.DESTINATIONS:
        imgs = {d["hero"], d["card_image"]} | {k for p in d["places"] for k in p["images"]}
        if imgs & set(keys):
            found.append(d["slug"])
    return found


def trips_teaser(out_rel, trips, where):
    rows = "".join(
        f'<a class="lavigo-day" style="text-decoration:none;color:inherit;" href="{rel(out_rel, PAGES["trip:" + t["slug"]])}">'
        f'<div class="n"><b>{t["days"]}</b>days</div><div><h3>{html.escape(t["name"])}</h3>'
        f'<div class="t-base">{html.escape(t["tagline"])} &ndash; from {money(t["price_adult"])} per adult</div>'
        f'<div class="t-small top-margin-0-5 color-green">See dates and book &rarr;</div></div></a>'
        for t in trips)
    return (f'<section class="lavigo-section bg-color-lightgreen" id="section-trips"><div class="centered-midwide">'
            f'{section_heading("Trips including " + where, "Travel with us")}<div class="lavigo-days">{rows}</div></div></section>')


def page_cards(base, out_rel, page_title, P, cards, outro_link, dark_logo=True):
    """Overview page (grid of photo cards). cards: list of (name, subline, href, image)."""
    soup = load(os.path.join(base, "discover-the-destination/index.html"))
    chrome(soup, out_rel, page_title, P["intro"][:150], P["image"], dark_logo=dark_logo)
    intro = soup.select_one("#section-intro")
    for t in bg_tags(intro):
        set_bg(t, rel(out_rel, img_path(P["image"])))
    set_text(intro.find("h1"), P["title"])
    txt = intro.find(string=re.compile("Sumène Artense"))
    set_text(txt.parent, P["intro"])
    sec = soup.select_one("#section-destinations")
    card_nodes = [a.find_parent(lambda t: t.name == "div" and t.parent is not None and len(
        [k for k in t.parent.children if isinstance(k, Tag)]) > 3) for a in sec.find_all("a", href=True)]
    holder = card_nodes[0].parent
    if len(cards) % 2:  # odd count: last card centred, like the original 7th card
        templates = [card_nodes[i % 2] for i in range(len(cards) - 1)] + [card_nodes[-1]]
    else:
        templates = [card_nodes[i % 2] for i in range(len(cards))]

    def fill(node, card, i):
        name, sub, href, image = card
        a = node.find("a", href=True)
        a["href"] = href
        for t in bg_tags(node):
            set_bg(t, rel(out_rel, img_path(image)))
        for c in captions(node):
            set_text(c, credit(image))
        title = node.select_one(".t-title-2")
        set_text(title, name)
        if sub:
            wrap = frag(f'<div class="center-holder z-index-3"></div>').contents[0]
            title.replace_with(wrap)
            wrap.append(title)
            wrap.append(frag(f'<div class="lavigo-card-sub color-white text-shadow">{html.escape(sub)}</div>'))

    fill_list(holder, cards, fill, templates)
    out = soup.select_one("#section-outro")
    set_text(out.find("h2"), P["outro_title"])
    rc = out.select_one(".rich-content") or out.find("h2").find_next_sibling()
    rc.clear()
    tb = frag('<div class="t-base"></div>').contents[0]
    rc.append(tb)
    for p in P["outro_text"]:
        tb.append(frag(f"<p>{html.escape(p)}</p>"))
        tb.append(soup.new_tag("br"))
    tb.append(frag(f'<p><a href="{outro_link[1]}">{html.escape(outro_link[0])}</a></p>'))
    for t in bg_tags(out):
        set_bg(t, rel(out_rel, img_path(P["outro_image"])))
    return soup


def page_destinations(base, out_rel):
    cards = [(d["name"], "", rel(out_rel, PAGES["dest:" + d["slug"]]), d["card_image"]) for d in C.DESTINATIONS]
    return page_cards(base, out_rel, "Destinations", C.DESTINATIONS_PAGE, cards,
                      (f"Contact the {C.COMPANY} travel desk", rel(out_rel, PAGES["contact"])))


def page_trips(base, out_rel):
    cards = [(t["name"], f"{t['days']} days · {t['nights']} nights · from {money(t['price_adult'])}",
              rel(out_rel, PAGES["trip:" + t["slug"]]), t["card_image"]) for t in C.TRIPS]
    soup = page_cards(base, out_rel, "Trips", C.TRIPS_PAGE, cards, ("Plan a custom trip", "#custom-trip"))
    soup.select_one("#section-destinations").insert_after(frag(custom_trip_section()))
    soup.body.append(frag(f'<script src="{rel(out_rel, "assets/js/lavigo-custom.js")}"></script>'))
    return soup


def custom_trip_section():
    X = C.CUSTOM_TRIP
    chips = "".join(f'<label class="lavigo-chip"><input type="checkbox" name="places" value="{html.escape(p)}"/>'
                    f'<span>{html.escape(p)}</span></label>' for p in X["places"])
    budgets = "".join(f'<option>{html.escape(b)}</option>' for b in X["budgets"])

    def field(name, placeholder, kind="text", extra=""):
        return (f'<label><span class="input"><input type="{kind}" name="{name}" placeholder="{placeholder}" {extra}/></span></label>')

    def num(name, label, value, minimum):
        return (f'<label><span class="lbl">{label}</span><span class="lavigo-stepper">'
                f'<button type="button" data-step="-1" data-for="{name}" aria-label="Fewer">&minus;</button>'
                f'<input type="number" name="{name}" value="{value}" min="{minimum}" max="30" inputmode="numeric"/>'
                f'<button type="button" data-step="1" data-for="{name}" aria-label="More">+</button></span></label>')

    return (
        '<section class="lavigo-section bg-color-lightgreen" id="custom-trip"><div class="centered-midwide">'
        f'{section_heading(X["small"], X["title"])}'
        f'<div class="t-base center-holder" style="max-width:38em;margin:-1.5em auto 2.5em;">{html.escape(X["text"])}</div>'
        f'<div id="lavigo-custom" class="wpcf7 lavigo-custom" data-wa="{C.CONTACT["whatsapp"]}" data-company="{C.COMPANY}">'
        '<form action="#"><div class="lavigo-custom-grid"><div>'
        + field("name", "Your name*", extra="required")
        + field("phone", "Phone (optional)", "tel")
        + '<label><span class="lbl">Where would you like to go?</span></label>'
        f'<div class="lavigo-chips">{chips}</div>'
        + '</div><div>'
        + '<label><span class="lbl">When?</span><span class="input"><input type="month" name="month"/></span></label>'
        + num("days", "Number of days", 6, 2)
        + '<div class="lavigo-two-inputs">' + num("adults", "Adults", 2, 1) + num("children", "Children (under 11)", 0, 0) + '</div>'
        + f'<label><span class="lbl">Budget</span><span class="input"><select name="budget">{budgets}</select></span></label>'
        + '<label><span class="input"><textarea name="message" rows="3" placeholder="Anything else? (hotel style, interests, special occasions...)"></textarea></span></label>'
        + '</div></div>'
        f'<div class="center-holder top-margin-2"><button type="submit" class="lavigo-wa-btn" style="display:inline-flex;border:none;cursor:pointer;">'
        f'{WHATSAPP_ICON}<span>{html.escape(X["button"])}</span></button></div>'
        '</form></div></div></section>')


def page_trip(base, out_rel, t):
    soup = load(os.path.join(base, "discover-the-destination/land-of-lakes/index.html"))
    chrome(soup, out_rel, t["name"], t["tagline"], t["hero"])
    intro = detail_intro(soup, out_rel, t["hero"], PAGES["trips"], "Trips",
                         (t["name"], f"{t['days']} days · {t['nights']} nights"), t["overview"])
    for el in intro.find_all(attrs={"data-target": "#location-0"}):
        el["data-target"] = "#trip-details"

    dates = t["dates"]
    first = nice_date(dates[0]) if dates else "On request"
    more = f"+ {len(dates) - 1} more dates" if len(dates) > 1 else ""
    facts = (
        '<div class="lavigo-facts">'
        f'<div class="lavigo-fact"><div class="k">Total days</div><div class="v">{t["days"]} days<small>{t["nights"]} nights</small></div></div>'
        f'<div class="lavigo-fact"><div class="k">Next departure</div><div class="v">{first}<small>{more}</small></div></div>'
        f'<div class="lavigo-fact"><div class="k">Start / end</div><div class="v">{html.escape(t["start"])}'
        f'<small>ends in {html.escape(t["end"])}</small></div></div>'
        f'<div class="lavigo-fact"><div class="k">Price from</div><div class="v">{money(t["price_adult"])}'
        f'<small>{child_note(t)}</small></div></div>'
        '</div>')
    date_list = "".join(f"<li>{nice_date(x)}</li>" for x in dates)
    highlights = "".join(f"<li>{html.escape(h)}</li>" for h in t["highlights"])
    details = (
        '<section class="lavigo-section" id="trip-details"><div class="centered-midwide">'
        f'{facts}'
        '<div class="flexbox gap-4 column-mobile" style="margin-top:4em;">'
        f'<div class="flex-2"><h2 class="uppercase color-green"><div class="t-normal">Why you will love it</div>'
        f'<div class="t-title-2">Highlights</div></h2><div class="top-margin-2 t-base"><ul class="lavigo-list">{highlights}</ul></div></div>'
        f'<div class="flex"><h2 class="uppercase color-green"><div class="t-normal">Departures</div>'
        f'<div class="t-title-2">Dates</div></h2><div class="top-margin-2 t-base"><ul class="lavigo-list">{date_list}</ul>'
        f'<div class="t-small top-margin-1"><a class="hover-underline" href="#trip-booking">Check the price for your group &rarr;</a></div>'
        '</div></div></div></div></section>')
    intro.insert_after(frag(details))

    sec = fill_places(soup, out_rel, t["places"], heading=("On the way", "Places you'll visit"))
    add_class(sec, "lavigo-places")

    days = "".join(
        f'<div class="lavigo-day"><div class="n">Day<b>{i + 1}</b></div><div><h3>{html.escape(title)}</h3>'
        f'<div class="t-base">{html.escape(text)}</div></div></div>'
        for i, (title, text) in enumerate(t["itinerary"]))
    itinerary = (f'<section class="lavigo-section" id="trip-itinerary"><div class="centered-midwide">'
                 f'{section_heading("Itinerary", "Day by day")}<div class="lavigo-days">{days}</div></div></section>')

    inc = "".join(f"<li>{html.escape(x)}</li>" for x in t["included"])
    exc = "".join(f"<li>{html.escape(x)}</li>" for x in t["not_included"])
    included = (
        '<section class="lavigo-section bg-color-lightgreen" id="trip-included"><div class="centered-midwide"><div class="lavigo-two">'
        f'<div><h2 class="uppercase color-green"><div class="t-normal">The price includes</div><div class="t-title-2">Included</div></h2>'
        f'<div class="top-margin-2 t-base"><ul class="lavigo-list yes">{inc}</ul></div></div>'
        f'<div><h2 class="uppercase color-green"><div class="t-normal">To plan separately</div><div class="t-title-2">Not included</div></h2>'
        f'<div class="top-margin-2 t-base"><ul class="lavigo-list no">{exc}</ul></div></div>'
        '</div></div></section>')

    options = "".join(f'<option value="{x}">{nice_date(x)}</option>' for x in dates) or '<option>Flexible dates</option>'

    def stepper(name, label, value, minimum, price):
        return (f'<label><span class="lbl">{label}</span><span class="lavigo-stepper">'
                f'<button type="button" data-step="-1" data-for="{name}" aria-label="Fewer">&minus;</button>'
                f'<input type="number" name="{name}" value="{value}" min="{minimum}" max="20" inputmode="numeric"/>'
                f'<button type="button" data-step="1" data-for="{name}" aria-label="More">+</button>'
                f'<span class="price">{price}</span></span></label>')

    calc = (
        f'<section class="lavigo-section" id="trip-booking"><div class="centered-midwide">'
        f'{section_heading("Calculate your trip cost", "Book this trip")}'
        f'<div id="lavigo-calc" class="lavigo-calc" data-adult="{t["price_adult"]}" data-child="{t["price_child"] or 0}" '
        f'data-currency="{C.CURRENCY}" data-trip="{html.escape(t["name"])}" data-days="{t["days"]} days / {t["nights"]} nights" '
        f'data-wa="{C.CONTACT["whatsapp"]}" data-company="{C.COMPANY}">'
        '<div class="wpcf7"><form action="#">'
        f'<label><span class="lbl">Departure date</span><span class="input"><select name="date">{options}</select></span></label>'
        + (stepper("adults", "Adults (above 10 years)", 2, 1, f"{money(t['price_adult'])} each")
           + stepper("children", "Children (3 to 10 years)", 0, 0, f"{money(t['price_child'])} each")
           + stepper("infants", "Children under 3", 0, 0, "free")
           if t["price_child"] else
           stepper("adults", f"Travellers ({t.get('min_age', 12)}+ years)", 2, 1, f"{money(t['price_adult'])} each"))
        + '</form></div>'
        '<div class="lavigo-summary">'
        f'<div class="t-title-3 montaga color-green">{html.escape(t["name"])}</div>'
        f'<div class="t-small top-margin-0-5">{t["days"]} days / {t["nights"]} nights</div>'
        '<div class="top-margin-1-5">'
        '<div class="row"><span>Adults <span data-out="adults"></span></span><span data-out="adults-total"></span></div>'
        + ('<div class="row"><span>Children <span data-out="children"></span></span><span data-out="children-total"></span></div>'
           '<div class="row"><span>Under 3 years</span><span><span data-out="infants"></span> &middot; free</span></div>'
           if t["price_child"] else "") +
        '</div>'
        '<div class="total"><span class="t-normal uppercase">Estimated total</span><b data-out="total"></b></div>'
        f'<a class="lavigo-wa-btn" href="{wa_link("Hello " + C.COMPANY + ", I would like to book " + t["name"])}" '
        f'target="_blank" rel="noopener">{WHATSAPP_ICON}<span>Book on WhatsApp</span></a>'
        '<div class="note">Your booking request opens in WhatsApp with the trip, date and number of travellers already filled in. '
        'Prices are per person, based on twin sharing. We confirm availability and the final price before any payment.</div>'
        '</div></div></div></section>')

    sec.insert_after(frag(itinerary + included + reviews_section(out_rel, t["slug"]) + calc))
    soup.head.append(frag(trip_jsonld(out_rel, t)))
    soup.body.append(frag(f'<script src="{rel(out_rel, "assets/js/lavigo-trip.js")}"></script>'))
    build_gallery(soup, out_rel)
    return soup


def child_note(t):
    if t["price_child"]:
        return f"per adult · children {money(t['price_child'])}"
    return f"per person · adults only ({t.get('min_age', 12)}+)"


def stars(n):
    return "★" * int(n) + "☆" * (5 - int(n))


def reviews_section(out_rel, trip_slug=None):
    R = C.REVIEWS
    items = [r for r in R["items"] if not trip_slug or r.get("trip") == trip_slug]
    if not items:
        return ""
    cards = []
    for r in items:
        if r.get("photo"):
            avatar = f'<span class="av" style="background-image:url(&quot;{rel(out_rel, img_path(r["photo"]))}&quot;);"></span>'
        else:
            initials = "".join(w[0] for w in re.findall(r"[A-Za-z]+", r["name"])[:2]).upper() or "•"
            avatar = f'<span class="av">{html.escape(initials)}</span>'
        trip = next((t for t in C.TRIPS if t["slug"] == r.get("trip")), None)
        trip_line = (f'<a href="{rel(out_rel, PAGES["trip:" + trip["slug"]])}">{html.escape(trip["name"])}</a>' if trip else "")
        cards.append(
            f'<div class="lavigo-review"><div class="stars" aria-label="{r["rating"]} out of 5">{stars(r["rating"])}</div>'
            f'<div class="q">{html.escape(r["text"])}</div>'
            f'<div class="who">{avatar}<span><b>{html.escape(r["name"])}</b><small>{html.escape(r["place"])}'
            f'{" &middot; " + trip_line if trip_line else ""}</small></span></div></div>')
    google = ""
    if C.SITE.get("google_reviews") and C.SITE["google_reviews"] != "#":
        google = (f'<div class="center-holder top-margin-2"><a class="lavigo-wa-btn lavigo-btn-outline" style="display:inline-flex;" '
                  f'href="{html.escape(C.SITE["google_reviews"])}" target="_blank" rel="noopener"><span>{html.escape(R["google_text"])}</span></a></div>')
    return (f'<section class="lavigo-section" id="section-reviews"><div class="centered-midwide">'
            f'{section_heading(R["small"], R["title"])}<div class="lavigo-reviews">{"".join(cards)}</div>{google}</div></section>')


def trip_jsonld(out_rel, t):
    """Structured data so Google understands the trip page (name, itinerary, price)."""
    data = {
        "@context": "https://schema.org", "@type": "TouristTrip", "name": t["name"], "description": t["tagline"],
        "touristType": "Leisure",
        "itinerary": {"@type": "ItemList", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": f"Day {i + 1}: {title}"} for i, (title, _) in enumerate(t["itinerary"])]},
        "offers": {"@type": "Offer", "price": t["price_adult"], "priceCurrency": "INR",
                   "availability": "https://schema.org/InStock"},
        "provider": {"@type": "TravelAgency", "name": C.COMPANY},
    }
    if site_url():
        data["url"] = site_url() + "/" + PAGES["trip:" + t["slug"]].replace("index.html", "")
        data["image"] = site_url() + "/" + img_path(t["hero"])
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False) + "</script>"


def page_about(base, out_rel):
    A = C.ABOUT
    soup = load_as(base, "discover-the-destination/land-of-lakes/index.html", out_rel)
    chrome(soup, out_rel, "About us", A["card_text"], A["hero"])
    detail_intro(soup, out_rel, A["hero"], "index.html", "About us", A["title"], A["intro"])
    sec = fill_places(soup, out_rel, A["blocks"])
    cta = (f'<section class="lavigo-section bg-color-lightgreen"><div class="centered-midwide center-holder">'
           f'{section_heading("Ready to go?", "Travel with " + C.COMPANY)}'
           f'<div class="t-base" style="max-width:36em;margin:0 auto;">Browse our trips with fixed departure dates, or tell us '
           f'what you dream of and we will build a journey for you.</div>'
           f'<div class="flexbox center gap-2 top-margin-2 column-mobile">'
           f'<a class="lavigo-wa-btn" style="margin-top:0;" href="{rel(out_rel, PAGES["trips"])}"><span>See our trips</span></a>'
           f'<a class="lavigo-wa-btn" style="margin-top:0;" href="{wa_link("Hello " + C.COMPANY + "!")}" target="_blank" '
           f'rel="noopener">{WHATSAPP_ICON}<span>Chat on WhatsApp</span></a></div></div></section>')
    sec.insert_after(frag(cta))
    build_gallery(soup, out_rel)
    return soup


def page_blog(base, out_rel, b):
    soup = load(os.path.join(base, "blog/the-scandinature-festival/index.html"))
    chrome(soup, out_rel, b["title"], b["excerpt"], b["image"])
    intro = soup.select_one("#section-intro")
    for t in bg_tags(intro):
        set_bg(t, rel(out_rel, img_path(b["image"])))
    for c in captions(intro):
        set_text(c, credit(b["image"]))
    art = soup.select_one("#section-article")
    set_text(art.select_one(".t-title-1"), b["title"])
    rc = art.select_one(".rich-content")
    gallery_tpl = copy.copy(rc.select_one("figure.wp-block-gallery"))
    fig_tpl = copy.copy(gallery_tpl.select_one("figure.wp-block-image"))
    spacer = copy.copy(rc.select_one(".wp-block-spacer"))
    rc.clear()
    rc.append(frag(f'<p class="wp-block-paragraph"><strong>{html.escape(b["lead"])}</strong></p>'))
    if spacer:
        rc.append(spacer)
    for heading, paras, imgs in b["sections"]:
        rc.append(frag(f'<h2 class="wp-block-heading"><br/>{html.escape(heading)}</h2>'))
        for p in paras:
            rc.append(frag(f'<p class="wp-block-paragraph">{html.escape(p)}</p>'))
        if imgs:
            g = copy.copy(gallery_tpl)
            g.clear()
            for k in imgs:
                f = copy.copy(fig_tpl)
                im = f.find("img")
                for a in ("srcset", "sizes", "data-id", "class", "fetchpriority"):
                    im.attrs.pop(a, None)
                im["src"] = rel(out_rel, img_path(k))
                im["alt"] = CREDITS.get(k, {}).get("article", "")
                im["width"], im["height"] = CREDITS[k]["width"], CREDITS[k]["height"]
                im["loading"] = "lazy"
                set_text(f.find("figcaption"), credit(k))
                g.append(f)
            rc.append(g)
    return soup


def page_contact(base, out_rel):
    P = C.CONTACT_PAGE
    soup = load(os.path.join(base, "contact/index.html"))
    chrome(soup, out_rel, "Contact", P["text"], P["image"], dark_logo=True)
    intro = soup.select_one("#section-intro")
    for t in intro.select(".t-title-1"):
        set_text(t, P["line1"])
    for t in intro.select(".t-title-2"):
        set_text(t, P["line2"])
    for t in bg_tags(intro):
        if "submit_img" in t["style"]:
            set_bg(t, rel(out_rel, img_path(P["hours_image"])))
        else:
            set_bg(t, rel(out_rel, img_path(P["image"])))
    welcome = intro.find(string=re.compile("We welcome"))
    box = welcome.parent
    links = box.select_one(".inline-block")
    tel, mail = links.find_all("a")
    tel["href"] = C.CONTACT["phone_link"]
    set_text(tel.select_one(".bold"), C.CONTACT["phone"])
    mail["href"] = C.CONTACT["email_link"]
    set_text(mail.select_one(".bold"), C.CONTACT["email"])
    links.extract()
    box.clear()
    box.append(NavigableString(" " + P["text"] + " "))
    box.append(soup.new_tag("br"))
    box.append(soup.new_tag("br"))
    box.append(links)
    for s in intro.find_all(string=re.compile("I agree to receive")):
        s.replace_with(P["consent"])
    for sel in intro.find_all("select"):
        first = sel.find("option")
        for o in sel.find_all("option")[1:]:
            o.decompose()
        for country in C.CONTACT_PAGE["countries"]:
            o = soup.new_tag("option", value=country)
            o.string = country
            sel.append(o)
        _ = first
    for s in intro.find_all(string=re.compile(r"^\s*Merci\s*$")):
        s.replace_with("Thank you")
    # opening hours
    hc = soup.select_one("#section-half-circles")
    h2 = hc.find("h2")
    hd = h2.find_all("div")
    set_text(hd[0], P["hours_title"][0])
    set_text(hd[1], P["hours_title"][1])
    set_text(hc.select_one(".t-base"), P["hours_text"])
    rc = hc.select_one(".rich-content")
    rc.clear()
    rc.append(frag("<p>" + "<br/>".join(html.escape(x) for x in C.CONTACT["address_lines"]) + "</p>"))
    for day, hours in C.CONTACT["hours"]:
        rc.append(frag(f"<p>{html.escape(day)}<br/><strong>{html.escape(hours)}</strong></p>"))
    for t in bg_tags(hc):
        set_bg(t, rel(out_rel, img_path(P["hours_image"])))
    return soup


def page_legal(base, out_rel):
    soup = load(os.path.join(base, "legal-notice/index.html"))
    chrome(soup, out_rel, "Legal notice", f"Legal notice and photo credits of the {C.COMPANY} website.", "lachen-thangu")
    for t in bg_tags(soup.select_one("#section-intro")):
        set_bg(t, rel(out_rel, img_path("lachen-thangu")))
    rc = soup.select_one("#section-simple .rich-content")
    K = C.CONTACT
    site = C.COMPANY
    blocks = [
        ("1. Website publisher", [
            f"<strong>Company:</strong> {K['legal_name']}",
            f"<strong>Address:</strong> {', '.join(K['address_lines'])}",
            f"<strong>Registration:</strong> {K['registration']}",
            f"<strong>Phone:</strong> {K['phone']} &ndash; <strong>Email:</strong> {K['email']}",
            f"<strong>Publication manager:</strong> {K['director']}",
            f"<strong>Hosting provider:</strong> {K['host']}",
        ]),
        ("2. Terms of use", [
            f"By using the {site} website you accept these terms of use. They may be updated at any time, so please consult them regularly.",
            f"The information on this website is provided for guidance only. {site} does its best to keep it accurate and up to date, "
            "but travel conditions, opening times, permits and access rules in the Himalayas can change at short notice. "
            "Please check the details of your journey with our team before you travel.",
        ]),
        ("3. Intellectual property", [
            f"The texts, logo and design elements of this website are the property of {site} or are used with permission. "
            "Any reproduction without prior written permission is prohibited.",
            "The photographs are published under free licences (Creative Commons or public domain) by the authors listed below.",
        ]),
        ("4. Personal data", [
            f"Information you send us through the contact or newsletter forms is used only to answer your request and, "
            f"if you agree, to send you news from {site}. It is never sold to third parties. "
            f"You can ask to access, correct or delete your data at any time by writing to {K['email']}.",
        ]),
    ]
    out = []
    for h, ps in blocks:
        out.append(f'<h2 class="wp-block-heading">{html.escape(h)}</h2>')
        out += [f'<p class="wp-block-paragraph">{p}</p>' for p in ps]
    out.append('<h2 class="wp-block-heading" id="photo-credits">5. Photo credits</h2>')
    out.append('<p class="wp-block-paragraph">Photos from Wikimedia Commons, used under the licences shown. '
               'Click a name to see the original file and its licence.</p>')
    items = []
    for k in sorted(CREDITS):
        c = CREDITS[k]
        items.append(f'<li><a href="{html.escape(c["source"])}" target="_blank" rel="noopener">{html.escape(credit_title(k))}</a> '
                     f'&ndash; {html.escape(credit(k))} &ndash; {html.escape(c["license"])}</li>')
    out.append('<ul class="wp-block-list">' + "".join(items) + "</ul>")
    out.append('<p class="wp-block-paragraph">Map data: geoBoundaries (CC BY 4.0) and Natural Earth (public domain).</p>')
    rc.clear()
    rc.append(frag("".join(out)))
    title = soup.select_one("#section-intro .t-title-1")
    if title:
        title.clear()
        title.append(frag("Legal <br/>notice<br/>"))
    return soup


# ---------------------------------------------------------------- assets
def copy_assets(base, out):
    for sub in ("css", "js", "theme"):
        shutil.copytree(os.path.join(base, "assets", sub), os.path.join(out, "assets", sub))
    for dirpath, _, files in os.walk(os.path.join(out, "assets", "css")):
        for fn in files:
            fp = os.path.join(dirpath, fn)
            css = open(fp, encoding="utf-8").read()
            fixed = css.replace("https://tourisme-sumene-artense.com/wp-content/themes/otsa/img/btn_dropdown.svg",
                                "../theme/img/picto_dropdown.svg")
            if fixed != css:
                open(fp, "w", encoding="utf-8", newline="\n").write(fixed)
    os.makedirs(os.path.join(out, "assets", "images"))
    for f in os.listdir(os.path.join(CONTENT_DIR, "images")):
        if f.endswith(".jpg"):
            shutil.copyfile(os.path.join(CONTENT_DIR, "images", f), os.path.join(out, "assets", "images", f))
    shutil.copytree(os.path.join(CONTENT_DIR, "brand"), os.path.join(out, "assets", "brand"))
    shutil.copyfile(os.path.join(CONTENT_DIR, "extras", "lavigo.css"), os.path.join(out, "assets", "css", "lavigo.css"))
    shutil.copyfile(os.path.join(CONTENT_DIR, "extras", "lavigo-trip.js"), os.path.join(out, "assets", "js", "lavigo-trip.js"))
    shutil.copyfile(os.path.join(CONTENT_DIR, "extras", "lavigo-custom.js"), os.path.join(out, "assets", "js", "lavigo-custom.js"))


def copy_referenced_uploads(base, out):
    """Copy the few original upload files still referenced (none expected), and report them."""
    left = set()
    for dirpath, _, files in os.walk(out):
        for fn in files:
            if fn.endswith(".html"):
                s = open(os.path.join(dirpath, fn), encoding="utf-8").read()
                for m in re.finditer(r"""(?:src|href)=["']([^"']*assets/uploads/[^"']+)|url\(['"]?([^'")]*assets/uploads/[^'")]+)""", s):
                    u = unquote((m.group(1) or m.group(2)).split("#")[0].split("?")[0])
                    left.add(os.path.normpath(os.path.join(dirpath, u)))
    for p in left:
        r = os.path.relpath(p, out)
        src = os.path.join(base, r)
        if os.path.isfile(src):
            os.makedirs(os.path.dirname(p), exist_ok=True)
            shutil.copyfile(src, p)
    return sorted(os.path.relpath(p, out) for p in left)


def write(soup, out, out_rel):
    path = os.path.join(out, out_rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = str(soup)
    text = re.sub(r"/\*# sourceURL=[^*]*\*/", "", text)
    text = re.sub(r"//# sourceURL=\S+", "", text)
    if "tourisme-sumene-artense" in text or "Sumène" in text:
        print("WARNING: old-site reference left in", out_rel)
    if not text.lstrip().lower().startswith("<!doctype"):
        text = "<!DOCTYPE html>" + text
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def main():
    if len(sys.argv) >= 3:
        base, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
        tmp = None
    else:
        tmp = tempfile.mkdtemp(prefix="lavigo-base-")
        base, out = os.path.join(tmp, "base"), os.path.join(ROOT, "site")
        subprocess.run([sys.executable, os.path.join(ROOT, "build_site.py"), os.path.join(ROOT, "original-scrape"), base],
                       check=True)
    os.makedirs(out, exist_ok=True)
    for entry in os.listdir(out):
        p = os.path.join(out, entry)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)

    copy_assets(base, out)
    write(page_home(base, PAGES["home"], skip_intro=False), out, PAGES["home"])
    write(page_home(base, PAGES["home_skip"], skip_intro=True), out, PAGES["home_skip"])
    write(page_destinations(base, PAGES["destinations"]), out, PAGES["destinations"])
    for d in C.DESTINATIONS:
        write(page_destination(base, PAGES["dest:" + d["slug"]], d), out, PAGES["dest:" + d["slug"]])
    for b in C.BLOG:
        write(page_blog(base, PAGES["blog:" + b["slug"]], b), out, PAGES["blog:" + b["slug"]])
    write(page_trips(base, PAGES["trips"]), out, PAGES["trips"])
    for t in C.TRIPS:
        write(page_trip(base, PAGES["trip:" + t["slug"]], t), out, PAGES["trip:" + t["slug"]])
    write(page_about(base, PAGES["about"]), out, PAGES["about"])
    write(page_contact(base, PAGES["contact"]), out, PAGES["contact"])
    write(page_legal(base, PAGES["legal"]), out, PAGES["legal"])
    write_sitemap(out)
    leftovers = copy_referenced_uploads(base, out)
    print(f"Built {len(PAGES)} pages into {out}")
    if leftovers:
        print("Original images still referenced:", *leftovers, sep="\n  ")
    if tmp:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
