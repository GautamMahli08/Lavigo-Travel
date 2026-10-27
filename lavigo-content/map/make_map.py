"""Generate the LAVIGO travel map (same visual language as the original tourist map) and the context mini-map.

Usage: python make_map.py <geo_dir> <out_dir>
Writes: travel-map.svg, context-country.svg, context-region.svg, context-region-zoom.svg, map.json (pointer positions)
"""
import json
import math
import os
import sys

from shapely.geometry import shape, mapping, Point, LineString, MultiLineString, Polygon, MultiPolygon, box
from shapely.ops import unary_union, transform

GEO, OUT = sys.argv[1], sys.argv[2]
os.makedirs(OUT, exist_ok=True)


def load(name):
    return json.load(open(os.path.join(GEO, name), encoding="utf-8"))["features"]


adm1 = {f["properties"]["shapeName"]: shape(f["geometry"]) for f in load("IND-ADM1.geojson")}
adm2 = {f["properties"]["shapeName"]: shape(f["geometry"]) for f in load("IND-ADM2.geojson")}
nepal = unary_union([shape(f["geometry"]) for f in load("NPL-ADM0.geojson")])
india = unary_union([shape(f["geometry"]) for f in load("IND-ADM0.geojson")])
bhutan = unary_union([shape(f["geometry"]) for f in load("BTN-ADM0.geojson")])

regions = {
    "Himachal Pradesh": adm1["Himāchal Pradesh"],
    "Uttarakhand": adm1["Uttarākhand"],
    "Nepal": nepal,
    "Sikkim": adm1["Sikkim"],
    "Darjeeling": unary_union([adm2["Darjiling"], adm2["Kalimpong"]]),
    "Bhutan": bhutan,
}
regions = {k: v.buffer(0) for k, v in regions.items()}
union = unary_union(list(regions.values())).buffer(0.01).buffer(-0.01)

# ---------------------------------------------------------------- projection: equirectangular + fisheye on Sikkim
LAT0 = 29.5
KX = math.cos(math.radians(LAT0))
CENTER = (88.5, 27.4)  # between Darjeeling, Pelling, Gangtok and Lachen
FISH_D = 4.5
FISH_R = 8.5  # degrees (projected units) - beyond this radius the map is unchanged


def eq(lon, lat):
    return ((lon - CENTER[0]) * KX, -(lat - CENTER[1]))


def fish(x, y):
    r = math.hypot(x, y)
    if r == 0 or r >= FISH_R:
        return x, y
    t = r / FISH_R
    t2 = (FISH_D + 1) * t / (FISH_D * t + 1)
    s = t2 * FISH_R / r
    return x * s, y * s


def proj(lon, lat):
    return fish(*eq(lon, lat))


def proj_geom(g):
    return transform(lambda xs, ys, zs=None: tuple(zip(*[proj(x, y) for x, y in zip(xs, ys)])), densify(g))


def densify(g, step=0.05):
    """Add vertices so the non-linear fisheye bends long straight edges."""
    def dl(coords):
        out = []
        for (x1, y1), (x2, y2) in zip(coords[:-1], coords[1:]):
            n = max(1, int(math.hypot(x2 - x1, y2 - y1) / step))
            out += [(x1 + (x2 - x1) * i / n, y1 + (y2 - y1) * i / n) for i in range(n)]
        out.append(coords[-1])
        return out

    if isinstance(g, Polygon):
        return Polygon(dl(list(g.exterior.coords)), [dl(list(i.coords)) for i in g.interiors])
    if isinstance(g, MultiPolygon):
        return MultiPolygon([densify(p, step) for p in g.geoms])
    if isinstance(g, LineString):
        return LineString(dl(list(g.coords)))
    if isinstance(g, MultiLineString):
        return MultiLineString([densify(p, step) for p in g.geoms])
    return g


P = {k: proj_geom(v).simplify(0.004) for k, v in regions.items()}
PU = proj_geom(union).simplify(0.004)

