from django.db import models
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, PageChooserPanel
from wagtail.core.models import Page, Site


class PageNotFoundEntry(models.Model):
    site = models.ForeignKey(
        Site,
        related_name="pagenotfound_entries",
        on_delete=models.CASCADE,
        verbose_name="Site",
    )

    url = models.CharField(
        max_length=200, verbose_name="Redirect from URL"
    )
    redirect_to_url = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name="Redirect to URL",
    )
    redirect_to_page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Redirect to Page",
    )

    created = models.DateTimeField(auto_now_add=True)
    last_hit = models.DateTimeField(verbose_name="Last Hit")
    hits = models.PositiveIntegerField(
        default=1, verbose_name="# Hits"
    )
    permanent = models.BooleanField(default=False)

    regular_expression = models.BooleanField(
        default=False, verbose_name="RegExp"
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("site"),
                FieldPanel("url"),
                FieldPanel("regular_expression"),
            ],
            heading="Old Path / Redirect From",
        ),
        MultiFieldPanel(
            [
                FieldPanel("last_hit"),
                FieldPanel("hits"),
            ],
            heading="general",
            classname="collapsible",
        ),
        MultiFieldPanel(
            [
                PageChooserPanel("redirect_to_page"),
                FieldPanel("redirect_to_url"),
                FieldPanel("permanent"),
            ],
            heading="New Path / Redirect To",
            classname="collapsible",
        ),
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
        ordering = ("-hits",)
