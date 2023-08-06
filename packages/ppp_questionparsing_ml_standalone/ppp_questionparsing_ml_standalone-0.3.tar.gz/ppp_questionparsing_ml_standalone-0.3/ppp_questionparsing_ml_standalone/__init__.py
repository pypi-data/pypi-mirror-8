"""Example python module for the PPP."""

from ppp_libmodule import HttpRequestHandler
from .requesthandler import RequestHandler
from .extract_triple import ExtractTriple

def app(environ, start_response):
    """Function called by the WSGI server."""
    return HttpRequestHandler(environ, start_response, RequestHandler) \
            .dispatch()

__all__ = ['ExtractTriple']
