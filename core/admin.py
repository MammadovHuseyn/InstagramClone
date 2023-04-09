from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
# Register your models here.

@admin.register(CustomUser)
class CustomAdmin(UserAdmin):
    list_display = ('username', 'email')
    fieldsets = UserAdmin.fieldsets + (
        ('Change Avatar', {
            "fields": (
                    ['image' , ]               
                
            ),
        }), 
    
    )
    

@admin.register(Posts)
class PostsAdmin(admin.ModelAdmin):
    list_display = ( 'author',)

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('name' , 'slug')

@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    pass

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

