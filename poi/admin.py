from django.contrib import admin

# Register your models here.
from .models import PointOfInterest

@admin.register(PointOfInterest)
class PointOfInterestAdmin(admin.ModelAdmin):
    list_display = ('internal_ID', 'name', 'external_ID', 'category', 'avg_rating')
    search_fields = ('internal_ID', 'external_ID')
    list_filter = ('category', )