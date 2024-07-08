from django.contrib import admin
from .models import *


class LeadsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'company', 'next_action_owner','owner','status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'company','next_action_owner','owner','status', 'created_at')
    list_filter = ('name', 'company', 'next_action_owner','owner','status','created_at')
# Register your models here.
admin.site.register(Leads,LeadsAdmin)
