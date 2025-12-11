# src/meme_renderer/render_meme.py
from PIL import Image, ImageDraw, ImageFont
import os
from typing import Tuple

# Absolute base paths
THIS_DIR = os.path.dirname(__file__)                     # .../src/meme_renderer
BASE_DIR = os.path.dirname(os.path.dirname(THIS_DIR))    # .../CaptionAI root
FONTS_DIR = os.path.join(BASE_DIR, "data", "fonts")

# Put Impact.ttf ya koi bhi .ttf yahan
DEFAULT_FONT_PATH = os.path.join(FONTS_DIR, "Impact.ttf")
OUTPUT_DIR = os.path.join(BASE_DIR, "output_memes")


def get_text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont):
    """Use textbbox for Pillow>=10."""
    bbox = draw.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    return width, height


def wrap_text(text: str, draw: ImageDraw.ImageDraw, font: ImageFont.ImageFont, max_width: int):
    lines = []
    words = text.split()
    while words:
        line_words = []
        while words:
            line_words.append(words.pop(0))
            candidate = " ".join(line_words + words[:1])
            w, _ = get_text_size(draw, candidate, font)
            if w > max_width:
                break
        lines.append(" ".join(line_words))
    return lines


def draw_text_with_outline(
    draw: ImageDraw.ImageDraw,
    xy: Tuple[int, int],
    text: str,
    font: ImageFont.ImageFont,
    fill="black",
    outline="white",
    outline_width: int = 2,
):
    x, y = xy
    # outline
    for dx in [-outline_width, 0, outline_width]:
        for dy in [-outline_width, 0, outline_width]:
            if dx == 0 and dy == 0:
                continue
            draw.text((x + dx, y + dy), text, font=font, fill=outline)
    # main
    draw.text((x, y), text, font=font, fill=fill)


def render_meme(
    template_path: str,
    top_text: str,
    bottom_text: str,
    output_name: str = None,
) -> str:
    """
    Drake-style meme:
    - Left: original 2-panel Drake image
    - Right: big white area
      - Top-right: top_text
      - Bottom-right: bottom_text
    """
    # 1) Load base template (2-panel Drake)
    base_img = Image.open(template_path).convert("RGB")
    w, h = base_img.size

    # 2) New canvas: left = image, right = white panel
    new_w = w * 2
    canvas = Image.new("RGB", (new_w, h), "white")
    canvas.paste(base_img, (0, 0))

    # 3) Font
    font_size = max(22, int(h * 0.05))
    try:
        font = ImageFont.truetype(DEFAULT_FONT_PATH, font_size)
    except OSError:
        print(
            f"[render_meme] Could not open font at '{DEFAULT_FONT_PATH}'. "
            "Falling back to default PIL font."
        )
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(canvas)

    # Right side text panel
    padding_x = int(w * 0.07)
    padding_y = int(h * 0.05)

    right_x0 = w + padding_x
    right_x1 = new_w - padding_x
    max_text_width = right_x1 - right_x0

    # line height
    _, line_height = get_text_size(draw, "Ay", font)

    # ==== TOP TEXT (upper half) ====
    top_lines = wrap_text(top_text, draw, font, max_text_width)
    top_total_h = line_height * len(top_lines)

    top_panel_y0 = padding_y
    top_panel_y1 = (h // 2) - padding_y
    top_panel_h = top_panel_y1 - top_panel_y0

    y = top_panel_y0 + (top_panel_h - top_total_h) // 2  # vertically center in upper half

    for line in top_lines:
        line_w, _ = get_text_size(draw, line, font)
        x = right_x0 + (max_text_width - line_w) // 2     # center horizontally
        draw_text_with_outline(draw, (x, y), line, font)
        y += line_height

    # ==== BOTTOM TEXT (lower half) ====
    bottom_lines = wrap_text(bottom_text, draw, font, max_text_width)
    bottom_total_h = line_height * len(bottom_lines)

    bottom_panel_y0 = (h // 2) + padding_y
    bottom_panel_y1 = h - padding_y
    bottom_panel_h = bottom_panel_y1 - bottom_panel_y0

    y = bottom_panel_y0 + (bottom_panel_h - bottom_total_h) // 2  # vertically center in lower half

    for line in bottom_lines:
        line_w, _ = get_text_size(draw, line, font)
        x = right_x0 + (max_text_width - line_w) // 2
        draw_text_with_outline(draw, (x, y), line, font)
        y += line_height

    # 4) Save
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    if output_name is None:
        base_name = os.path.splitext(os.path.basename(template_path))[0]
        output_name = f"{base_name}_drake_text_right.png"

    out_path = os.path.join(OUTPUT_DIR, output_name)
    canvas.save(out_path)
    return out_path


if __name__ == "__main__":
    # local test – yahan apne template ka naam daal do
    test_template = os.path.join(BASE_DIR, "data", "templates", "drake.jpg")
    out = render_meme(
        test_template,
        "Doing your\nown research\nfor a test",
        "Copy and pasting\nfrom Wikipedia",
    )
    print("Saved:", out)
