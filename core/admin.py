from django.contrib import admin
from .models import College

@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    # नए फील्ड्स को लिस्ट में जोड़ा गया
    list_display = ('name', 'code', 'contact_number', 'email')
    search_fields = ('name', 'code')