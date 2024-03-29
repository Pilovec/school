from django.contrib import admin
from .models import Post, Source

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'source',)
    prepopulated_fields = {'slug': ('title',)} 

admin.site.register(Post, PostAdmin)
admin.site.register(Source)
