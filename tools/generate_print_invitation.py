#!/usr/bin/env python3
"""Generate the static A4 print edition of Nastya's invitation."""

from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image
from reportlab.graphics import renderPDF
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_CLEAN = ROOT / "output" / "pdf" / "nastya-bachelorette-invitation-a4.pdf"
OUTPUT_WITH_QR = ROOT / "output" / "pdf" / "nastya-bachelorette-invitation-a4-with-qr.pdf"
TMP = ROOT / "tmp" / "pdfs"
FONT = ROOT / "assets" / "fonts" / "Gabin-Regular.ttf"
SOURCE_ART = ROOT / "assets" / "bride-in-glass-nastya-v7-natural.png"
MASKED_ART = TMP / "bride-in-glass-print-masked.png"
SITE_URL = "https://nikolasjirovski-collab.github.io/bachelorette-invitation/"

PAPER = (240 / 255, 172 / 255, 178 / 255)
WINE = (116 / 255, 24 / 255, 46 / 255)
INK = (103 / 255, 73 / 255, 82 / 255)
WHITE = (1, 1, 1)
ROSE = (224 / 255, 92 / 255, 137 / 255)
GOLD = (210 / 255, 151 / 255, 49 / 255)


def smoothstep(value: float) -> float:
    value = max(0.0, min(1.0, value))
    return value * value * (3.0 - 2.0 * value)


def create_masked_art() -> None:
    TMP.mkdir(parents=True, exist_ok=True)
    image = Image.open(SOURCE_ART).convert("RGBA")
    width, height = image.size
    alpha = Image.new("L", image.size)
    pixels = alpha.load()
    fade_x = width * 0.075
    fade_top = height * 0.065
    fade_bottom = height * 0.075

    for y in range(height):
        vertical = min(y / fade_top, (height - 1 - y) / fade_bottom)
        for x in range(width):
            horizontal = min(x / fade_x, (width - 1 - x) / fade_x)
            pixels[x, y] = round(255 * smoothstep(min(horizontal, vertical)))

    image.putalpha(alpha)
    image.save(MASKED_ART, optimize=True)


def set_color(page: canvas.Canvas, rgb: tuple[float, float, float], alpha: float = 1) -> None:
    page.setFillColorRGB(*rgb)
    page.setFillAlpha(alpha)


def draw_star(
    page: canvas.Canvas,
    x: float,
    y: float,
    radius: float,
    rgb: tuple[float, float, float],
    alpha: float,
) -> None:
    inner = radius * 0.2
    path = page.beginPath()
    points = [
        (x, y + radius),
        (x + inner, y + inner),
        (x + radius, y),
        (x + inner, y - inner),
        (x, y - radius),
        (x - inner, y - inner),
        (x - radius, y),
        (x - inner, y + inner),
    ]
    path.moveTo(*points[0])
    for point in points[1:]:
        path.lineTo(*point)
    path.close()
    set_color(page, rgb, alpha)
    page.drawPath(path, fill=1, stroke=0)


def draw_centered(page: canvas.Canvas, text: str, y: float, size: float, color=WINE) -> None:
    set_color(page, color)
    page.setFont("Gabin", size)
    page.drawCentredString(A4[0] / 2, y, text)


def wrap_text(text: str, size: float, max_width: float) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if current and pdfmetrics.stringWidth(candidate, "Gabin", size) > max_width:
            lines.append(current)
            current = word
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines


def draw_paragraph(
    page: canvas.Canvas,
    text: str,
    top_y: float,
    size: float,
    leading: float,
    max_width: float,
    color=INK,
) -> float:
    y = top_y
    for line in wrap_text(text, size, max_width):
        draw_centered(page, line, y, size, color)
        y -= leading
    return y


def draw_background(page: canvas.Canvas) -> None:
    width, height = A4
    set_color(page, PAPER)
    page.rect(0, 0, width, height, fill=1, stroke=0)

    set_color(page, WHITE, 0.29)
    for row, y in enumerate(range(14, round(height), 18)):
        offset = 5 if row % 2 else 0
        for x in range(10 + offset, round(width), 18):
            page.circle(x, y, 0.55, fill=1, stroke=0)

    rng = random.Random(7312026)
    palette = [(WHITE, 0.7), (ROSE, 0.5), (GOLD, 0.72)]
    for index in range(44):
        x = rng.uniform(22, width - 22)
        y = rng.uniform(24, height - 24)
        radius = rng.uniform(1.8, 4.6) if index % 9 else rng.uniform(5, 7)
        color, alpha = palette[index % len(palette)]
        draw_star(page, x, y, radius, color, alpha)


