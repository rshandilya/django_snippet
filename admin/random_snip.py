
###  GenericForeignKey in admin ######
class PollAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': (
                'question'
                # ...
            )
        }),
        (_('page/article'), {
            'classes': ('grp-collapse grp-open',),
            'fields': ('content_type', 'object_id', )
        }),
    )
    autocomplete_lookup_fields = {
        'generic': [['content_type', 'object_id']],
    }
