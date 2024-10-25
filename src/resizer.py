from PIL import Image
import os


def resize_images_maintain_aspect_ratio(input_dir, output_dir, max_size=(800, 800)):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(input_dir, filename)
            img = Image.open(img_path)
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
            output_path = os.path.join(output_dir, filename)
            img.save(output_path)


if __name__ == "__main__":
    resize_images_maintain_aspect_ratio("../images/input", "../images/output", max_size=(512, 512))
