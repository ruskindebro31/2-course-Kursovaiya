#!/usr/bin/env python3
"""Markdown → DOCX по ГОСТ (только пояснительная записка)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Mm, Pt, RGBColor

DOCS = Path(__file__).resolve().parent
MD_PATH = DOCS / "ПОЯСНИТЕЛЬНАЯ_ЗАПИСКА.md"
OUT_PATH = DOCS / "docx" / "ПОЯСНИТЕЛЬНАЯ_ЗАПИСКА.docx"

FONT = "Times New Roman"
SIZE = Pt(14)
SIZE_H1 = Pt(16)
SIZE_CODE = Pt(12)
INDENT = Cm(1.25)


def setup_page(doc: Document) -> None:
    s = doc.sections[0]
    s.page_height = Mm(297)
    s.page_width = Mm(210)
    s.left_margin = Mm(30)
    s.right_margin = Mm(10)
    s.top_margin = Mm(20)
    s.bottom_margin = Mm(20)


def add_page_numbers(doc: Document) -> None:
    footer = doc.sections[0].footer
    p = footer.paragraphs[0] if footer.paragraphs else footer.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run()
    for el in _field_elements("PAGE"):
        run._r.append(el)
    run.font.name = FONT
    run.font.size = SIZE


def _field_elements(instr: str) -> list:
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    text = OxmlElement("w:instrText")
    text.set(qn("xml:space"), "preserve")
    text.text = instr
    sep = OxmlElement("w:fldChar")
    sep.set(qn("w:fldCharType"), "separate")
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    return [begin, text, sep, end]


def fmt_para(p, *, center=False, indent=True, code=False) -> None:
    f = p.paragraph_format
    f.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    f.line_spacing = 1.5
    f.space_before = Pt(0)
    f.space_after = Pt(0)
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        f.first_line_indent = Cm(0)
    elif code:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        f.first_line_indent = Cm(0)
        f.left_indent = Cm(0.5)
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        f.first_line_indent = INDENT if indent else Cm(0)
    for r in p.runs:
        r.font.name = FONT
        r.font.size = SIZE_CODE if code else SIZE
        r._element.rPr.rFonts.set(qn("w:eastAsia"), FONT)


def add_text(p, text: str, *, bold=False, code=False) -> None:
    for part in re.split(r"(\*\*[^*]+\*\*|`[^`]+`)", text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            r = p.add_run(part[2:-2])
            r.bold = True
        elif part.startswith("`") and part.endswith("`"):
            r = p.add_run(part[1:-1])
            r.font.name = "Courier New"
            r.font.size = SIZE_CODE
        else:
            r = p.add_run(part)
            r.bold = bold
        r.font.name = FONT if not (part.startswith("`")) else "Courier New"
        if not part.startswith("`"):
            r.font.size = SIZE_CODE if code else SIZE


def title_page(doc: Document) -> None:
    for line in [
        "МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ",
        "Федеральное государственное автономное образовательное учреждение",
        "высшего образования",
        "«СЕВЕРО-КАВКАЗСКИЙ ФЕДЕРАЛЬНЫЙ УНИВЕРСИТЕТ»",
        "Институт перспективной инженерии",
        "Кафедра межинститутская базовая",
    ]:
        p = doc.add_paragraph(line)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        fmt_para(p, center=True, indent=False)

    doc.add_paragraph()
    doc.add_paragraph()
    p = doc.add_paragraph("ПОЯСНИТЕЛЬНАЯ ЗАПИСКА")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in p.runs:
        r.bold = True
        r.font.size = SIZE_H1
    fmt_para(p, center=True, indent=False)

    doc.add_paragraph()
    for line in [
        "по дисциплине «Технология разработки программного обеспечения»",
        "",
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
    ]:
        p = doc.add_paragraph(line)
        fmt_para(p, indent=False)

    doc.add_page_break()


def is_major(heading: str) -> bool:
    h = heading.strip().upper()
    if h in {"СОДЕРЖАНИЕ", "ВВЕДЕНИЕ", "ЗАКЛЮЧЕНИЕ"}:
        return True
    if h.startswith("СПИСОК ИСПОЛЬЗОВАННЫХ"):
        return True
    if h.startswith("ПРИЛОЖЕНИЕ"):
        return True
    return bool(re.match(r"^\d+\.\s", heading))


def add_heading(doc: Document, text: str, level: int) -> None:
    p = doc.add_paragraph()
    add_text(p, text, bold=True)
    if level == 1:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        for r in p.runs:
            r.font.size = SIZE_H1
    fmt_para(p, indent=False)


def parse_row(line: str) -> list[str]:
    line = line.strip().strip("|")
    return [c.strip() for c in line.split("|")]


def add_table(doc: Document, rows: list[list[str]]) -> None:
    cols = max(len(r) for r in rows)
    t = doc.add_table(rows=len(rows), cols=cols)
    t.style = "Table Grid"
    for i, row in enumerate(rows):
        for j in range(cols):
            cell = t.rows[i].cells[j]
            cell.text = ""
            p = cell.paragraphs[0]
            r = p.add_run(row[j] if j < len(row) else "")
            r.font.name = FONT
            r.font.size = Pt(12)
            r.bold = i == 0
    doc.add_paragraph()


def convert(md_path: Path, out_path: Path) -> None:
    lines = md_path.read_text(encoding="utf-8").splitlines()
    doc = Document()
    setup_page(doc)
    add_page_numbers(doc)
    title_page(doc)

    i = 0
    while i < len(lines):
        line = lines[i]
        s = line.strip()

        if not s or s == "---":
            i += 1
            continue

        if s.startswith("```"):
            i += 1
            block = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                block.append(lines[i])
                i += 1
            p = doc.add_paragraph()
            add_text(p, "Листинг:")
            fmt_para(p, indent=True)
            for ln in block:
                cp = doc.add_paragraph()
                r = cp.add_run(ln)
                r.font.name = "Courier New"
                r.font.size = SIZE_CODE
                r.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
                fmt_para(cp, code=True)
            i += 1
            continue

        if s.startswith("#"):
            lvl = len(s) - len(s.lstrip("#"))
            head = s[lvl:].strip()
            if lvl == 1 and head.upper() == "ПОЯСНИТЕЛЬНАЯ ЗАПИСКА":
                i += 1
                continue
            if lvl == 2 and is_major(head):
                doc.add_page_break()
            add_heading(doc, head, min(lvl, 3))
            i += 1
            continue

        if s.startswith("|") and i + 1 < len(lines) and re.match(r"^\|?[\s\-:|]+\|?$", lines[i + 1]):
            rows = [parse_row(s)]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(parse_row(lines[i]))
                i += 1
            add_table(doc, rows)
            continue

        if s.startswith(("- ", "* ")):
            items = []
            while i < len(lines) and lines[i].strip().startswith(("- ", "* ")):
                items.append(lines[i].strip()[2:])
                i += 1
            for item in items:
                p = doc.add_paragraph(style="List Bullet")
                add_text(p, item)
                fmt_para(p, indent=False)
                p.paragraph_format.left_indent = INDENT
            continue

        if re.match(r"^\d+\.\s", s):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s*", "", lines[i].strip()))
                i += 1
            for item in items:
                p = doc.add_paragraph(style="List Number")
                add_text(p, item)
                fmt_para(p, indent=False)
                p.paragraph_format.left_indent = INDENT
            continue

        parts = [s]
        i += 1
        while i < len(lines):
            n = lines[i].strip()
            if not n or n.startswith("#") or n == "---" or n.startswith("```") or n.startswith("|"):
                break
            if n.startswith(("- ", "* ")) or re.match(r"^\d+\.\s", n):
                break
            parts.append(n)
            i += 1
        p = doc.add_paragraph()
        add_text(p, " ".join(parts))
        fmt_para(p)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(out_path)


def main() -> int:
    if not MD_PATH.exists():
        print("Сначала: python docs/build_full_report.py", file=sys.stderr)
        return 1
    convert(MD_PATH, OUT_PATH)
    # проверка: файл открывается без ошибок
    Document(OUT_PATH)
    print(f"OK: {OUT_PATH} ({OUT_PATH.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
