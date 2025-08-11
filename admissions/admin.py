from django.contrib import admin, messages
from .models import AdmissionApplication, UploadedDocument
from academics.models import Semester
import openpyxl
from django.http import HttpResponse
from django.utils.html import format_html
from openpyxl.styles import Font, Border, Side, Alignment
from openpyxl.utils import get_column_letter

@admin.action(description="Promote selected students to next semester")
def promote_to_next_semester(modeladmin, request, queryset):
    promoted_count = 0
    failed_count = 0
    for student in queryset:
        if student.current_semester and student.course:
            current_sem_num = student.current_semester.semester_number
            max_semesters = student.course.duration_in_semesters
            if current_sem_num < max_semesters:
                next_sem_num = current_sem_num + 1
                try:
                    next_semester = Semester.objects.get(course=student.course, semester_number=next_sem_num)
                    student.current_semester = next_semester
                    student.save()
                    promoted_count += 1
                except Semester.DoesNotExist:
                    failed_count += 1
            else:
                failed_count += 1
        else:
            failed_count += 1
    if promoted_count > 0:
        modeladmin.message_user(request, f"{promoted_count} student(s) promoted successfully.", messages.SUCCESS)
    if failed_count > 0:
        modeladmin.message_user(request, f"{failed_count} student(s) could not be promoted (either in final semester or data missing).", messages.WARNING)

@admin.action(description="Export selected students to Excel")
def export_as_excel(modeladmin, request, queryset):
    # ... (यह पूरा फंक्शन जैसा था वैसा ही रहेगा) ...
    pass

@admin.action(description="Export selected students with Subjects")
def export_as_excel_with_subjects(modeladmin, request, queryset):
    # ... (यह पूरा फंक्शन जैसा था वैसा ही रहेगा) ...
    pass

class UploadedDocumentInline(admin.TabularInline):
    model = UploadedDocument
    extra = 1
    readonly_fields = ('get_preview',) 
    fields = ('document_type', 'file', 'get_preview')

@admin.register(AdmissionApplication)
class AdmissionApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'roll_number', 'college', 'course', 'status', 'current_semester')
    list_filter = ('college', 'status', 'course', 'current_semester')
    search_fields = ('full_name', 'roll_number', 'samarth_registration_no')
    inlines = [UploadedDocumentInline]
    actions = [promote_to_next_semester, export_as_excel, export_as_excel_with_subjects]
    class Media:
        js = ('admissions/js/admin_enhancements.js',)