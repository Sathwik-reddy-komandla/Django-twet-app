from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import User,Group
from .models import Profile,Meep

admin.site.register(Meep)

admin.site.unregister(Group)


class ProfilInline(admin.StackedInline):
    model=Profile

class UserAdmin(admin.ModelAdmin):
    model=User
    fields=['username']
    inlines=[ProfilInline]

admin.site.unregister(User)
admin.site.register(User,UserAdmin)


