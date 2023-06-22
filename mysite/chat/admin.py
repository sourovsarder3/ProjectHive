from django.contrib import admin
from django.contrib.sessions.models import Session
from . import models


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']


admin.site.register(models.User)
admin.site.register(models.Thread)
admin.site.register(models.ChatMessage)
admin.site.register(models.WorkSpace)
admin.site.register(models.WorkspaceMembership)
admin.site.register(models.Channel)
admin.site.register(models.PrivateChannelMembership)
admin.site.register(models.ChannelMessage)
admin.site.register(models.Invitation)
admin.site.register(Session, SessionAdmin)
admin.site.register(models.SeenByChannel)
