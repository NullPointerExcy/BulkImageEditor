# BulkImageEditor

[![Download Latest Release](https://img.shields.io/github/v/release/NullPointerExcy/BulkImageEditor)](https://github.com/NullPointerExcy/BulkImageEditor/releases/latest)

A simple image processing tool for resizing images and adding text watermarks to them. Built using Python's `Pillow`
library, this tool can adjust image dimensions while maintaining aspect ratio and apply customizable text or image watermarks.

## Features

- **Resize Images**: Maintain aspect ratio while resizing images to a specified max width.
- **Add Watermarks**: Apply either text or image-based watermarks in configurable positions and transparency levels.
- **Fill Watermarks**: Optionally fill the entire image with the watermark (for that professional, branded wallpaper
  effect).

## Requirements

- Python 3.7 or higher
- Pillow (Python Imaging Library)

Install the required dependencies with:

```bash
pip install pillow
```

## Usage
### Basic Usage

Use the .exe file, otherwise follow the next steps:

```bash
py .\main.py --input_path path/to/input --output_path path/to/output [options]
```

### Arguments

| Argument          | Type    | Default             | Description                                                                                |
|-------------------|---------|---------------------|--------------------------------------------------------------------------------------------|
| --input_path      | str     | Required            | Path to the directory containing images to be processed.                                   |
| --output_path     | str     | Required            | Path to the directory where processed images will be saved.                                |
| --resize          | Flag    | False               | Enable resizing of images.                                                                 |
| --max_width       | int     | 800                 | Max width for resizing images (maintains aspect ratio).                                    |
| --max_height      | int     | 800                 | Max height for resizing images (maintains aspect ratio).                                   |
| --add_watermark   | Flag    | False               | Enable watermarking on images.                                                             |
| --watermark_text  | str     | "Sample Watermark"  | Text to use for watermarking. Ignored if --watermark_image is specified.                   |
| --watermark_image | str     | None                | Path to an image file for use as a watermark (overrides --watermark_text).                 |
| --position        | str     | "bottom-right"      | Position of the watermark. Options: top-left, top-right, bottom-left, bottom-right, center |
| --font_size       | int     | 40                  | Font size for text watermarking.                                                           |
| --font_family     | str     | "arial"             | Font family for the text watermark.                                                        |
| --text_color      | str     | "#ffffff"           | Hex color code for the text watermark.                                                     |
| --alpha           | float   | 0.5                 | Transparency level of the watermark (0 = fully transparent, 1 = opaque).                   |
| --fill            | Flag    | False               | Fill the entire image with the watermark (tiled effect).                                   |
                           
