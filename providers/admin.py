from django.contrib import admin
from .models import Provider

@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
    list_display = ("name", "class_path", "is_active", "priority")
    list_editable = ("is_active", "priority")
    ordering = ("priority",)
