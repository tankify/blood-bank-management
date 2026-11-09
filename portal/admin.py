from django.contrib import admin
from .models import BloodBank, BloodCamp, BloodRequest, Donor

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ("name", "blood_group", "city", "is_available")
    list_filter = ("blood_group", "city", "is_available")
    search_fields = ("name", "city")

@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ("requester_name", "blood_group", "city", "units_needed")
    list_filter = ("blood_group", "city")

admin.site.register(BloodBank)
admin.site.register(BloodCamp)
