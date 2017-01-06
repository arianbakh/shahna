from os import path, stat
from PIL import Image

def image_thumb_name(name):
    parts = name.rsplit('.', 1)
    if len(parts) < 2:
        return parts[0] + '_thumb'
    return parts[0] + "_thumb." + parts[1]

def make_thumbnail(img):
    thumb_adr = image_thumb_name(img)
    try:
        if not path.exists(thumb_adr) or stat(thumb_adr).st_mtime < stat(p).st_mtime:
            origin = Image.open(img)
            origin.thumbnail((100, 100), Image.ANTIALIAS)
            origin.save(thumb_adr, origin.format)
    except:
        pass
