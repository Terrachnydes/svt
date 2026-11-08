#!/usr/bin/env python3
"""Régénère la page récap « Mes sites SVT ».

Usage : python3 _recap/build_hub.py [fichier.html ...]
  - Refait la capture (aperçu) des fichiers passés en argument, et de ceux
    qui n'ont pas encore d'aperçu dans _recap/apercus/.
  - Reconstruit _recap/mes-sites.html à partir de tpl.html + sites.json.
"""
import asyncio, base64, json, os, re, subprocess, sys, unicodedata
from datetime import datetime
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
APERCUS = os.path.join(HERE, "apercus")


def slug(f):
    s = unicodedata.normalize("NFD", f[:-5]).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


def three_dir():
    """three.js en local (le CDN n'est pas joignable depuis l'environnement)."""
    d = "/tmp/recap-npm"
    p = os.path.join(d, "node_modules/three/")
    if not os.path.exists(p):
        os.makedirs(d, exist_ok=True)
        subprocess.run(["npm", "i", "-s", "--prefix", d, "three@0.147.0"], check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return p if os.path.exists(p) else None


async def captures(fichiers):
    from playwright.async_api import async_playwright
    from PIL import Image
    t3 = three_dir()
    async with async_playwright() as p:
        chrome = "/usr/bin/google-chrome" if os.path.exists("/usr/bin/google-chrome") else None
        b = await p.chromium.launch(executable_path=chrome,
                                    args=["--use-gl=swiftshader", "--enable-webgl", "--ignore-gpu-blocklist"])
        for f in fichiers:
            pg = await b.new_page(viewport={"width": 1280, "height": 800}, color_scheme="light")
            if t3:
                async def h(route, t3=t3):
                    u = route.request.url
                    rel = "build/three.min.js" if "three.min.js" in u else "examples/js/controls/OrbitControls.js"
                    await route.fulfill(path=t3 + rel, content_type="application/javascript")
                await pg.route("**/three@*/**", h)
            try:
                await pg.goto("file://" + os.path.join(REPO, f), timeout=60000)
                await pg.wait_for_timeout(8000)
                tmp = "/tmp/recap-shot.png"
                await pg.screenshot(path=tmp)
                Image.open(tmp).convert("RGB").resize((520, 325), Image.LANCZOS).save(
                    os.path.join(APERCUS, slug(f) + ".webp"), "WEBP", quality=68)
                print("aperçu ok :", f)
            except Exception as e:
                print("aperçu ÉCHEC :", f, e)
            await pg.close()
        await b.close()


def main():
    os.makedirs(APERCUS, exist_ok=True)
    cfg = json.load(open(os.path.join(HERE, "sites.json"), encoding="utf-8"))
    a_faire = set(a for a in sys.argv[1:] if a.endswith(".html"))
    for s in cfg["sites"]:
        if not os.path.exists(os.path.join(APERCUS, slug(s["fichier"]) + ".webp")):
            a_faire.add(s["fichier"])
    if a_faire:
        asyncio.run(captures(sorted(a_faire)))

    if sys.argv[1:]:
        cfg["derniere_maj"] = datetime.now(ZoneInfo("Europe/Paris")).strftime("%Y-%m-%d")
        json.dump(cfg, open(os.path.join(HERE, "sites.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    data = []
    for th in cfg["themes"]:
        items = []
        for s in cfg["sites"]:
            if s["theme"] != th:
                continue
            ap = os.path.join(APERCUS, slug(s["fichier"]) + ".webp")
            img = ("data:image/webp;base64," + base64.b64encode(open(ap, "rb").read()).decode()) if os.path.exists(ap) else None
            items.append({"t": s["titre"], "f": s["fichier"], "c": s["artifact"], "img": img})
        if items:
            data.append([th, items])
    d = cfg["derniere_maj"].split("-")
    tpl = open(os.path.join(HERE, "tpl.html"), encoding="utf-8").read()
    out = tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False)).replace("__MAJ__", f"{d[2]}/{d[1]}/{d[0]}")
    open(os.path.join(HERE, "mes-sites.html"), "w", encoding="utf-8").write(out)
    print("page récap régénérée :", sum(len(i) for _, i in data), "sites")


if __name__ == "__main__":
    main()
