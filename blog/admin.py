from django.contrib import admin
from blog.models import Entry, Term
from filebrowser.widgets import FileInput
from django.db import models


class EntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'term', 'style', 'mod_date',)
    search_fields = ('content_md',)
    list_filter = ('style', 'term')
    fieldsets = [
        ('Post',
         {
             'classes':['wide', 'extrapretty'],
             'fields': ['title', 'image', 'desc',
                        'content_md', 'tags']
         }),
        ('Information',
         {
             'fields': ['style', 'start_date']
         }),

        #('Outbound Link',
        #   {'fields':['ref_source', 'ref_link']}),
    ]
    form_field_overrides = {
        models.ImageField: {'widget': FileInput}
    }

admin.site.register(Entry, EntryAdmin)
admin.site.register(Term)
