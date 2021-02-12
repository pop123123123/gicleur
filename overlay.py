from PIL import Image, ImageDraw, ImageFont

from image_utils import ImageText

MAX_SIZE = 1 << 8


def get_size(size):
    if size[0] > size[1]:
        return (MAX_SIZE, MAX_SIZE * size[1] // size[0])
    else:
        return (MAX_SIZE * size[0] // size[1], MAX_SIZE)


def overlay(msg, in_path, out_path):
    img = Image.open(in_path).convert("RGBA")
    img = img.resize(get_size(img.size))
    w, h = img.width, img.height

    r_height = max(h // 8, 26)
    h_mid = 2 * h // 3
    f_size = int(r_height * 0.6)

    imgText = ImageText(img.size)
    box_size = imgText.write_text_box(
        (0, h_mid),
        msg,
        box_width=int(w * 0.95),
        font_filename="LiberationSans-Regular.ttf",
        font_size=f_size,
        color=(255, 255, 255, 200),
        place="center",
    )

    imgText = ImageText(img.size)
    imgText.write_text_box(
        (0, h_mid - box_size[1] // 2),
        msg,
        box_width=int(w * 0.95),
        font_filename="LiberationSans-Regular.ttf",
        font_size=f_size,
        color=(255, 255, 255, 200),
        place="center",
    )

    r_height = box_size[1] + f_size * 0.6
    shape = [(0, h_mid - r_height // 2), (w, h_mid + r_height // 2)]

    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    overlayDraw = ImageDraw.Draw(overlay)
    overlayDraw.rectangle(shape, fill=(0, 0, 0, 128))

    out = Image.alpha_composite(img, overlay)
    out = Image.alpha_composite(out, imgText.image)
    out.convert("RGB").save(out_path, "JPEG")


if __name__ == "__main__":
    import sys

    msg = "Envi de gicler"
    if len(sys.argv) > 1:
        msg = sys.argv[1]
    in_path = "test.png"
    out_path = "out.jpg"
    overlay(msg, in_path, out_path)