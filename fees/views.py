from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from admissions.models import AdmissionApplication
from .models import StudentInvoice, Course, Payment, YearlyFee
from academics.models import Semester # <-- Semester को 'academics.models' से इम्पोर्ट किया गया है
from django.http import JsonResponse
from django.db.models import Sum
from datetime import datetime

def check_fee_status_view(request):
    invoice = None
    error_message = None
    student = None

    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        if roll_number:
            try:
                student = AdmissionApplication.objects.get(roll_number__iexact=roll_number)
                invoice = StudentInvoice.objects.filter(student=student).last()
            except AdmissionApplication.DoesNotExist:
                error_message = "No record found for this Roll Number."
            except Exception as e:
                error_message = f"An error occurred: {e}"
        else:
            error_message = "Please enter a roll number."

    context = {
        'invoice': invoice,
        'error_message': error_message,
        'student': student
    }
    return render(request, 'fees/check_status.html', context)

@staff_member_required
def generate_invoices_view(request):
    if request.method == 'POST':
        course_id = request.POST.get('course')
        due_date = request.POST.get('due_date')
        
        if not all([course_id, due_date]):
            messages.error(request, "Course and Due Date are required.")
            return redirect('generate_invoices')

        course = Course.objects.get(id=course_id)
        students = AdmissionApplication.objects.filter(course=course, status='CONFIRMED')
        count = 0

        if course.fee_structure_type == 'SEMESTER_WISE':
            semester_id = request.POST.get('semester')
            if not semester_id:
                messages.error(request, "Semester is required for this course.")
                return redirect('generate_invoices')
            
            semester = Semester.objects.get(id=semester_id)
            total_amount = semester.semester_fee
            description = f"Fee for {semester}"
            
            for student in students:
                if not StudentInvoice.objects.filter(student=student, semester=semester).exists():
                    StudentInvoice.objects.create(
                        student=student, semester=semester, description=description,
                        total_amount=total_amount, due_date=due_date
                    )
                    count += 1

        elif course.fee_structure_type == 'YEARLY':
            year = request.POST.get('year')
            if not year:
                messages.error(request, "Year is required for this course.")
                return redirect('generate_invoices')

            yearly_fee = YearlyFee.objects.get(course=course, year=year)
            total_amount = yearly_fee.fee_amount
            description = f"Fee for Year {year}"

            for student in students:
                if not StudentInvoice.objects.filter(student=student, description=description).exists():
                    StudentInvoice.objects.create(
                        student=student, description=description,
                        total_amount=total_amount, due_date=due_date
                    )
                    count += 1
        
        if count > 0:
            messages.success(request, f"{count} invoices generated successfully.")
        else:
            messages.info(request, "No new invoices were generated. They might already exist for all selected students.")
        
        return redirect('generate_invoices')

    courses = Course.objects.all()
    context = {'courses': courses}
    return render(request, 'fees/generate_invoices.html', context)

@staff_member_required
def payment_receipt_view(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    context = {
        'payment': payment
    }
    return render(request, 'fees/receipt.html', context)

def get_course_fee_details_view(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        details = {'fee_structure_type': course.fee_structure_type}
        if course.fee_structure_type == 'SEMESTER_WISE':
            options = list(course.semesters.values('id', 'semester_number', 'semester_fee'))
            details['options'] = options
        elif course.fee_structure_type == 'YEARLY':
            options = list(course.yearly_fees.values('id', 'year', 'fee_amount'))
            details['options'] = options
        return JsonResponse(details)
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)

@staff_member_required
def fee_collection_report_view(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    
    payments = Payment.objects.all()
    
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        payments = payments.filter(payment_date__range=[start_date, end_date])

    total_collection = payments.aggregate(total=Sum('amount'))['total'] or 0

    context = {
        'payments': payments.order_by('-payment_date'),
        'total_collection': total_collection,
        'start_date': start_date_str,
        'end_date': end_date_str,
    }
    return render(request, 'fees/fee_report.html', context)