#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
aurelion_menu.py
Menú interactivo para navegar la Documentacion.md del proyecto Aurelion.
- Navegación con flechas (InquirerPy) y renderizado bonito con rich.
- Si faltan dependencias, el script muestra instrucciones y cae a un menú numérico simple.
- Colocar este archivo en la misma carpeta que Documentacion.md y ejecutar: python aurelion_menu.py
"""

from __future__ import annotations
import os
import re
import sys
from typing import List, Tuple, Dict

# Intentaremos usar InquirerPy y rich. Si no están instalados, avisamos.
USE_INQUIRER = True
USE_RICH = True
try:
    from InquirerPy import inquirer
except Exception:
    USE_INQUIRER = False

try:
    from rich.console import Console
    from rich.markdown import Markdown
    from rich.panel import Panel
    from rich.text import Text
except Exception:
    USE_RICH = False

# Nombre por defecto del archivo Markdown
MD_FILENAME = "Documentacion.md"

console = Console() if USE_RICH else None

def leer_documentacion(path: str) -> str | None:
    if not os.path.exists(path):
        print(f"❗ No se encontró '{path}' en el directorio actual: {os.getcwd()}")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def dividir_sprints(md: str) -> Tuple[str, str]:
    """
Divide el documento en sprint1 y sprint2.
Considera sprint2 a partir de la línea que contiene 'Documentación - Sprint 2' (case-insensitive).
"""
    patron = re.compile(r'(?mi)^#\s*documentaci[oó]n.*sprint\s*2', re.IGNORECASE)
    m = patron.search(md)
    if not m:
        # Si no encuentra, lo deja todo en sprint1 y sprint2 vacío
        return md, ""
    idx = m.start()
    sprint1 = md[:idx].strip()
    sprint2 = md[idx:].strip()
    return sprint1, sprint2

def extraer_secciones_sprint1(md: str) -> List[Tuple[str, str]]:
    """Extrae secciones numeradas del Sprint 1 (encabezados que empiezan con '## 1.' '## 2.' etc.).
    Retorna lista de (titulo, contenido)
    """
    # Normalizar saltos
    lines = md.splitlines()
    text = "\n".join(lines)
    # Buscaremos encabezados del tipo '## 1.' o '## 1 ' o '## 1)'
    patron = re.compile(r'(?m)^(##\s*\d+\..*)$')
    matches = list(patron.finditer(text))
    sections = []
    if not matches:
        # Si no hay secciones numeradas, intenta tomar todo como una sección
        title = "Sprint 1 - Contenido"
        sections.append((title, text.strip()))
        return sections
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        content = text[start:end].strip()
        # Limpiar prefijo "## N." para mostrar solo nombre legible
        title_clean = re.sub(r'^##\s*\d+\.\s*', '', title).strip()
        sections.append((title_clean or title, (title + "\n\n" + content).strip()))
    return sections

def extraer_fases_sprint2(md: str) -> List[Tuple[str, str]]:
    """Extrae las fases del Sprint 2 buscando encabezados que contengan 'Fase' seguido por número o palabra.\n    Retorna lista de (titulo, contenido)\n    """

    text = md
    # Buscamos encabezados que contengan 'Fase' (pueden ser '## Fase 1:' o '## Fase 1' o '### Fase 1')
    patron = re.compile(r'(?m)^(##+\s*Fase\s*\d+.*)$', re.IGNORECASE)
    matches = list(patron.finditer(text))
    sections = []
    if not matches:
        # Si no hay fases, intentar partir por '## ' (encabezados de segundo nivel)
        patron2 = re.compile(r'(?m)^(##\s+.+)$')
        matches2 = list(patron2.finditer(text))
        if not matches2:
            sections.append(("Sprint 2 - Contenido", text.strip()))
            return sections
        for i, m in enumerate(matches2):
            title = m.group(1).strip()
            start = m.end()
            end = matches2[i+1].start() if i+1 < len(matches2) else len(text)
            content = text[start:end].strip()
            title_clean = re.sub(r'^##\s*', '', title).strip()
            sections.append((title_clean, (title + "\n\n" + content).strip()))
        return sections
    for i, m in enumerate(matches):
        title = m.group(1).strip()
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        content = text[start:end].strip()
        # Limpiar prefijo '## Fase X:'
        title_clean = re.sub(r'^(##+\s*)', '', title).strip()
        sections.append((title_clean, (title + "\n\n" + content).strip()))
    return sections

def mostrar_markdown(text: str):
    """Muestra markdown con rich si está disponible, sino imprime plano."""
    if USE_RICH and console:
        md = Markdown(text)
        console.print(md)
    else:
        print(text)

def resumenes_preparados() -> Dict[str, str]:
    """Devuelve resúmenes redactados para cada Sprint."""
    r = {}
    r['Sprint 1'] = (
        "En Sprint 1 se realiza la preparación y estructuración inicial de los datos: "
        "carga de archivos, limpieza básica, normalización y diseño del visor de documentación. "
        "Incluye la definición del dataset, estructura de tablas y pasos para que el usuario pueda "
        "consultar la documentación desde la terminal."
    )
    r['Sprint 2'] = (
        "Sprint 2 se enfoca en el análisis estadístico descriptivo de ventas: corrección de categorías, "
        "análisis por segmentos, detección de outliers, generación de visualizaciones y exportación "
        "de resultados ejecutables (CSV y gráficos)."
    )
    return r

# Función principal del menú usando InquirerPy
def menu_con_inquirer(s1_sections: List[Tuple[str,str]], s2_sections: List[Tuple[str,str]]):
    while True:
        # Menú principal con descripciones
        resumen = resumenes_preparados()
        choices = [
            {"name": "Sprint 1 - Análisis inicial y preparación de datos", "value": "sprint1", "short": "Sprint 1"},
            {"name": "Sprint 2 - Análisis estadístico descriptivo de ventas", "value": "sprint2", "short": "Sprint 2"},
            {"name": "Ver todo el documento", "value": "ver_todo", "short": "Ver todo"},
            {"name": "Salir", "value": "salir", "short": "Salir"}
        ]
        answer = inquirer.select(
            message="📘 Documentación del proyecto — usa ↑/↓ y ENTER para seleccionar:",
            choices=choices,
            default="sprint1",
            qmark="►",
            amark="•"
        ).execute()
        if answer == "salir":
            print("👋 Saliendo. ¡Hasta luego!")
            sys.exit(0)
        elif answer == "ver_todo":
            # Mostrar todo concatenado
            full = s1_text + "\n\n---\n\n" + s2_text if s2_text else s1_text
            mostrar_markdown(full)
            input("\nPresiona ENTER para volver al menú principal...")
            continue
        elif answer == "sprint1":
            # Submenu para sprint1
            submenu_sections = s1_sections
            keys = [f"{i+1}. {titulo}" for i,(titulo,_) in enumerate(submenu_sections)]
            keys.append("⬅ Volver")
            chosen = inquirer.select(
                message="Sprint 1 — Elige sección:",
                choices=keys,
                qmark="►",
                amark="•"
            ).execute()
            if chosen == "⬅ Volver":
                continue
            # extraer índice
            idx = keys.index(chosen)
            title, content = submenu_sections[idx]
            # Mostrar con título destacado
            header = f"# {title}\\n\\n"
            mostrar_markdown(header + content)
            input("\\nPresiona ENTER para volver al menú de Sprint 1...")
            continue
        elif answer == "sprint2":
            submenu_sections = s2_sections
            keys = [f"{i+1}. {titulo}" for i,(titulo,_) in enumerate(submenu_sections)]
            keys.append("⬅ Volver")
            chosen = inquirer.select(
                message="Sprint 2 — Elige fase:",
                choices=keys,
                qmark="►",
                amark="•"
            ).execute()
            if chosen == "⬅ Volver":
                continue
            idx = keys.index(chosen)
            title, content = submenu_sections[idx]
            header = f"# {title}\\n\\n"
            mostrar_markdown(header + content)
            input("\\nPresiona ENTER para volver al menú de Sprint 2...")
            continue

def menu_simple(s1_sections: List[Tuple[str,str]], s2_sections: List[Tuple[str,str]]):
    """Menú por consola numérico simple (fallback si no se instalan dependencias)."""
    while True:
        print("\\n=== Documentación del Proyecto Aurelion ===")
        print("1) Sprint 1 - Análisis inicial y preparación de datos")
        print("2) Sprint 2 - Análisis estadístico descriptivo de ventas")
        print("3) Ver todo el documento")
        print("0) Salir")
        opc = input("Elige una opción: ").strip()
        if opc == "0":
            print("Saliendo...")
            break
        if opc == "3":
            full = s1_text + "\\n\\n---\\n\\n" + s2_text if s2_text else s1_text
            print(full)
            input("\\nEnter para continuar...")
            continue
        if opc == "1":
            print("\\nSprint 1 - Secciones disponibles:")
            for i, (t,_) in enumerate(s1_sections):
                print(f"{i+1}) {t}")
            sel = input("Elige sección (número) o 'v' para volver: ").strip()
            if sel.lower() == "v":
                continue
            try:
                idx = int(sel)-1
                print("\\n" + s1_sections[idx][1])
            except Exception:
                print("Selección inválida.")
            input("\\nEnter para continuar...")
            continue
        if opc == "2":
            print("\\nSprint 2 - Fases disponibles:")
            for i, (t,_) in enumerate(s2_sections):
                print(f"{i+1}) {t}")
            sel = input("Elige fase (número) o 'v' para volver: ").strip()
            if sel.lower() == "v":
                continue
            try:
                idx = int(sel)-1
                print("\\n" + s2_sections[idx][1])
            except Exception:
                print("Selección inválida.")
            input("\\nEnter para continuar...")
            continue
        print("Opción inválida. Intenta de nuevo.")

def main():
    global s1_text, s2_text
    md = leer_documentacion(MD_FILENAME)
    if md is None:
        print("Asegúrate de que Documentacion.md esté en la misma carpeta que este script.")
        sys.exit(1)
    s1_text, s2_text = dividir_sprints(md)
    s1_sections = extraer_secciones_sprint1(s1_text)
    s2_sections = extraer_fases_sprint2(s2_text)
    # Mostrar resúmenes en el menú principal
    if USE_INQUIRER:
        try:
            menu_con_inquirer(s1_sections, s2_sections)
            return
        except Exception as e:
            print("Error con InquirerPy durante la ejecución del menú interactivo:", e)
            print("Caeremos al menú simple (numérico)." )
    # Fallback
    menu_simple(s1_sections, s2_sections)

if __name__ == '__main__':
    # Mostrar aviso de dependencias si faltan
    missing = []
    if not USE_INQUIRER:
        missing.append("InquirerPy")
    if not USE_RICH:
        missing.append("rich")
    if missing:
        print("Nota: faltan las siguientes dependencias que mejoran la experiencia:", ", ".join(missing))
        print("Puedes instalarlas con:\\n    pip install InquirerPy rich\\n")
        print("El programa seguirá funcionando en modo simple.\\n")
    main()
