from django.contrib import admin
from .models import AdmissionApplication

@admin.action(description="Print selected students list")
def print_student_list(modeladmin, request, queryset):
    # This will be implemented later
    pass

@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'roll_number', 'college', 'course_enrolled', 'status')
    list_filter = ('college', 'status', 'course_enrolled')
    search_fields = ('full_name', 'roll_number', 'samarth_registration_no')
    list_editable = ('status',)
    actions = [print_student_list]