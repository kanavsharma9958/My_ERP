from django.contrib import admin
from .models import Course, StudentInvoice, Payment, YearlyFee
from academics.admin import SemesterInline
from django.urls import reverse
from django.utils.html import format_html

class YearlyFeeInline(admin.TabularInline):
    model = YearlyFee
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'college', 'fee_structure_type')
    list_filter = ('college', 'fee_structure_type')
    search_fields = ('name', 'code')
    filter_horizontal = ('required_documents',)
    inlines = [SemesterInline, YearlyFeeInline]

@admin.register(StudentInvoice)
class StudentInvoiceAdmin(admin.ModelAdmin):
    list_display = ('student', 'description', 'total_amount', 'amount_paid', 'status')
    list_filter = ('student__college', 'status', 'semester')
    search_fields = ('student__full_name', 'student__roll_number')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'invoice', 'amount', 'payment_date', 'view_receipt_link')
    list_filter = ('invoice__student__college', 'payment_date')
    search_fields = ('invoice__student__full_name',)
    
    def view_receipt_link(self, obj):
        url = reverse('payment_receipt', args=[obj.id])
        return format_html('<a href="{}" target="_blank">View Receipt</a>', url)
    view_receipt_link.short_description = "Receipt"