from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from .models import Faculty, ClassSchedule, Attendance, Subject
from admissions.models import AdmissionApplication
from examinations.models import UnitTest, Marks
from django.utils import timezone

# --- यह नया लॉगिन व्यू है ---
def faculty_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and hasattr(user, 'faculty'):
                login(request, user)
                return redirect('faculty_dashboard')
            else:
                form.add_error(None, "Invalid credentials or not a faculty account.")
    else:
        form = AuthenticationForm()
    return render(request, 'academics/faculty_login.html', {'form': form})

def is_faculty(user):
    return hasattr(user, 'faculty')

@login_required
@user_passes_test(is_faculty)
def faculty_dashboard_view(request):
    today = timezone.now().strftime('%A')
    faculty = request.user.faculty
    schedule = ClassSchedule.objects.filter(faculty=faculty, day_of_week=today).order_by('start_time')
    context = {
        'schedule': schedule,
        'today': today
    }
    return render(request, 'academics/faculty_dashboard.html', context)

@login_required
@user_passes_test(is_faculty)
def mark_attendance_view(request, schedule_id):
    schedule = get_object_or_404(ClassSchedule, id=schedule_id)
    students = AdmissionApplication.objects.filter(college=schedule.college, course=schedule.course, status='CONFIRMED')
    
    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    scheduled_class=schedule,
                    date=timezone.now().date(),
                    defaults={'status': status}
                )
        return redirect('faculty_dashboard')

    context = {
        'schedule': schedule,
        'students': students
    }
    return render(request, 'academics/mark_attendance.html', context)

@login_required
@user_passes_test(is_faculty)
def select_test_for_marks_view(request):
    faculty = request.user.faculty
    subjects = Subject.objects.filter(classschedule__faculty=faculty).distinct()
    unit_tests = UnitTest.objects.filter(college=faculty.college)
    context = {
        'subjects': subjects,
        'unit_tests': unit_tests
    }
    if request.method == 'POST':
        subject_id = request.POST.get('subject')
        unit_test_id = request.POST.get('unit_test')
        if subject_id and unit_test_id:
            return redirect('enter_marks', unit_test_id=unit_test_id, subject_id=subject_id)
    return render(request, 'academics/select_test_form.html', context)

@login_required
@user_passes_test(is_faculty)
def enter_marks_view(request, unit_test_id, subject_id):
    unit_test = get_object_or_404(UnitTest, id=unit_test_id)
    subject = get_object_or_404(Subject, id=subject_id)
    students = AdmissionApplication.objects.filter(course=subject.course, status='CONFIRMED')
    
    if request.method == 'POST':
        for student in students:
            marks_obtained = request.POST.get(f'marks_{student.id}')
            max_marks = request.POST.get(f'max_marks_{student.id}')
            if marks_obtained and max_marks:
                Marks.objects.update_or_create(
                    student=student,
                    unit_test=unit_test,
                    subject=subject,
                    defaults={'marks_obtained': int(marks_obtained), 'max_marks': int(max_marks)}
                )
        return redirect('select_test_for_marks')
        
    context = {
        'unit_test': unit_test,
        'subject': subject,
        'students': students
    }
    return render(request, 'academics/enter_marks_form.html', context)