from django.conf import settings
from django.utils import translation
from django.utils.cache import patch_vary_headers
import logging
logger = logging.getLogger(__name__)

class MultiLangMiddleware(object):
    """
    This is a very simple middleware that parses a request
    and decides what translation object to install in the current
    thread context. This allows pages to be dynamically
    translated to the language the user desires (if the language
    is available, of course).
    """

    SUPPORTED = dict(settings.LANGUAGES)

    def process_request(self, request):
        language = None

        if 'lang' in request.POST:
            language = request.POST['lang']
        elif 'l' in request.GET:
            language = request.GET['l'][:2].lower()
        elif 'preferences_lang' in request.COOKIES:
            language = request.COOKIES['settings_lang']

        if (not language) or (language not in MultiLangMiddleware.SUPPORTED):
            language = settings.LANGUAGE_CODE[:2].lower()

        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()

    def process_response(self, request, response):
        patch_vary_headers(response, ('Accept-Language',))
        if 'Content-Language' not in response:
            response['Content-Language'] = translation.get_language()
        translation.deactivate()
        return response
