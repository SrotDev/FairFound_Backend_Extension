from django.contrib import admin
from .models import ComparisonHistory


@admin.register(ComparisonHistory)
class ComparisonHistoryAdmin(admin.ModelAdmin):
    list_display = ['created_at', 'freelancer1_url', 'freelancer2_url']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
