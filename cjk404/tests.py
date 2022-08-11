from __future__ import unicode_literals

from unittest.case import skipUnless

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django.core.cache import cache
from wagtail.core.models import Site


from .middleware import (
    DJANGO_REGEX_REDIRECTS_CACHE_KEY,
    DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY,
)
from .models import PageNotFoundEntry


class Cjk404RedirectTests(TestCase):
    def setUp(self):
        cache.delete(DJANGO_REGEX_REDIRECTS_CACHE_KEY)
        cache.delete(DJANGO_REGEX_REDIRECTS_CACHE_REGEX_KEY)

    def test_model(self):
        site = Site.objects.filter(is_default_site=True)[0]
        r1 = PageNotFoundEntry.objects.create(
            url="/initial", redirect_to_url="/new_target", site=site
        )
        self.assertEqual(r1.__str__(), "/initial ---> /new_target")

    def redirect_url(
        self,
        permanent,
        old_url,
        redirect_url,
        requested_url,
        status_code=None,
        regexp=False,
    ):
        site = Site.objects.filter(is_default_site=True)[0]
        pnfe = PageNotFoundEntry.objects.create(
            permanent=permanent,
            url=old_url,
            redirect_to_url=redirect_url,
            site=site,
        )
        self.assertEqual(pnfe.hits, 0)
        response = self.client.get(requested_url)
        if status_code:
            self.assertRedirects(
                response, redirect_url, status_code=status_code, target_status_code=404
            )
        else:
            self.assertRedirects(response, redirect_url)
        pnfe.refresh_from_db()
        self.assertEqual(pnfe.hits, 1)

    def test_redirect(self):
        self.redirect_url(False, "/initial1/", "/new_target/", "/initial1/", 302)

    def test_redirect_premanent(self):
        self.redirect_url(True, "/initial2/", "/new_target/", "/initial2/", 301)

    # def test_regular_expression(self):
    #     self.redirect_url(
    #         False,
    #         "/news/index/[a-z]/",
    #         "/my/news/$1/",
    #         "/news/index/b/",
    #         302,
    #         True,
    #     )

    #
    # def test_fallback_redirects(self):
    #     """
    #     Ensure redirects with fallback_redirect set are the last evaluated
    #     """
    #     PageNotFoundEntry.objects.create(
    #         old_path='/project/foo',
    #         new_path='/my/project/foo')
    #
    #     PageNotFoundEntry.objects.create(
    #         old_path='/project/foo/(.*)',
    #         new_path='/my/project/foo/$1',
    #         regular_expression=True)
    #
    #     PageNotFoundEntry.objects.create(
    #         old_path='/project/(.*)',
    #         new_path='/projects',
    #         regular_expression=True,
    #         fallback_redirect=True)
    #
    #     PageNotFoundEntry.objects.create(
    #         old_path='/project/bar/(.*)',
    #         new_path='/my/project/bar/$1',
    #         regular_expression=True)
    #
    #     PageNotFoundEntry.objects.create(
    #         old_path='/project/bar',
    #         new_path='/my/project/bar')
    #
    #     PageNotFoundEntry.objects.create(
    #         old_path='/second_project/.*',
    #         new_path='http://example.com/my/second_project/bar/',
    #         regular_expression=True)
    #
    #     PageNotFoundEntry.objects.create(
    #         old_path='/third_project/(.*)',
    #         new_path='http://example.com/my/third_project/bar/$1',
    #         regular_expression=True)
    #
    #     response = self.client.get('/project/foo')
    #     self.assertRedirects(response,
    #                          '/my/project/foo',
    #                          status_code=301, target_status_code=404)
    #
    #     response = self.client.get('/project/bar')
    #     self.assertRedirects(response,
    #                          '/my/project/bar',
    #                          status_code=301, target_status_code=404)
    #
    #     response = self.client.get('/project/bar/details')
    #     self.assertRedirects(response,
    #                          '/my/project/bar/details',
    #                          status_code=301, target_status_code=404)
    #
    #     response = self.client.get('/project/foobar')
    #     self.assertRedirects(response,
    #                          '/projects',
    #                          status_code=301, target_status_code=404)
    #
    #     response = self.client.get('/project/foo/details')
    #     self.assertRedirects(response,
    #                          '/my/project/foo/details',
    #                          status_code=301, target_status_code=404)
    #
    #     response = self.client.get('/second_project/details')
    #     self.assertRedirects(response,
    #                          'http://example.com/my/second_project/bar/',
    #                          status_code=301, target_status_code=404)
    #
    #     response = self.client.get('/third_project/details')
    #     self.assertRedirects(response,
    #                          'http://example.com/my/third_project/bar/details',
    #                          status_code=301, target_status_code=404)
