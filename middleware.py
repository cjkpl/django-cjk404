import re

from django import http
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils.timezone import now

from .models import PageNotFoundEntry
from wagtail.core.models import Site

IGNORED_404S = getattr(settings, 'IGNORED_404S', [
    r'^/static/',
    r'^/favicon.ico'
])

DJANGO_REGEX_REDIRECTS_CACHE_KEY = 'django-regex-redirects-regular'
DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY = 'django-regex-redirects-regex'
DJANGO_REGEX_REDIRECTS_CACHE_TIMEOUT = 60


class PageNotFoundRedirectMiddleware:
    def __init__(self, response):
        self.response = response
        self.blacklist_url_patterns = [
            re.compile(string) for string in IGNORED_404S]

    def __call__(self, request):
        url = request.path
        if self._check_url_in_blacklist(url):
            return self.response(request)
        else:
            return self.handle_request(request)

    def _check_url_in_blacklist(self, url):
        return any([pattern.match(url) for pattern in self.blacklist_url_patterns])

    def handle_request(self, request):
        response = self.response(request)
        if response.status_code != 404:
            return response

        url = request.path
        site = Site.find_for_request(request)
        entry = PageNotFoundEntry.objects.filter(
            site=site, url=url).first()
        if entry:
            entry.hits += 1
            entry.last_hit = now()
            entry.save()

        full_path = request.get_full_path()
        http_host = request.META.get('HTTP_HOST', '')
        if http_host:
            if request.is_secure():
                http_host = 'https://' + http_host
            else:
                http_host = 'http://' + http_host

        redirects = cache.get(DJANGO_REGEX_REDIRECTS_CACHE_KEY)
        if redirects is None:
            redirects = list(PageNotFoundEntry.objects.all().values())
            cache.set(DJANGO_REGEX_REDIRECTS_CACHE_KEY, redirects, DJANGO_REGEX_REDIRECTS_CACHE_TIMEOUT)

        for redirect in redirects:
            if entry:
                if entry.redirect_to:
                    if entry.permanent:
                        return HttpResponsePermanentRedirect(entry.redirect_to)
                    else:
                        return HttpResponseRedirect(entry.redirect_to)

            if redirect['url'] == full_path:
                if redirect['redirect_to_url'].startswith('http') or redirect['redirect_to_url'].startswith('https'):
                    return http.HttpResponsePermanentRedirect(redirect['redirect_to_url'])
                else:
                    return http.HttpResponsePermanentRedirect(http_host + redirect['redirect_to_url'])

            if settings.APPEND_SLASH and not request.path.endswith('/'):
                path_len = len(request.path)
                slashed_full_path = full_path[:path_len] + '/' + full_path[path_len:]

                if redirect['url'] == slashed_full_path:
                    if redirect['redirect_to_url'].startswith('http') or redirect['redirect_to_url'].startswith('https'):
                        return http.HttpResponsePermanentRedirect(redirect['redirect_to_url'])
                    else:
                        return http.HttpResponsePermanentRedirect(http_host + redirect['redirect_to_url'])

        regular_expressions_redirects = cache.get(DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY)
        if regular_expressions_redirects is None:
            regular_expressions_redirects = list(PageNotFoundEntry.objects.filter(regular_expression=True).values())
            cache.set(DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY, regular_expressions_redirects,
                      DJANGO_REGEX_REDIRECTS_CACHE_TIMEOUT)

        for redirect in regular_expressions_redirects:

            try:
                old_path = re.compile(redirect['url'], re.IGNORECASE)
            except re.error:
                continue

            if re.match(redirect['url'], full_path):
                if redirect['redirect_to_page_id'] is not None:
                    entry = PageNotFoundEntry.objects.filter(
                        redirect_to_page_id=redirect['redirect_to_page_id'], id=redirect['id']).first()
                    if entry.redirect_to:
                        if entry.permanent:
                            return HttpResponsePermanentRedirect(entry.redirect_to)
                        else:
                            return HttpResponseRedirect(entry.redirect_to)
                new_path = redirect['redirect_to_url'].replace('$', '\\')
                replaced_path = re.sub(old_path, new_path, full_path)
                if redirect['redirect_to_url'].startswith('http') or redirect['redirect_to_url'].startswith('https'):
                    return http.HttpResponsePermanentRedirect(replaced_path)
                else:
                    return http.HttpResponsePermanentRedirect(http_host + replaced_path)

        if response.status_code == 404 and not entry:
            PageNotFoundEntry.objects.create(
                site=site, url=url, last_hit=now())

        return response
