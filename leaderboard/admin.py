from django.contrib import admin
from .models import Freelancer


@admin.register(Freelancer)
class FreelancerAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialty', 'platform', 'marketplace_score', 'fairfound_score']
    list_filter = ['platform', 'specialty']
    search_fields = ['name', 'profile_url']
    ordering = ['-fairfound_score']