# view box with margin
minx, miny, maxx, maxy = PU.bounds
pad = 0.07 * (maxx - minx)
minx, miny, maxx, maxy = minx - pad, miny - pad * 1.6, maxx + pad, maxy + pad * 1.6
W = 600.0
SC = W / (maxx - minx)
H = round((maxy - miny) * SC, 1)


def xy(x, y):
    return (x - minx) * SC, (y - miny) * SC


def path_d(g):
    parts = []

    def ring(coords):
        pts = [xy(x, y) for x, y in coords]
        return "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"

    def line(coords):
        pts = [xy(x, y) for x, y in coords]
        return "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

    geoms = getattr(g, "geoms", [g])
    for gg in geoms:
        if isinstance(gg, Polygon):
            parts.append(ring(gg.exterior.coords))
            parts += [ring(i.coords) for i in gg.interiors]
        elif isinstance(gg, LineString):
            parts.append(line(gg.coords))
    return "".join(parts)


svg = [f'<svg viewBox="0 0 {W:.0f} {H:.0f}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet" '
       'style="fill-rule:evenodd;clip-rule:evenodd;stroke-miterlimit:10;stroke-linejoin:round;">']
# topographic-style contour rings around the region
for i, dist in enumerate([0.12, 0.26, 0.42, 0.6, 0.8, 1.02, 1.26]):
    ringg = PU.buffer(dist, resolution=24).simplify(0.01)
    svg.append(f'<path d="{path_d(ringg.exterior if hasattr(ringg, "exterior") else ringg)}" '
               'style="fill:none;stroke:#dfe2de;stroke-width:0.5px;"/>')
svg.append(f'<path d="{path_d(PU)}" style="fill:none;stroke:#2d540e;stroke-opacity:0.08;stroke-width:40px;"/>')
svg.append(f'<path d="{path_d(PU)}" style="fill:#fff;stroke:#2d540e;stroke-width:1px;"/>')

# rivers (clipped to the region)
rivers = load("rivers.geojson")
keep = {"Beas", "Sutlej", "Ganges", "Yamuna", "Gandak", "Ghäghara", "Sapt", "Tista", "Ravi", "Chenab"}
rv = []
for f in rivers:
    if (f["properties"].get("name") or "") in keep:
        g = shape(f["geometry"]).intersection(union.buffer(-0.02))
        if not g.is_empty:
            rv.append(proj_geom(g).simplify(0.004))
for g in rv:
    svg.append(f'<path d="{path_d(g)}" style="fill:none;stroke:#aab2dd;stroke-width:1px;stroke-linecap:round;"/>')

# internal borders (dashed, like the original commune borders)
borders = []
names = list(P)
for i, a in enumerate(names):
    for b in names[i + 1:]:
        inter = P[a].buffer(0.003).intersection(P[b].buffer(0.003))
        if not inter.is_empty:
            borders.append(inter.boundary if False else None)
for k, g in P.items():
    svg.append(f'<path d="{path_d(g)}" style="fill:none;stroke:#2d540e;stroke-width:0.6px;stroke-dasharray:2,2;"/>')
svg.append(f'<path d="{path_d(PU)}" style="fill:none;stroke:#2d540e;stroke-width:1px;"/>')
svg.append("</svg>")
open(os.path.join(OUT, "travel-map.svg"), "w", encoding="utf-8").write("".join(svg))


def pct(lon, lat):
    x, y = xy(*proj(lon, lat))
    return round(100 * x / W, 2), round(100 * y / H, 2)


# region labels and small town dots
towns = {
    "Shimla": (77.17, 31.10), "Dharamshala": (76.32, 32.22), "Rishikesh": (78.27, 30.09),
    "Nainital": (79.46, 29.38), "Kathmandu": (85.32, 27.71), "Pokhara": (83.99, 28.21),
    "Lukla": (86.73, 27.69), "Pelling": (88.10, 27.30), "Kalimpong": (88.47, 27.06),
    "Siliguri": (88.40, 26.73), "Mangan": (88.53, 27.51), "Lachung": (88.745, 27.69),
    "Paro": (89.41, 27.43), "Punakha": (89.86, 27.58),
}
pointers = {
    "nepal": (85.32, 27.71), "gangtok": (88.63, 27.33), "darjeeling": (88.33, 27.02),
    "manali": (77.19, 32.24), "lachen-and-lachung": (88.556, 27.72),
    "pelling": (88.02, 27.36), "bhutan": (89.64, 27.47), "everest-base-camp": (86.85, 28.0),
}
labels = {"Himachal Pradesh": (77.6, 31.6), "Uttarakhand": (79.2, 30.3), "Nepal": (84.0, 28.4)}
meta = {
    "viewBox": [W, H],
    "towns": {k: pct(*v) for k, v in towns.items()},
    "pointers": {k: pct(*v) for k, v in pointers.items()},
    "labels": {k: pct(*v) for k, v in labels.items()},
}

