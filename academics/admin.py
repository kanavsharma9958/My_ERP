from django.contrib import admin
from .models import Faculty, Subject, ClassSchedule, Attendance, Semester

class SemesterInline(admin.TabularInline):
    model = Semester
    extra = 1
    fields = ('semester_number', 'semester_fee')

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ('user', 'college')
    list_filter = ('college',)

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'course', 'semester_number', 'semester_fee')
    list_filter = ('course__college', 'course')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'course', 'college')
    list_filter = ('college', 'course')
    search_fields = ('name', 'code')

@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'faculty', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('semester__course__college', 'semester__course', 'faculty', 'day_of_week')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'scheduled_class', 'date', 'status')
    list_filter = ('scheduled_class__semester__course__college', 'date', 'status')
    search_fields = ('student__full_name',)