from typing import Literal, Optional
from PIL import Image, ImageDraw, ImageFont
import os


def add_watermark(
        input_dir: str,
        output_dir: str,
        watermark_text: Optional[str] = "Sample Watermark",
        watermark_image: Optional[str] = None,
        font_size: int = 30,
        font: str = "arial.ttf",
        position: Literal["bottom-left", "bottom-right", "top-left", "top-right", "center"] = "bottom-right",
        alpha: float = 0.5,
        fill: bool = False
):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_dir, filename)
            img = Image.open(img_path).convert("RGBA")
            watermark_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))

            if watermark_image:
                watermark = Image.open(watermark_image).convert("RGBA")
                watermark = resize_watermark(watermark, img.size)

                if fill:
                    watermark = apply_transparency(watermark, alpha)
                    watermark_layer = tile_watermark(watermark_layer, watermark)
                else:
                    watermark = apply_transparency(watermark, alpha)
                    x, y = get_watermark_position(img.size, watermark.width, watermark.height, position)
                    watermark_layer.paste(watermark, (x, y), watermark)
            else:
                draw = ImageDraw.Draw(watermark_layer)
                try:
                    font = ImageFont.truetype(font, font_size)
                except IOError:
                    font = ImageFont.load_default()

                if fill:
                    fill_watermark_text(draw, img.size, watermark_text, font, alpha)
                else:
                    bbox = draw.textbbox((0, 0), watermark_text, font=font)
                    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
                    x, y = get_watermark_position(img.size, text_width, text_height, position)
                    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, int(255 * alpha)))

            watermarked_image = Image.alpha_composite(img, watermark_layer)
            output_image = watermarked_image.convert("RGB")
            output_path = os.path.join(output_dir, filename)
            output_image.save(output_path)
            print(f"Watermarked and saved: {output_path}")


def resize_watermark(watermark, base_image_size, scale_factor=0.1):
    base_width, base_height = base_image_size
    watermark_width = int(base_width * scale_factor)
    watermark_height = int((watermark.size[1] / watermark.size[0]) * watermark_width)
    return watermark.resize((watermark_width, watermark_height), Image.Resampling.LANCZOS)


def apply_transparency(image, alpha):
    alpha = min(max(alpha, 0), 1)
    r, g, b, a = image.split()
    a = a.point(lambda p: int(p * alpha))
    return Image.merge("RGBA", (r, g, b, a))


def get_watermark_position(img_size, wm_width, wm_height, position):
    img_width, img_height = img_size
    margin = 10

    if position == "bottom-right":
        x = img_width - wm_width - margin
        y = img_height - wm_height - margin
    elif position == "bottom-left":
        x = margin
        y = img_height - wm_height - margin
    elif position == "top-right":
        x = img_width - wm_width - margin
        y = margin
    elif position == "top-left":
        x = margin
        y = margin
    elif position == "center":
        x = (img_width - wm_width) // 2
        y = (img_height - wm_height) // 2
    else:
        x, y = img_width - wm_width - margin, img_height - wm_height - margin

    return x, y


def tile_watermark(base_layer, watermark):
    wm_width, wm_height = watermark.size
    base_width, base_height = base_layer.size

    for x in range(0, base_width, wm_width):
        for y in range(0, base_height, wm_height):
            base_layer.paste(watermark, (x, y), watermark)
    return base_layer


def fill_watermark_text(draw, img_size, text, font, alpha):
    img_width, img_height = img_size
    text_width, text_height = draw.textsize(text, font=font)

    for x in range(0, img_width, text_width + 50):
        for y in range(0, img_height, text_height + 50):
            draw.text((x, y), text, font=font, fill=(255, 255, 255, int(255 * alpha)))


if __name__ == "__main__":
    add_watermark(
        "../images/input",
        "../images/output",
        watermark_text="Test Watermark",
        watermark_image="../images/watermark/test.png",
        font_size=40,
        position="bottom-right",
        alpha=0.4,
        fill=True
    )
