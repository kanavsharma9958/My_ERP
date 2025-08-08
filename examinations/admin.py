from django.contrib import admin
from .models import UnitTest, Marks

@admin.register(UnitTest)
class UnitTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'college', 'date')
    list_filter = ('college', 'date')
    search_fields = ('name',)

@admin.register(Marks)
class MarksAdmin(admin.ModelAdmin):
    list_display = ('student', 'unit_test', 'subject', 'marks_obtained', 'max_marks')
    list_filter = ('unit_test__college', 'unit_test', 'subject')
    search_fields = ('student__full_name', 'student__roll_number', 'subject__name')