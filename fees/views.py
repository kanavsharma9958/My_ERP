from django.shortcuts import render, redirect
from .models import Course, StudentInvoice
from admissions.models import AdmissionApplication
from django.contrib import messages
from examinations.models import Marks

def generate_invoices_view(request):
    if request.method == 'POST':
        course_name = request.POST.get('course_enrolled')
        total_amount = request.POST.get('total_amount')
        due_date = request.POST.get('due_date')

        students = AdmissionApplication.objects.filter(course_enrolled=course_name)

        for student in students:
            if not StudentInvoice.objects.filter(student=student, due_date=due_date).exists():
                StudentInvoice.objects.create(
                    student=student,
                    total_amount=total_amount,
                    due_date=due_date
                )

        messages.success(request, f"Successfully generated invoices for {students.count()} students!")
        return redirect('generate_invoices')

    courses = AdmissionApplication.objects.values_list('course_enrolled', flat=True).distinct()
    return render(request, 'fees/generate_invoices.html', {'courses': courses})
from academics.models import Attendance 

def check_fee_status_view(request):
    invoice = None
    error_message = None
    attendance_records = None
    marks_records = None # <-- यह नई लाइन जोड़ें

    if request.method == 'POST':
        roll_number = request.POST.get('roll_number')
        try:
            student = AdmissionApplication.objects.get(roll_number=roll_number)

            # फीस, अटेंडेंस और मार्क्स की जानकारी ढूंढें
            invoice = StudentInvoice.objects.filter(student=student).latest('due_date')
            attendance_records = Attendance.objects.filter(student=student).order_by('-date')
            marks_records = Marks.objects.filter(student=student).order_by('unit_test__date')

        except AdmissionApplication.DoesNotExist:
            error_message = "No record found for this Roll Number."
        except Exception:
            # अगर कोई जानकारी नहीं मिलती है तो भी एरर न आए
            pass

    context = {
        'invoice': invoice,
        'attendance_records': attendance_records,
        'marks_records': marks_records, # <-- इसे कॉन्टेक्स्ट में जोड़ें
        'error_message': error_message,
        'student': student if 'student' in locals() else None
    }
    return render(request, 'fees/check_status.html', context)
