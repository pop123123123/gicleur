from PIL import Image, ImageDraw, ImageFont

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

    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    overlayDraw = ImageDraw.Draw(overlay)

    h_base = 2 * h // 3
    r_height = max(h // 8, 20)
    shape = [(0, h_base), (w, h_base + r_height)]
    overlayDraw.rectangle(shape, fill=(0, 0, 0, 128))
    fnt = ImageFont.truetype("LiberationSans-Regular.ttf", r_height // 2)
    tw, th = overlayDraw.textsize(msg, font=fnt)
    overlayDraw.text(
        ((w - tw) / 2, h_base + (r_height - th) // 2),
        msg,
        font=fnt,
        fill=(255, 255, 255, 200),
    )

    out = Image.alpha_composite(img, overlay)
    out.convert("RGB").save(out_path, "JPEG")


if __name__ == "__main__":
    msg = "Envi de gicler"
    in_path = "test.png"
    out_path = "out.jpg"
    overlay(msg, in_path, out_path)