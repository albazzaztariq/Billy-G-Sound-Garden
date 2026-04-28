"""Render a guitar icon to assets/guitar.ico, .icns, and .png.

Approach: Pillow ImageDraw with an emoji-capable font (Segoe UI Emoji on
Windows, Apple Color Emoji on macOS) using `embedded_color=True` so the
COLR/CBDT color glyph table is preserved. Falls back to a hand-drawn
guitar silhouette if no emoji font is available.

Inputs:  none
Outputs: assets/guitar.png, assets/guitar.ico, assets/guitar.icns
Packages: Pillow (PIL.Image, ImageDraw, ImageFont)
"""
from __future__ import annotations
import io
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASSETS = PROJECT_ROOT / "assets"
SIZES = (16, 24, 32, 48, 64, 128, 256, 512)
GUITAR_GLYPH = "\U0001F3B8"


def find_emoji_font() -> Path | None:
    candidates = [
        Path("C:/Windows/Fonts/seguiemj.ttf"),
        Path("/System/Library/Fonts/Apple Color Emoji.ttc"),
        Path("/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"),
    ]
    for p in candidates:
        if p.exists():
            print(f"[DEBUG] make_icon: using emoji font {p}")
            return p
    print("[DEBUG] make_icon: no emoji font found, will draw silhouette")
    return None


def render_emoji(size: int, font_path: Path) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Apple Color Emoji only ships at fixed sizes (160). Pillow handles scaling
    # but we ask for a sensible target size.
    target_px = max(16, int(size * 0.95))
    try:
        font = ImageFont.truetype(str(font_path), size=target_px)
    except OSError:
        font = ImageFont.truetype(str(font_path), size=109)
    bbox = draw.textbbox((0, 0), GUITAR_GLYPH, font=font, embedded_color=True)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - w) // 2 - bbox[0]
    y = (size - h) // 2 - bbox[1]
    draw.text((x, y), GUITAR_GLYPH, font=font, embedded_color=True)
    if img.size != (size, size):
        img = img.resize((size, size), Image.LANCZOS)
    return img


def render_silhouette(size: int) -> Image.Image:
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    s = size

    body = (s * 0.50, s * 0.60)
    neck = (int(s * 0.10), int(s * 0.55))
    body_color = (160, 92, 36, 255)
    neck_color = (90, 50, 22, 255)
    string_color = (240, 240, 240, 220)
    hole_color = (20, 20, 20, 255)

    d.line(
        [(s * 0.62, s * 0.40), (s * 0.18, s * 0.10)],
        fill=neck_color, width=max(2, s // 18),
    )
    d.rectangle([s * 0.10, s * 0.05, s * 0.20, s * 0.18], fill=neck_color)
    bx, by = s * 0.50, s * 0.62
    d.ellipse([bx - body[0] / 2, by - body[1] / 2, bx + body[0] / 2, by + body[1] / 2],
              fill=body_color, outline=(60, 30, 10, 255), width=max(1, s // 64))
    hole_r = s * 0.10
    d.ellipse([bx - hole_r, by - hole_r, bx + hole_r, by + hole_r], fill=hole_color)
    for i in range(3):
        off = (i - 1) * (s * 0.012)
        d.line(
            [(s * 0.18 + off, s * 0.12), (bx + off, by)],
            fill=string_color, width=max(1, s // 96),
        )
    return img


def main() -> int:
    print("[DEBUG] make_icon: starting")
    ASSETS.mkdir(parents=True, exist_ok=True)
    font = find_emoji_font()
    images: list[Image.Image] = []
    for s in SIZES:
        try:
            im = render_emoji(s, font) if font else render_silhouette(s)
            extrema = im.getextrema()
            color_present = any(ch[1] > 0 for ch in extrema[:3])
            if not color_present:
                print(f"[DEBUG] make_icon: emoji rendered colorless at {s}, falling back to silhouette")
                im = render_silhouette(s)
        except Exception as e:
            print(f"[DEBUG] make_icon: emoji render failed at {s} ({e}); using silhouette")
            im = render_silhouette(s)
        images.append(im)
        print(f"[DEBUG] make_icon: rendered {s}x{s}")

    images[-2].save(ASSETS / "guitar.png", "PNG")
    print(f"[DEBUG] make_icon: wrote {ASSETS / 'guitar.png'}")

    ico_sizes = [(s, s) for s in SIZES if s <= 256]
    images[0].save(
        ASSETS / "guitar.ico",
        format="ICO",
        sizes=ico_sizes,
        append_images=[im for im in images[1:] if im.size[0] <= 256],
    )
    print(f"[DEBUG] make_icon: wrote {ASSETS / 'guitar.ico'}")

    try:
        images[-1].save(ASSETS / "guitar.icns", format="ICNS")
        print(f"[DEBUG] make_icon: wrote {ASSETS / 'guitar.icns'}")
    except Exception as e:
        print(f"[DEBUG] make_icon: ICNS write failed ({e}); .icns will be regenerated on macOS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
