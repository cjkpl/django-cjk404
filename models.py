from django.db import models
from wagtail.admin.edit_handlers import (
    FieldPanel, MultiFieldPanel, PageChooserPanel)
from wagtail.core.models import Page, Site


class PageNotFoundEntry(models.Model):
    site = models.ForeignKey(
        Site, related_name='pagenotfound_entries', on_delete=models.CASCADE, verbose_name="Website / Domain")

    url = models.CharField(max_length=200, verbose_name="Old Path / Redirect From (URL)")
    redirect_to_url = models.CharField(max_length=200, null=True, blank=True, verbose_name="New Path / Redirect To ("
                                                                                           "URL)")
    redirect_to_page = models.ForeignKey(
        Page, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Redirect To (Wagtail Page)")

    created = models.DateTimeField(auto_now_add=True)
    last_hit = models.DateTimeField(verbose_name="Last Hit (Last Page View)")
    hits = models.PositiveIntegerField(default=1, verbose_name="Number of Hits (Page Views)")
    permanent = models.BooleanField(default=False)

    regular_expression = models.BooleanField(default=False, verbose_name="Regular Expression")

    panels = [
        MultiFieldPanel(
            [
                FieldPanel('site'),
                FieldPanel('url'),
                FieldPanel('regular_expression'),
            ], heading='Old Path / Redirect From'),
        MultiFieldPanel(
            [
                FieldPanel('last_hit'),
                FieldPanel('hits'),
            ], heading='general', classname='collapsible'),
        MultiFieldPanel(
            [
                PageChooserPanel('redirect_to_page'),
                FieldPanel('redirect_to_url'),
                FieldPanel('permanent'),
            ], heading='New Path / Redirect To', classname='collapsible'),
    ]

    @property
    def redirect_to(self):
        if self.redirect_to_page:
            return self.redirect_to_page.url
        return self.redirect_to_url

    def __str__(self):
        return self.url

    class Meta:
        verbose_name_plural = "page not found redirects"
        ordering = ('-hits',)
