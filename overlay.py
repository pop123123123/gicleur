from PIL import Image, ImageDraw, ImageFont

W = 1 << 8


def overlay(msg, in_path, out_path):
    img = Image.open(in_path).convert("RGBA")
    img = img.resize((W, W * img.height // img.width))
    w, h = img.width, img.height

    overlay = Image.new("RGBA", img.size, (255, 255, 255, 0))
    overlayDraw = ImageDraw.Draw(overlay)

    h_base = 2 * h // 3
    r_height = h // 8
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