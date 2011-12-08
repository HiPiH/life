from django.contrib.auth.models import User
from django.contrib             import admin
from django.utils.translation   import ugettext_lazy as _
from django.template.loader import render_to_string

# original layout taken from django.contrib.auth.admin
from django.contrib.auth.admin  import UserAdmin as UserAdminOld
from apps.accounts.models       import UsersAvatars

class UserAdmin(UserAdminOld):
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name','sex','birthday', 'email','metro','address')}),
        #(_('Important dates'), {'fields': ()}),
        (_('Avatars'), {'fields': ('avatar',)}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_superuser', 'is_blog_author', 'user_permissions')}),
        (_('Groups'), {'fields': ('groups',)}),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active','sex','birthday', )
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'is_blog_author','sex')
    
    class Media:
        js = (
              '/media/fckeditor/fckeditor.js',
              '/media/fckeditor/_media/textarea_all.js',
              )

# We have to unregister it, and then reregister
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class UsersAvatarsAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'who_upload', 'avatar_preview')
    list_filter = ('title', 'owner', 'who_upload',)
    
    def avatar_preview(self, obj):
        return render_to_string("admin/accounts/avatar_preview.html",{'avatar':obj})
            
    avatar_preview.allow_tags = True

    
admin.site.register(UsersAvatars, UsersAvatarsAdmin)