#!/usr/bin/env python3
"""
Конвертация документации Markdown → DOCX по ГОСТ 7.32-2017 и ГОСТ Р 7.0.97-2016.

Оформление:
- шрифт Times New Roman, 14 пт (основной текст);
- межстрочный интервал 1,5;
- абзацный отступ 1,25 см;
- поля: левое 30 мм, правое 15 мм, верхнее и нижнее 20 мм;
- выравнивание основного текста по ширине;
- нумерация страниц — внизу по центру.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Mm, Pt, RGBColor

DOCS_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = DOCS_DIR / "docx"

# ГОСТ: основные параметры
FONT_NAME = "Times New Roman"
FONT_SIZE = Pt(14)
FONT_SIZE_H1 = Pt(16)
FONT_SIZE_H2 = Pt(14)
FONT_SIZE_H3 = Pt(14)
FONT_SIZE_CODE = Pt(12)
LINE_SPACING = 1.5
INDENT = Cm(1.25)

MD_FILES = [
    "ЗАДАНИЕ_КП.md",
    "ПОЯСНИТЕЛЬНАЯ_ЗАПИСКА.md",
    "API_SPECIFICATION.md",
    "ER_DIAGRAM.md",
    "ARCHITECTURE.md",
    "JWT_AUTH_DESIGN.md",
    "WEBSOCKET_SETUP.md",
    "TESTING_REPORT.md",
    "USER_GUIDE.md",
    "DOMAIN_MODEL.md",
    "USE_CASE.md",
]


def set_gost_page_setup(doc: Document) -> None:
    section = doc.sections[0]
    section.page_height = Mm(297)
    section.page_width = Mm(210)
    section.left_margin = Mm(30)
    section.right_margin = Mm(15)
    section.top_margin = Mm(20)
    section.bottom_margin = Mm(20)


def add_page_number_footer(doc: Document) -> None:
    section = doc.sections[0]
    footer = section.footer
    paragraph = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = paragraph.add_run()
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = "PAGE"
    fld_sep = OxmlElement("w:fldChar")
    fld_sep.set(qn("w:fldCharType"), "separate")
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_sep)
    run._r.append(fld_end)
    run.font.name = FONT_NAME
    run.font.size = FONT_SIZE


def format_paragraph(paragraph, *, bold: bool = False, center: bool = False, indent: bool = True, code: bool = False) -> None:
    fmt = paragraph.paragraph_format
    fmt.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    fmt.line_spacing = LINE_SPACING
    fmt.space_after = Pt(0)
    fmt.space_before = Pt(0)
    if center:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fmt.first_line_indent = Cm(0)
    elif code:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        fmt.first_line_indent = Cm(0)
        fmt.left_indent = Cm(0.5)
    else:
        paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        fmt.first_line_indent = INDENT if indent else Cm(0)

    for run in paragraph.runs:
        run.font.name = FONT_NAME
        run.font.size = FONT_SIZE_CODE if code else FONT_SIZE
        run.font.bold = bold
        run._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_NAME)


def add_run_with_inline(paragraph, text: str, *, bold: bool = False, code: bool = False) -> None:
    pattern = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`|\[[^\]]+\]\([^)]+\))")
    pos = 0
    for match in pattern.finditer(text):
        if match.start() > pos:
            run = paragraph.add_run(text[pos:match.start()])
            run.font.name = FONT_NAME
            run.font.size = FONT_SIZE_CODE if code else FONT_SIZE
            run.font.bold = bold
        chunk = match.group(0)
        if chunk.startswith("**"):
            run = paragraph.add_run(chunk[2:-2])
            run.font.bold = True
            run.font.name = FONT_NAME
            run.font.size = FONT_SIZE
        elif chunk.startswith("`"):
            run = paragraph.add_run(chunk[1:-1])
            run.font.name = "Courier New"
            run.font.size = FONT_SIZE_CODE
        elif chunk.startswith("["):
            link = re.match(r"\[([^\]]+)\]\(([^)]+)\)", chunk)
            if link:
                label, url = link.groups()
                run = paragraph.add_run(f"{label} ({url})")
                run.font.name = FONT_NAME
                run.font.size = FONT_SIZE
        pos = match.end()
    if pos < len(text):
        run = paragraph.add_run(text[pos:])
        run.font.name = FONT_NAME
        run.font.size = FONT_SIZE_CODE if code else FONT_SIZE
        run.font.bold = bold


def add_heading(doc: Document, text: str, level: int) -> None:
    p = doc.add_paragraph()
    add_run_with_inline(p, text, bold=True)
    if level == 1:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for run in p.runs:
            run.font.size = FONT_SIZE_H1
        p.paragraph_format.first_line_indent = Cm(0)
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        for run in p.runs:
            run.font.size = FONT_SIZE_H2 if level == 2 else FONT_SIZE_H3
        p.paragraph_format.first_line_indent = Cm(0)
    format_paragraph(p, indent=False)


def add_body(doc: Document, text: str, *, indent: bool = True) -> None:
    if not text.strip():
        return
    p = doc.add_paragraph()
    add_run_with_inline(p, text.strip())
    format_paragraph(p, indent=indent)


def add_code_block(doc: Document, lines: list[str]) -> None:
    note = doc.add_paragraph()
    run = note.add_run("Листинг (схема в нотации Mermaid/текстовый фрагмент):")
    run.font.name = FONT_NAME
    run.font.size = FONT_SIZE
    run.font.italic = True
    format_paragraph(note, indent=True)

    for line in lines:
        p = doc.add_paragraph()
        run = p.add_run(line.rstrip("\n"))
        run.font.name = "Courier New"
        run.font.size = FONT_SIZE_CODE
        run.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
        format_paragraph(p, code=True)


def parse_table_row(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [cell.strip() for cell in line.split("|")]


def is_table_separator(line: str) -> bool:
    return bool(re.match(r"^\|?[\s\-:|]+\|?$", line.strip()))


def add_table(doc: Document, rows: list[list[str]]) -> None:
    if not rows:
        return
    cols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=cols)
    table.style = "Table Grid"
    for i, row in enumerate(rows):
        for j in range(cols):
            cell = table.rows[i].cells[j]
            text = row[j] if j < len(row) else ""
            cell.text = ""
            p = cell.paragraphs[0]
            run = p.add_run(text)
            run.font.name = FONT_NAME
            run.font.size = Pt(12)
            run.font.bold = i == 0
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i == 0 else WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.line_spacing_rule = WD_LINE_SPACING.SINGLE
    doc.add_paragraph()


def add_gost_title_page(doc: Document, title: str) -> None:
    lines = [
        "МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ",
        "Федеральное государственное автономное образовательное учреждение",
        "высшего образования",
        "«СЕВЕРО-КАВКАЗСКИЙ ФЕДЕРАЛЬНЫЙ УНИВЕРСИТЕТ»",
        "Институт перспективной инженерии",
        "Кафедра межинститутская базовая",
    ]
    for line in lines:
        p = doc.add_paragraph(line)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_paragraph(p, center=True, indent=False)

    doc.add_paragraph()
    doc.add_paragraph()

    p = doc.add_paragraph(title.upper())
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for run in p.runs:
        run.font.bold = True
        run.font.size = FONT_SIZE_H1
    format_paragraph(p, center=True, indent=False)

    doc.add_paragraph()
    p = doc.add_paragraph("по дисциплине «Технология разработки программного обеспечения»")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_paragraph(p, center=True, indent=False)

    doc.add_paragraph()
    doc.add_paragraph()
    doc.add_paragraph()

    info = [
        "Направление подготовки: 09.03.04 «Программная инженерия»",
        "Направленность: «Разработка и сопровождение программного обеспечения»",
        "",
        "Тема: Интернет-магазин свечей ручной работы «Candels»",
        "Траектория: В (Django REST + React + JWT + WebSocket)",
        "",
        "Выполнил: студент группы ПИЖ-б-о-24-1",
        "Рашевский Р.Р.",
        "",
        "Руководитель: к.т.н. Самойлов Ф.В.",
        "",
        "",
        "Ставрополь — 2026",
    ]
    for line in info:
        p = doc.add_paragraph(line)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        format_paragraph(p, indent=False)

    doc.add_page_break()


def convert_md_to_docx(md_path: Path, docx_path: Path, *, with_title: bool = False, title: str = "") -> None:
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()

    doc = Document()
    set_gost_page_setup(doc)
    add_page_number_footer(doc)

    if with_title:
        add_gost_title_page(doc, title or md_path.stem.replace("_", " "))

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        if stripped == "---":
            i += 1
            continue

        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            i += 1
            block: list[str] = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            if lang == "mermaid" and block:
                add_body(doc, "Диаграмма (нотация Mermaid; для просмотра см. исходный файл .md):", indent=True)
            add_code_block(doc, block)
            i += 1
            continue

        if stripped.startswith("#"):
            level = len(stripped) - len(stripped.lstrip("#"))
            heading = stripped[level:].strip()
            add_heading(doc, heading, min(level, 3))
            i += 1
            continue

        if stripped.startswith("|") and i + 1 < len(lines) and is_table_separator(lines[i + 1]):
            table_rows = [parse_table_row(stripped)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_rows.append(parse_table_row(lines[i]))
                i += 1
            add_table(doc, table_rows)
            continue

        if stripped.startswith("- ") or stripped.startswith("* "):
            items = []
            while i < len(lines) and (lines[i].strip().startswith("- ") or lines[i].strip().startswith("* ") or (lines[i].startswith("  ") and lines[i].strip())):
                items.append(lines[i].strip().lstrip("-* ").strip())
                i += 1
            for item in items:
                p = doc.add_paragraph(style="List Bullet")
                add_run_with_inline(p, item)
                format_paragraph(p, indent=False)
                p.paragraph_format.left_indent = INDENT
            continue

        if re.match(r"^\d+\.\s", stripped):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s*", "", lines[i].strip()))
                i += 1
            for item in items:
                p = doc.add_paragraph(style="List Number")
                add_run_with_inline(p, item)
                format_paragraph(p, indent=False)
                p.paragraph_format.left_indent = INDENT
            continue

        para_lines = [stripped]
        i += 1
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt or nxt.startswith("#") or nxt == "---" or nxt.startswith("```") or nxt.startswith("|") or nxt.startswith("- ") or re.match(r"^\d+\.\s", nxt):
                break
            para_lines.append(nxt)
            i += 1
        add_body(doc, " ".join(para_lines))

    docx_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(docx_path)
    print(f"  OK: {docx_path.name}")


def main() -> int:
    try:
        import docx  # noqa: F401
    except ImportError:
        print("Установите зависимость: pip install python-docx", file=sys.stderr)
        return 1

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"GOST 7.32-2017 / GOST R 7.0.97-2016 -> {OUTPUT_DIR}")

    titles = {
        "ПОЯСНИТЕЛЬНАЯ_ЗАПИСКА.md": "Пояснительная записка",
        "ЗАДАНИЕ_КП.md": "Задание на курсовой проект",
    }

    for name in MD_FILES:
        md_path = DOCS_DIR / name
        if not md_path.exists():
            print(f"  SKIP (нет файла): {name}")
            continue
        docx_name = md_path.stem + ".docx"
        convert_md_to_docx(
            md_path,
            OUTPUT_DIR / docx_name,
            with_title=name in titles,
            title=titles.get(name, ""),
        )

    print(f"\nСоздано файлов: {len(list(OUTPUT_DIR.glob('*.docx')))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
