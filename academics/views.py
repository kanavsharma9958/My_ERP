from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import datetime

# Models from this app
from .models import ClassSchedule, Faculty, Subject, Attendance

# Models from other apps
from admissions.models import AdmissionApplication
from examinations.models import UnitTest, Marks


@login_required
def faculty_dashboard_view(request):
    # ... (यह फंक्शन वैसा ही रहेगा) ...
    today_name = datetime.date.today().strftime('%A').upper()
    try:
        faculty = request.user.faculty
        todays_classes = ClassSchedule.objects.filter(
            faculty=faculty, 
            day_of_week=today_name
        ).order_by('start_time')
    except Faculty.DoesNotExist:
        todays_classes = None
    context = {'todays_classes': todays_classes}
    return render(request, 'academics/faculty_dashboard.html', context)


@login_required
def mark_attendance_view(request, schedule_id):
    # ... (यह फंक्शन वैसा ही रहेगा) ...
    scheduled_class = get_object_or_404(ClassSchedule, id=schedule_id)
    students = AdmissionApplication.objects.filter(
        college=scheduled_class.subject.college,
        course_enrolled=scheduled_class.subject.course.name
    )
    if request.method == 'POST':
        today = datetime.date.today()
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student, scheduled_class=scheduled_class, date=today,
                    defaults={'status': status}
                )
        return redirect('faculty_dashboard')
    return render(request, 'academics/mark_attendance.html', {'students': students, 'class': scheduled_class})


@login_required
def select_test_for_marks_view(request):
    # ... (यह फंक्शन वैसा ही रहेगा) ...
    try:
        faculty = request.user.faculty
        subjects = Subject.objects.filter(classschedule__faculty=faculty).distinct()
        unit_tests = UnitTest.objects.filter(college=faculty.college)
    except Faculty.DoesNotExist:
        subjects = None
        unit_tests = None
    context = {'subjects': subjects, 'unit_tests': unit_tests}
    return render(request, 'academics/select_test_form.html', context)


@login_required
def enter_marks_view(request, unit_test_id, subject_id):
    # ... (यह फंक्शन वैसा ही रहेगा) ...
    unit_test = get_object_or_404(UnitTest, id=unit_test_id)
    subject = get_object_or_404(Subject, id=subject_id)
    students = AdmissionApplication.objects.filter(
        college=subject.college,
        course_enrolled=subject.course.name
    )
    if request.method == 'POST':
        for student in students:
            marks_obtained = request.POST.get(f'marks_{student.id}')
            if marks_obtained:
                Marks.objects.update_or_create(
                    student=student, unit_test=unit_test, subject=subject,
                    defaults={'marks_obtained': float(marks_obtained)}
                )
        return redirect('faculty_dashboard')
    marks_data = {
        mark.student.id: mark.marks_obtained 
        for mark in Marks.objects.filter(student__in=students, unit_test=unit_test, subject=subject)
    }
    context = {
        'students': students, 'unit_test': unit_test,
        'subject': subject, 'marks_data': marks_data,
    }
    return render(request, 'academics/enter_marks_form.html', context)