from django.contrib import admin

from .models import Entry, Topic


class EntryInline(admin.StackedInline):
    model = Entry
    extra = 1


class TopicAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Topic name', {'fields': ['topic_text']}),
    ]
    inlines = [EntryInline]
    list_display = ('topic_text', 'date_added', 'public')
    list_filter = ['date_added']
    search_fields = ['topic_text']


class EntryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['topic', 'entry_text']}),
    ]
    list_filter = ('topic', 'date_added')


admin.site.register(Topic, TopicAdmin)
admin.site.register(Entry, EntryAdmin)
