from django.contrib import admin
from .models import Category, Post, Favourite, Profile, Gallery, Region, Chat, Message
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}

admin.site.register(Post, PostAdmin)
admin.site.register(Profile)
admin.site.register(Gallery)
admin.site.register(Chat)
admin.site.register(Message)
admin.site.register(Region, PostAdmin)
admin.site.register(Category, PostAdmin)
admin.site.register(Favourite)
