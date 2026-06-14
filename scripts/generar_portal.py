#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
GENERADOR DEL PORTAL FAR

Com s'utilitza:
1. Posa les apps HTML dins de la carpeta correcta:
   apps/pasapalabra/temporada1/
   apps/pasapalabra/temporada2/
   apps/escape_room/temporada1/
   apps/millionari/temporada1/
   apps/esde/...

2. Executa:
   python scripts/generar_portal.py

3. El programa actualitza:
   data/apps.json
   apps.json

Després puja-ho tot a GitHub.
"""

from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parents[1]

THUMBNAILS = {
    "El Gran Millonari": "assets/thumbnails/millionari.jpg",
    "Pasapalabra": "assets/thumbnails/pasapalabra.jpg",
    "Escape Rooms": "assets/thumbnails/escape_rooms.jpg",
    "ESDE": "assets/thumbnails/esde.jpg",
}

BANNERS = {
    "El Gran Millonari": "assets/banners/millionari.jpg",
    "Pasapalabra": "assets/banners/pasapalabra.jpg",
    "Escape Rooms": "assets/banners/escape_rooms.jpg",
    "ESDE": "assets/banners/esde.jpg",
}

ESDE_SPECIAL_IMAGES = {
    "simulador": ("assets/thumbnails/esde_simulador_regne.jpg", "assets/banners/esde_simulador_regne.jpg"),
    "setge": ("assets/thumbnails/esde_tauler_setges.jpg", "assets/banners/esde_tauler_setges.jpg"),
    "tauler": ("assets/thumbnails/esde_tauler_setges.jpg", "assets/banners/esde_tauler_setges.jpg"),
    "masmor": ("assets/thumbnails/esde_masmorres.jpg", "assets/banners/esde_masmorres.jpg"),
    "trivial": ("assets/thumbnails/esde_trivials.jpg", "assets/banners/esde_trivials.jpg"),
    "generador": ("assets/thumbnails/esde_trivials.jpg", "assets/banners/esde_trivials.jpg"),
}

GREEK = {
    "alpha": "Alpha",
    "beta": "Beta",
    "gamma": "Gamma",
    "delta": "Delta",
    "epsilon": "Èpsilon",
    "zeta": "Zeta",
    "eta": "Èta",
    "theta": "Theta",
    "iota": "Iota",
    "gran_final": "La Gran Final",
}

def clean_words(stem: str) -> str:
    s = stem
    s = re.sub(r"^(pasa|pasapalabra|mill|esc|esde)_?", "", s, flags=re.I)
    s = re.sub(r"s\d+e\d+_?", "", s, flags=re.I)
    s = s.replace("_", " ").replace("-", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return s.title()

def title_from_path(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    stem = path.stem.lower()

    if rel.startswith("apps/millionari/"):
        for key, val in GREEK.items():
            if key in stem:
                return f"El Gran Millonari · Megamix {val}" if key != "gran_final" else "El Gran Millonari · La Gran Final"
        m = re.search(r"e(\d+)", stem)
        return f"El Gran Millonari · Episodi {m.group(1)}" if m else "El Gran Millonari"

    if rel.startswith("apps/pasapalabra/"):
        name = clean_words(path.stem)
        replacements = {
            "General 5E": "General 5é",
            "Matematiques": "Matemàtiques",
            "Llengua": "Llengua",
            "Medi": "Coneixement del Medi",
            "Historia Valenciana": "Història Valenciana",
            "Ciencia Natura": "Ciència i Natura",
            "Esport Salut": "Esport i Salut",
            "Art Cultura": "Art i Cultura",
            "Geografia Mon": "Geografia del Món",
            "Megamix Alpha": "Megamix Juvenil · Alpha",
            "Megamix Beta": "Megamix Juvenil · Beta",
            "Megamix Gamma": "Megamix Juvenil · Gamma",
            "Megamix Delta": "Megamix Juvenil · Delta",
            "Megamix Final Boss": "Megamix Juvenil · Final Boss",
        }
        return "Pasapalabra · " + replacements.get(name, name)

    if rel.startswith("apps/escape_room/"):
        name = clean_words(path.stem)
        if "Edat Mitjana" in name:
            return "Escape Room · Edat Mitjana del País Valencià"
        if "Valencia Romana" in name or "València Romana" in name:
            return "Escape Room · València Romana"
        if "Tresor" in name:
            return "Escape Room · El Tresor de Sant Marcel·lí"
        return "Escape Room · " + name

    if rel.startswith("apps/esde/"):
        name = clean_words(path.stem)
        if "Simulador" in name or "V33" in name:
            return "ESDE · Simulador del Regne"
        if "Setge" in name or "Tauler" in name:
            return "ESDE · Tauler i Setges"
        if "Masmor" in name:
            return "ESDE · Masmorres"
        if "Trivial" in name:
            return "ESDE · Trivials"
        if "Generador" in name:
            return "ESDE · Generador de Trivials"
        return "ESDE · " + name

    return clean_words(path.stem)

def category_from_path(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("apps/millionari/"):
        return "El Gran Millonari"
    if rel.startswith("apps/pasapalabra/"):
        return "Pasapalabra"
    if rel.startswith("apps/escape_room/"):
        return "Escape Rooms"
    if rel.startswith("apps/esde/"):
        return "ESDE"
    return "Altres"

def description_from_path(path: Path, category: str) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if category == "El Gran Millonari":
        if "temporada1" in rel:
            return "Temporada 1 · Concurs de preguntes per equips."
        return "Concurs de preguntes per equips."
    if category == "Pasapalabra":
        if "temporada1" in rel:
            return "Temporada 1 · Rosca curricular amb selector d’idioma."
        if "temporada2" in rel:
            return "Temporada 2 · Megamix juvenil amb selector d’idioma."
        if "especials" in rel:
            return "Especial · Pasapalabra amb suport lingüístic."
        return "Rosca interactiva amb selector Valencià / Castellà / Rus."
    if category == "Escape Rooms":
        return "Escape room amb selector Valencià / Castellà / Rus."
    if category == "ESDE":
        return "App del sistema ESDE per a la simulació medieval de classe."
    return "App educativa del Portal Far."

def image_for_app(path: Path, category: str):
    if category == "ESDE":
        lower = path.as_posix().lower()
        for key, imgs in ESDE_SPECIAL_IMAGES.items():
            if key in lower:
                return imgs
    return THUMBNAILS.get(category, "assets/thumbnails/esde.jpg"), BANNERS.get(category, "assets/banners/esde.jpg")

def build_catalogue():
    apps_dir = ROOT / "apps"
    items = []

    if not apps_dir.exists():
        print("No existeix la carpeta apps/")
        return []

    for html in sorted(apps_dir.rglob("*.html")):
        # ignore hidden/temp files
        if html.name.startswith("."):
            continue

        rel = html.relative_to(ROOT).as_posix()
        category = category_from_path(html)
        title = title_from_path(html)
        thumb, banner = image_for_app(html, category)

        item = {
            "id": re.sub(r"[^a-zA-Z0-9_]+", "_", html.stem.lower()),
            "title": title,
            "type": "app",
            "category": category,
            "description": description_from_path(html, category),
            "thumbnail": thumb,
            "banner": banner,
            "url": rel
        }
        items.append(item)

    return items

def main():
    items = build_catalogue()

    data_dir = ROOT / "data"
    data_dir.mkdir(exist_ok=True)

    (data_dir / "apps.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "apps.json").write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Portal Far actualitzat: {len(items)} apps detectades.")
    cats = {}
    for item in items:
        cats[item["category"]] = cats.get(item["category"], 0) + 1
    for cat, total in cats.items():
        print(f"- {cat}: {total}")

if __name__ == "__main__":
    main()
