import requests
import shutil
import urllib
import tempfile
import asyncio

import overlay


def tempPath(suffix=None):
    fp = tempfile.NamedTemporaryFile(suffix=suffix)
    path = fp.name
    fp.close()

    return path


async def get_last_att(channel, bot):
    attachments = None
    async for message in channel.history(limit=200):
        if message.author != bot and len(message.attachments) > 0:
            attachments = message.attachments
            break
    return attachments[-1]


async def download_avatar_and_overlay(mention, msg):
    out_path = tempPath(".jpg")
    f = tempfile.NamedTemporaryFile(mode="w+b")
    await mention.avatar_url.save(f.name)
    overlay.overlay(msg, f.name, out_path)
    f.close()
    return out_path


class Command:
    @classmethod
    async def gicle(cls, in_string, channel, bot, mentions=None):
        img_url = in_string
        out_path = tempPath(".jpg")
        msg = "Envi de gicler"
        in_path = None

        if mentions is not None:
            if len(in_string.strip()) > 0:
                msg = in_string.strip()
            return await asyncio.gather(
                *[download_avatar_and_overlay(m, msg) for m in mentions]
            )

        if "http" not in in_string:
            if len(in_string.strip()) > 0:
                msg = in_string.strip()
            att = await get_last_att(channel, bot)
            f = tempfile.NamedTemporaryFile(mode="w+b", suffix=att.filename)
            await att.save(f.name)
            overlay.overlay(msg, f.name, out_path)
            f.close()
            return [out_path]

        x = in_string.split(maxsplit=1)
        if len(x) > 1:
            img_url, msg = x

        r = requests.get(img_url, stream=True)

        if r.status_code == 200:
            r.raw.decode_content = True

            f = tempfile.NamedTemporaryFile(mode="wb")
            in_path = f.name
            shutil.copyfileobj(r.raw, f)

            overlay.overlay(msg, in_path, out_path)
            f.close()
            return [out_path]
        else:
            return None


if __name__ == "__main__":
    print(
        Command.gicle(
            "https://cdn.cnn.com/cnnnext/dam/assets/190415104943-fake-smile-stock-exlarge-169.jpg"
        )
    )
