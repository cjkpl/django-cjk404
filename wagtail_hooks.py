from wagtail.contrib.modeladmin.helpers import PermissionHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import PageNotFoundEntry


class PageNotFoundPermissionHelper(PermissionHelper):
    def user_can_create(self, user):
        return False


@modeladmin_register
class PageNotFoundEntryAdmin(ModelAdmin):
    permission_helper_class = PageNotFoundPermissionHelper
    model = PageNotFoundEntry
    menu_label = '404 Redirects'
    list_display = (
        'url', 'site', 'hits', 'redirect_to', 'permanent', 'created', 'regular_expression')
    list_filter = ('permanent', 'regular_expression', 'site')
    menu_icon = 'fa-frown-o'
