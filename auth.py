import re

from vial.middleware import Middleware


STATIC_TOKEN = "token_hd27gd340d293f253dg3h40f23eh3"


class TokenMiddleware(Middleware):
    regex = re.compile(r"^Token: (\w+)$")

    def process_request(self, request):
        header = request.headers.get("Authorization") or ""
        match = self.regex.match(header)
        token = match.group(1) if match else None
        request.token = token


class InvalidTokenException(Exception):
    pass


def login_required(handler):
    def wrapped_handler(request, response, *args, **kwargs):
        token = getattr(request, "token", None)

        if token is None or token != STATIC_TOKEN:
            raise InvalidTokenException

        return handler(request, response, *args, **kwargs)

    return wrapped_handler


def on_exception(request, response, exception):
    if isinstance(exception, InvalidTokenException):
        response.text = "Token is invalid"
        response.status_code = 401
