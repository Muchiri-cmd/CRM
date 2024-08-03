from django.contrib import admin
from .models import User

# Register your models here.
admin.ModelAdmin
class UserAdmin(admin.ModelAdmin):
  list_display = ['username', 'email', 'is_manager', 'is_employee', 'is_superuser']

admin.site.register(User, UserAdmin)
