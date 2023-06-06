from django.contrib import admin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.admin import UserAdmin
from .models import *


class CustomUserAdmin(UserAdmin):
    include = ('date_of_birth')
    ordering = ['email']
    form = UserChangeForm
    
    list_display = (
        'email', 'uid', 'fname', 'lname','is_staff','is_active'
        )
    list_filter = (
        "email", "is_staff", "is_active",
        )

    fieldsets = (
        ('login data', {
            'fields': ('password', 'uid')
        }),
        ('Personal info', {
            'fields': ('fname', 'lname', 'email', 'date_of_birth','country','tel')
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
        ("Permissions", {
            "fields": ("is_staff", "is_active", "groups", "user_permissions")
        }),
    )
    
    add_fieldsets = (
        ('Personal info', {
            'fields': ('fname', 'lname', 'email')
        }),
        ('Additional information',{
            'fields': ('tel','country','date_of_birth')        
        }),
        ("Authentication", {
            'fields': ('password1', 'password2')
        })
    )


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)

admin.site.register(Invitation)
admin.site.register(FriendList)

admin.site.register(Follow)
admin.site.register(PageFollowed)
admin.site.register(GroupFollowed)

admin.site.register(PostHistoric)
admin.site.register(Post)
admin.site.register(PostShared)
admin.site.register(PostGroupShared)
admin.site.register(PostPageShared)

admin.site.register(PostPhoto)

admin.site.register(Comment)
admin.site.register(CommentShared)
admin.site.register(CommentGroupShared)
admin.site.register(CommentPageShared)

admin.site.register(PostLiked)
admin.site.register(PostSharedLike)
admin.site.register(PostGroupSharedLike)
admin.site.register(PostPageSharedLike)

admin.site.register(Notification)