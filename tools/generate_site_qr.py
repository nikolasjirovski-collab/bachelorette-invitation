#!/usr/bin/env python3
"""Generate the invitation QR code in the site's pink and wine palette."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.graphics import renderSVG
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.lib.colors import HexColor


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "assets" / "qr"
SITE_URL = "https://nikolasjirovski-collab.github.io/bachelorette-invitation/"
SIZE = 420
PNG_MODULE_SIZE = 12
QUIET_ZONE = 4
CARD_SIZE = (1200, 1600)
FONT = ROOT / "assets" / "fonts" / "Gabin-Regular.ttf"


def build_drawing() -> Drawing:
    drawing = Drawing(SIZE, SIZE)
    drawing.add(Rect(0, 0, SIZE, SIZE, fillColor=HexColor("#f0acb2"), strokeColor=None))

    qr = QrCodeWidget(
        SITE_URL,
        barLevel="H",
        barBorder=4,
        barFillColor=HexColor("#74182e"),
        barWidth=SIZE,
        barHeight=SIZE,
    )
    drawing.add(qr)
    return drawing


def centered_text(draw: ImageDraw.ImageDraw, y: int, text: str, font: ImageFont.FreeTypeFont, fill: str) -> None:
    box = draw.textbbox((0, 0), text, font=font)
    x = (CARD_SIZE[0] - (box[2] - box[0])) // 2
    draw.text((x, y), text, font=font, fill=fill)


def draw_star(draw: ImageDraw.ImageDraw, x: int, y: int, radius: int, fill: str) -> None:
    inner = max(2, radius // 5)
    draw.polygon(
        [
            (x, y - radius),
            (x + inner, y - inner),
            (x + radius, y),
            (x + inner, y + inner),
            (x, y + radius),
            (x - inner, y + inner),
            (x - radius, y),
            (x - inner, y - inner),
        ],
        fill=fill,
    )


def build_share_card(qr_image: Image.Image) -> Image.Image:
    card = Image.new("RGB", CARD_SIZE, "#f0acb2")
    draw = ImageDraw.Draw(card)

    for row, y in enumerate(range(18, CARD_SIZE[1], 30)):
        offset = 8 if row % 2 else 0
        for x in range(18 + offset, CARD_SIZE[0], 30):
            draw.ellipse((x, y, x + 2, y + 2), fill="#f8cbd0")

    stars = [
        (104, 132, 17, "#ffffff"),
        (1090, 190, 12, "#d29731"),
        (176, 484, 11, "#df5c89"),
        (1040, 610, 19, "#ffffff"),
        (94, 1282, 13, "#d29731"),
        (1092, 1370, 16, "#df5c89"),
        (1002, 1108, 8, "#ffffff"),
        (170, 1026, 8, "#ffffff"),
    ]
    for star in stars:
        draw_star(draw, *star)

    label_font = ImageFont.truetype(str(FONT), 92)

    qr_size = qr_image.width
    qr_x = (CARD_SIZE[0] - qr_size) // 2
    qr_y = 345
    card.paste(qr_image, (qr_x, qr_y))

    centered_text(draw, 1192, "ОТКРЫВАЙ", label_font, "#74182e")
    return card


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    drawing = build_drawing()
    renderSVG.drawToFile(drawing, str(OUTPUT_DIR / "site-invitation-qr.svg"))

    qr = QrCodeWidget(SITE_URL, barLevel="H", barBorder=QUIET_ZONE)
    qr.qr.make()
    module_count = qr.qr.moduleCount
    image_size = (module_count + QUIET_ZONE * 2) * PNG_MODULE_SIZE
    image = Image.new("RGB", (image_size, image_size), "#f0acb2")
    draw = ImageDraw.Draw(image)
    for row, modules in enumerate(qr.qr.modules):
        for column, enabled in enumerate(modules):
            if not enabled:
                continue
            x = (column + QUIET_ZONE) * PNG_MODULE_SIZE
            y = (row + QUIET_ZONE) * PNG_MODULE_SIZE
            draw.rectangle(
                (x, y, x + PNG_MODULE_SIZE - 1, y + PNG_MODULE_SIZE - 1),
                fill="#74182e",
            )
    image.save(OUTPUT_DIR / "site-invitation-qr.png", optimize=True)
    build_share_card(image).save(OUTPUT_DIR / "nastya-invitation-qr-card.png", optimize=True)


if __name__ == "__main__":
    main()
