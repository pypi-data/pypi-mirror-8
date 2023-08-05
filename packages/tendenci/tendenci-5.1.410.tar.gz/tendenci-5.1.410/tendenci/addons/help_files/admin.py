from django.contrib import admin
from django.conf import settings

from tendenci.core.perms.admin import TendenciBaseModelAdmin
from tendenci.addons.help_files.models import Topic, HelpFile, Request
from tendenci.addons.help_files.forms import HelpFileAdminForm


class HelpFileAdmin(TendenciBaseModelAdmin):

    list_display = ['question', 'level', 'status_detail', 'view_totals']
    list_filter = ['topics', 'level', 'is_faq', 'is_featured', 'is_video', 'syndicate']
    filter_horizontal = ['topics']
    search_fields = ['question', 'answer']
    fieldsets = (
        (None, {'fields': ('question', 'slug', 'answer', 'group', 'level', 'topics')}),
        ('Flags', {'fields': (
            ('is_faq', 'is_featured', 'is_video', 'syndicate'),)}),
        ('Permissions', {'fields': ('allow_anonymous_view',)}),
        ('Advanced Permissions', {'classes': ('collapse',), 'fields': (
            'user_perms',
            'member_perms',
            'group_perms',
        )}),
        ('Publishing Status', {'fields': (
            'status_detail',
        )}),
    )
    prepopulated_fields = {'slug': ['question']}
    form = HelpFileAdminForm

    class Media:
        js = (
            '%sjs/global/tinymce.event_handlers.js' % settings.STATIC_URL,
        )

admin.site.register(Topic)
admin.site.register(HelpFile, HelpFileAdmin)
admin.site.register(Request)
