from django.contrib import admin
from .models import Course, StudentInvoice, Payment

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    # 'requires_subject_selection' को बदलकर 'subject_selection_type' कर दिया गया है
    list_display = ('name', 'code', 'college', 'subject_selection_type')
    list_filter = ('college',)
    search_fields = ('name', 'code')

@admin.register(StudentInvoice)
class StudentInvoiceAdmin(admin.ModelAdmin):
    list_display = ('student', 'college', 'total_amount', 'amount_paid', 'status')
    list_filter = ('college', 'status')
    search_fields = ('student__full_name', 'student__roll_number')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('get_student', 'invoice', 'amount', 'payment_date')
    list_filter = ('invoice__college', 'payment_date')
    search_fields = ('invoice__student__full_name', 'invoice__student__roll_number')

    @admin.display(description='Student')
    def get_student(self, obj):
        return obj.invoice.student