def draw_qr(page: canvas.Canvas, x: float, y: float, size: float) -> None:
    qr = QrCodeWidget(
        SITE_URL,
        barLevel="H",
        barBorder=4,
        barFillColor=Color(*WINE),
        barWidth=size,
        barHeight=size,
    )
    drawing = Drawing(size, size)
    drawing.add(qr)
    renderPDF.draw(drawing, page, x, y)

    set_color(page, WINE, .82)
    page.setFont("Gabin", 6.2)
    page.drawCentredString(x + size / 2, y - 9, "СКАНИРУЙ")


def build_pdf(output: Path, include_qr: bool) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)

    pdfmetrics.registerFont(TTFont("Gabin", str(FONT)))
    page = canvas.Canvas(str(output), pagesize=A4, pageCompression=1)
    page.setTitle("Настя, этот вечер - твой!")
    page.setAuthor("Твои девчонки")
    page.setSubject("Печатное приглашение на девичник, 15 августа")
    draw_background(page)

    width, _ = A4
    draw_centered(page, "СОВЕРШЕННО СЕКРЕТНО", 806, 8.2, WINE)
    draw_centered(page, "НАСТЯ,", 755, 49, WINE)
    draw_centered(page, "ТЫ НИ О ЧЁМ НЕ ДОГАДЫВАЕШЬСЯ...", 714, 14.3, WINE)

    draw_paragraph(
        page,
        "НО МЫ, ТВОИ ЛЮБИМЫЕ ПОДРУГИ, УЖЕ ВСЁ ПРОДУМАЛИ! ТЕБЯ ЖДЁТ ОСОБЕННЫЙ ВЕЧЕР, ПОЛНЫЙ СЮРПРИЗОВ, СМЕХА И САМЫХ ТЁПЛЫХ СЛОВ.",
        681,
        10.8,
        14.5,
        466,
        INK,
    )

    draw_centered(page, "БУДЬ ГОТОВА", 611, 8.4, INK)
    draw_star(page, width / 2, 595, 4.2, WINE, 1)
    draw_centered(page, "15 АВГУСТА   /   18:30", 563, 27, WINE)
    draw_centered(page, "ОДЕВАЙСЯ ТАК, ЧТОБЫ ЧУВСТВОВАТЬ СЕБЯ САМОЙ КРАСИВОЙ", 536, 9.4, INK)
    draw_centered(page, "(ТЫ ВСЕГДА ТАКАЯ!)", 520, 9.8, WINE)
    art_size = 340
    page.drawImage(
        ImageReader(str(MASKED_ART)),
        (width - art_size) / 2,
        155,
        width=art_size,
        height=art_size,
        preserveAspectRatio=True,
        mask="auto",
    )
    if include_qr:
        draw_qr(page, 480, 185, 72)

    draw_centered(page, "ГЛАВНАЯ ГЕРОИНЯ ВЕЧЕРА", 154, 7.6, INK)
    draw_centered(page, "НИЧЕГО НЕ ПЛАНИРУЙ НА ЭТОТ ВЕЧЕР:", 132, 10.8, INK)
    draw_centered(page, "ОН ЦЕЛИКОМ ТВОЙ!", 113, 13.3, WINE)
    draw_centered(page, "ТВОИ ДЕВЧОНКИ", 78, 24, WINE)
    draw_centered(page, "НИГИНА  •  АРИНА  •  АНЯ  •  ПОЛИНА", 51, 9.4, WINE)
    draw_centered(page, "МАША  •  КАТЯ  •  АЛИНА", 34, 9.4, WINE)

    page.showPage()
    page.save()


if __name__ == "__main__":
    create_masked_art()
    build_pdf(OUTPUT_CLEAN, include_qr=False)
    build_pdf(OUTPUT_WITH_QR, include_qr=True)
