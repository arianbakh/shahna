import random
import logging
from hashlib import sha1
from os import path, stat
from PIL import Image

from django.conf import settings

logger = logging.getLogger(__name__)


def image_thumb_name(name, size='100x100'):
    parts = name.rsplit('.', 1)
    if len(parts) < 2:
        return parts[0] + '_' + size
    return "%s_%s.%s" % ( parts[0], size, parts[1])

def make_thumbnail(img):
    thumb_adr = image_thumb_name(img)
    try:
        origin = Image.open(img)
        # For profile page
        origin.thumbnail((200, 200), Image.ANTIALIAS)
        origin.save(image_thumb_name(img, '200x200'), origin.format)
        # For thumbnails
        origin.thumbnail((40, 40), Image.ANTIALIAS)
        origin.save(image_thumb_name(img, '40x40'), origin.format)
    except:
        logger.warning("problem at creating thumbnails")


def random_key_generator(email):
    salt = sha1(str(random.random())).hexdigest()[:5]
    key = sha1(salt + email.encode('utf-8')).hexdigest()
    return key

def email_verification_days():
    return getattr(settings, 'EMAILAUTH_VERIFICATION_DAYS', 3)
