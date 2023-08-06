from django.http import Http404
from .views import page


class PageFallbackMiddleware(object):
    def process_response(self, request, response):
        if response.status_code != 404:
            return response  # No need to check for a page for non-404 responses.
        try:
            return page(request, request.path_info)

        # django.contrib.flatpages usually ignores non-404 exceptions in production.
        # This can cause a site to show "page not found" when what you want is an error.
        except Http404:
            return response
