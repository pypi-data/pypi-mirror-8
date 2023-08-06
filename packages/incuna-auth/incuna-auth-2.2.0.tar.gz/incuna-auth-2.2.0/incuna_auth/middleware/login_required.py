import re

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseForbidden
from django.utils.translation import ugettext_lazy as _

# Python 2/3 compatibility hackery
try:
    unicode
except NameError:
    unicode = str


LOGIN_EXEMPT_URLS = getattr(settings, 'LOGIN_EXEMPT_URLS', [])
LOGIN_PROTECTED_URLS = getattr(settings, 'LOGIN_PROTECTED_URLS', [r'^'])

EXEMPT_URLS = [
    re.compile('^%s$' % settings.LOGIN_URL.lstrip('/')),
    re.compile('^%s$' % settings.LOGOUT_URL.lstrip('/')),
]
EXEMPT_URLS += [re.compile(unicode(expr)) for expr in LOGIN_EXEMPT_URLS]
PROTECTED_URLS = [re.compile(unicode(expr)) for expr in LOGIN_PROTECTED_URLS]
SEND_MESSAGE = getattr(settings, 'LOGIN_REQUIRED_SEND_MESSAGE', True)


class LoginRequiredMiddleware:
    '''
    Middleware that requires a user to be authenticated to view any page in
    LOGIN_PROTECTED_URLS other than LOGIN_URL. Exemptions to this requirement
    can optionally be specified in settings via a list of regular expressions
    in LOGIN_EXEMPT_URLS (which you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.

    Will default to protecting everything if LOGIN_PROTECTED_URLS is not in
    settings.


    Original code from:
    http://onecreativeblog.com/post/59051248/django-login-required-middleware

    This version has been modified to allow us to define areas of the site to
    password protect instead of protecting everything under /.
    '''
    def process_request(self, request):
        assert hasattr(request, 'user'), (
            "The 'LoginRequiredMiddleware' "
            + "requires authentication middleware to be installed. Edit your "
            + "'MIDDLEWARE_CLASSES' setting to insert "
            + "'django.contrib.auth.middlware.AuthenticationMiddleware'. "
            + "If that doesn't work, ensure your 'TEMPLATE_CONTEXT_PROCESSORS' "
            + "setting includes 'django.core.context_processors.auth'."
        )

        # Jump over this middleware if not a protected url.
        path = request.path_info.lstrip('/')
        path_is_exempt = any(m.match(path) for m in EXEMPT_URLS)
        path_is_protected = any(m.match(path) for m in PROTECTED_URLS)
        if path_is_exempt or not path_is_protected:
            return

        # Jump over this middleware if user logged in.
        if request.user.is_authenticated():
            return

        # Raise a 403 for POST/DELETE etc.
        if request.method != 'GET':
            return HttpResponseForbidden()

        # Add a message, and redirect to login.
        if SEND_MESSAGE:
            messages.info(request, _('You must be logged in to view this page.'))

        return redirect_to_login(request.path_info)