# ---------------------------------------------------------------- context mini-map (India + Nepal, region highlighted)
CK = math.cos(math.radians(22))


def cproj(g):
    return transform(lambda xs, ys, zs=None: (tuple((x - 68) * CK for x in xs), tuple(-(y - 37.5) for y in ys)), g)


country = cproj(unary_union([india, nepal, bhutan]).buffer(0.05).buffer(-0.05)).simplify(0.06)
cminx, cminy, cmaxx, cmaxy = country.bounds
CW = 112.0
csc = CW / (cmaxx - cminx)
CH = round((cmaxy - cminy) * csc, 1)


def cd(g, ox, oy, sc):
    out = []
    for gg in getattr(g, "geoms", [g]):
        if isinstance(gg, Polygon):
            for r in [gg.exterior] + list(gg.interiors):
                out.append("M" + "L".join(f"{(x - ox) * sc:.2f},{(y - oy) * sc:.2f}" for x, y in r.coords) + "Z")
    return "".join(out)


open(os.path.join(OUT, "context-country.svg"), "w", encoding="utf-8").write(
    f'<svg viewBox="0 0 {CW:.0f} {CH:.0f}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">'
    f'<path fill="#fff" fill-opacity="0.35" d="{cd(country, cminx, cminy, csc)}"/></svg>')

reg = cproj(union).simplify(0.01)
rminx, rminy, rmaxx, rmaxy = reg.bounds
RW = 226.0
rsc = RW / (rmaxx - rminx)
RH = round((rmaxy - rminy) * rsc, 1)
rd = cd(reg, rminx, rminy, rsc)
open(os.path.join(OUT, "context-region.svg"), "w", encoding="utf-8").write(
    f'<svg viewBox="0 0 {RW:.0f} {RH:.0f}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">'
    f'<path fill="#fff" d="{rd}"/></svg>')
open(os.path.join(OUT, "context-region-zoom.svg"), "w", encoding="utf-8").write(
    f'<svg viewBox="0 0 {RW:.0f} {RH:.0f}" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet">'
    f'<path d="{rd}" style="fill:none;stroke:#fff;stroke-width:1.5px;"/></svg>')

# placement of the region inside the country box (centre, % of the box) and its height relative to the box
side = max(CW, CH)  # the original places the country svg inside a square box, fit to height
cx = ((rminx + rmaxx) / 2 - cminx) * csc
cy = ((rminy + rmaxy) / 2 - cminy) * csc
meta["context"] = {
    "country_viewBox": [CW, CH],
    "region_center_pct": [round(100 * (cx + (side - CW) / 2) / side, 2), round(100 * (cy + (side - CH) / 2) / side, 2)],
    "region_height_pct": round(100 * (rmaxy - rminy) * csc / side, 2),
    "region_aspect": round(RW / RH, 3),
    # dots shown when zoomed in (relative to the region svg box, %)
    "zoom_dots": {
        name: [round(100 * ((lon - 68) * CK - rminx) * rsc / RW, 1), round(100 * (-(lat - 37.5) - rminy) * rsc / RH, 1)]
        for name, (lon, lat) in {"Manali": (77.19, 32.24), "Kathmandu": (85.32, 27.71), "Gangtok": (88.61, 27.33), "Thimphu": (89.64, 27.47)}.items()
    },
}
json.dump(meta, open(os.path.join(OUT, "map.json"), "w", encoding="utf-8"), indent=1)
print(json.dumps(meta, indent=1))
