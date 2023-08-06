from django.contrib import admin

from .models import Entry, EntryImage


class EntryImageInline(admin.TabularInline):
    model = EntryImage
    extra = 1
    readonly_fields = ['image_url']


class EntryAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'is_published',
        'published_timestamp',
    )
    search_fields = (
        'title',
        'content',
    )
    readonly_fields = (
        'slug',
        'published_timestamp',
        'author',
    )

    inlines = [
        EntryImageInline,
    ]

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()


class EntryImageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Entry, EntryAdmin)
admin.site.register(EntryImage, EntryImageAdmin)
