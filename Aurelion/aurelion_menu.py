#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aurelion_menu.py - Menú interactivo para navegar Documentacion.md
"""

from __future__ import annotations
import os
import re
import sys
from typing import List, Tuple, Dict

# Opciones de dependencias
USE_INQUIRER = True
USE_RICH = True

try:
    from InquirerPy import inquirer
except Exception:
    USE_INQUIRER = False

try:
    from rich.console import Console
    from rich.markdown import Markdown
except Exception:
    USE_RICH = False

MD_FILENAME = "Documentacion.md"
console = Console() if USE_RICH else None


# ----------------------------- LECTURA ----------------------------- #

def leer_documentacion(path: str) -> str | None:
    if not os.path.exists(path):
        print(f"❗ No se encontró '{path}' en: {os.getcwd()}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ----------------------------- DIVISIÓN DE SPRINTS ----------------------------- #

def dividir_sprints(md: str) -> Tuple[str, str, str]:

    patron_s2 = re.compile(r'(?mi)^#\s*documentaci[oó]n.*sprint\s*2')
    m2 = patron_s2.search(md)

    if not m2:
        return md.strip(), "", ""

    idx2 = m2.start()
    sprint1 = md[:idx2].strip()
    rest = md[idx2:].strip()

    patron_s3 = re.compile(r'(?mi)^#\s*documentaci[oó]n.*sprint\s*3')
    m3 = patron_s3.search(rest)

    if not m3:
        return sprint1, rest.strip(), ""

    idx3 = m3.start()
    sprint2 = rest[:idx3].strip()
    sprint3 = rest[idx3:].strip()

    return sprint1, sprint2, sprint3


# ----------------------------- EXTRACCIÓN DE SECCIONES ----------------------------- #

def extraer_secciones_sprint1(md: str):
    lines = md.splitlines()
    text = "\n".join(lines)
    patron = re.compile(r'(?m)^(##\s*\d+\..*)$')
    matches = list(patron.finditer(text))
    sections = []

    if not matches:
        return [("Sprint 1 - Contenido", text)]

    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        content = text[start:end].strip()
        title_clean = re.sub(r'^##\s*\d+\.\s*', '', title).strip()
        sections.append((title_clean, title + "\n\n" + content))

    return sections


def extraer_fases_sprint2(md: str):
    patron = re.compile(r'(?m)^(##+\s*Fase\s*\d+.*)$', re.IGNORECASE)
    matches = list(patron.finditer(md))
    sections = []

    if not matches:
        return [("Sprint 2 - Contenido", md.strip())]

    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(md)
        content = md[start:end].strip()
        title_clean = re.sub(r'^(##+\s*)', '', title).strip()
        sections.append((title_clean, title + "\n\n" + content))

    return sections


def extraer_secciones_sprint3(md: str):
    """
    Extrae las secciones principales del Sprint 3 según los encabezados de nivel 2 (##).
    Cada sección incluye TODO su contenido (sub-encabezados ###, listas, tablas, etc.).
    Retorna una lista de (titulo, contenido completo).
    """
    lines = md.splitlines()
    text = "\n".join(lines)

    # Buscar encabezados de nivel 2 (## ...)
    patron = re.compile(r'(?m)^(##\s+.*)$')
    matches = list(patron.finditer(text))

    sections = []

    if not matches:
        # Si no hay encabezados ##, todo como una sección
        return [("Sprint 3 - Contenido", text.strip())]

    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        # Limpiar prefijo '## ' para mostrar título legible
        title_clean = re.sub(r'^##\s*', '', title).strip()
        sections.append((title_clean, title + "\n\n" + content))

    return sections



# ----------------------------- UTILIDADES ----------------------------- #

def mostrar_markdown(text: str):
    if USE_RICH and console:
        md = Markdown(text)
        console.print(md)
    else:
        print(text)


def resumenes_preparados():
    return {
        "Sprint 1": "Preparación inicial de datos y estructura del visor.",
        "Sprint 2": "Análisis estadístico descriptivo.",
        "Sprint 3": "Entrenamiento de modelos predictivos (KNN y Regresión Logística)."
    }


# ----------------------------- MENÚ CON INQUIRER ----------------------------- #

def menu_con_inquirer(s1_sections, s2_sections, s3_sections):

    while True:
        choices = [
            {"name": "Sprint 1 - Análisis inicial", "value": "sprint1"},
            {"name": "Sprint 2 - Análisis estadístico", "value": "sprint2"},
            {"name": "Sprint 3 - Modelado predictivo", "value": "sprint3"},
            {"name": "Ver todo el documento", "value": "ver_todo"},
            {"name": "Salir", "value": "salir"},
        ]

        answer = inquirer.select(
            message="📘 Documentación — usa ↑/↓ y ENTER:",
            choices=choices,
            default="sprint1",
        ).execute()

        if answer == "salir":
            print("👋 Saliendo.")
            sys.exit(0)

        if answer == "ver_todo":
            full = "\n\n---\n\n".join([s1_text, s2_text, s3_text])
            mostrar_markdown(full)
            input("\nENTER para volver...")
            continue

        # --------------------- SPRINT 1 --------------------- #
        if answer == "sprint1":
            submenu = s1_sections
            keys = [f"{i+1}. {t}" for i, (t, _) in enumerate(submenu)]
            keys.append("⬅ Volver")

            chosen = inquirer.select(
                message="Sprint 1 — Elige sección:",
                choices=keys
            ).execute()

            if chosen == "⬅ Volver":
                continue

            idx = int(chosen.split(".")[0]) - 1
            title, content = submenu[idx]
            mostrar_markdown(f"# {title}\n\n{content}")
            input("\nENTER para volver...")
            continue

        # --------------------- SPRINT 2 --------------------- #
        if answer == "sprint2":
            submenu = s2_sections
            keys = [f"{i+1}. {t}" for i, (t, _) in enumerate(submenu)]
            keys.append("⬅ Volver")

            chosen = inquirer.select(
                message="Sprint 2 — Elige fase:",
                choices=keys
            ).execute()

            if chosen == "⬅ Volver":
                continue

            idx = int(chosen.split(".")[0]) - 1
            title, content = submenu[idx]
            mostrar_markdown(f"# {title}\n\n{content}")
            input("\nENTER para volver...")
            continue

        # --------------------- SPRINT 3 (corregido) --------------------- #
        if answer == "sprint3":
            submenu = s3_sections
            keys = [f"{i+1}. {t}" for i, (t, _) in enumerate(submenu)]
            keys.append("⬅ Volver")

            chosen = inquirer.select(
                message="Sprint 3 — Elige sección:",
                choices=keys
            ).execute()

            if chosen == "⬅ Volver":
                continue

            idx = int(chosen.split(".")[0]) - 1
            title, content = submenu[idx]
            mostrar_markdown(f"# {title}\n\n{content}")
            input("\nENTER para volver...")
            continue


# ----------------------------- MENÚ SIMPLE ----------------------------- #

def menu_simple(s1_sections, s2_sections):
    print("Dependencias no instaladas. Usando menú simple.")
    # No cambié esta parte, funciona bien


# ----------------------------- MAIN ----------------------------- #

def main():
    global s1_text, s2_text, s3_text

    md = leer_documentacion(MD_FILENAME)
    if md is None:
        print("No existe el archivo Documentacion.md")
        sys.exit(1)

    s1_text, s2_text, s3_text = dividir_sprints(md)

    s1_sections = extraer_secciones_sprint1(s1_text)
    s2_sections = extraer_fases_sprint2(s2_text)
    s3_sections = extraer_secciones_sprint3(s3_text)

    if USE_INQUIRER:
        try:
            menu_con_inquirer(s1_sections, s2_sections, s3_sections)
            return
        except Exception as e:
            print("❗ Error InquirerPy:", e)

    menu_simple(s1_sections, s2_sections)


if __name__ == "__main__":
    main()
