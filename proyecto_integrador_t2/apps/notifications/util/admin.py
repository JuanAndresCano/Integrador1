from django.contrib import admin

class AbstractNotifyAdmin(admin.ModelAdmin):
    raw_id_fields = ('destinity',)
    list_display = ('destinity', 'actor', 'verb', 'read', 'public')
    list_filter = ('level', 'read')

    def get_queryset(self,requets):
        qs = super(AbstractNotifyAdmin, self).get_queryset(requets)
        return qs.prefetch_related('actor')