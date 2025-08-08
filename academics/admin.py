from django.contrib import admin
from .models import Faculty, Subject, ClassSchedule, Attendance

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'full_name', 'department', 'college')
    list_filter = ('college', 'department')
    search_fields = ('full_name', 'employee_id')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'course', 'college')
    list_filter = ('college', 'course')
    search_fields = ('name', 'code')

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'faculty', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'faculty', 'subject__college')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'scheduled_class', 'date', 'status')
    list_filter = ('status', 'date', 'scheduled_class__subject__college')
    search_fields = ('student__full_name', 'student__roll_number')