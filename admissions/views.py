from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import AdmissionApplicationForm
from .models import AdmissionApplication, UploadedDocument
from academics.models import Subject, Semester
from fees.models import Course
from reception.models import DocumentType
import json

def admission_form_view(request):
    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save()
            major_subject_ids = request.POST.getlist('major_subjects')
            minor_subject_ids = request.POST.getlist('minor_subjects')
            application.major_subjects.set(major_subject_ids)
            application.minor_subjects.set(minor_subject_ids)
            for key, uploaded_file in request.FILES.items():
                if key.startswith('document_'):
                    doc_type_id = key.split('_')[1]
                    try:
                        document_type = DocumentType.objects.get(id=doc_type_id)
                        UploadedDocument.objects.create(
                            application=application,
                            document_type=document_type,
                            file=uploaded_file
                        )
                    except DocumentType.DoesNotExist:
                        pass
            return redirect('admission_success')
        else:
            courses_data = {course.id: course.subject_selection_type for course in Course.objects.all()}
            context = {'form': form, 'courses_data': json.dumps(courses_data)}
            return render(request, 'admissions/admission_form.html', context)
    
    form = AdmissionApplicationForm()
    courses_data = {course.id: course.subject_selection_type for course in Course.objects.all()}
    context = {'form': form, 'courses_data': json.dumps(courses_data)}
    return render(request, 'admissions/admission_form.html', context)

def success_view(request):
    return render(request, 'admissions/success.html')

def id_card_view(request, roll_number):
    student = get_object_or_404(AdmissionApplication, roll_number=roll_number)
    student_photo = None
    try:
        photo_doc = student.documents.get(document_type__name__iexact='Student Photograph')
        student_photo = photo_doc.file
    except UploadedDocument.DoesNotExist:
        pass
    context = {'student': student, 'student_photo': student_photo}
    return render(request, 'admissions/id_card.html', context)

def get_required_documents_view(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        documents = list(course.required_documents.values('id', 'name', 'is_required'))
        return JsonResponse({'documents': documents})
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)

def get_subjects_for_course_view(request, course_id):
    try:
        subjects = list(Subject.objects.filter(course_id=course_id).values('id', 'name'))
        return JsonResponse({'subjects': subjects})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

def get_courses_for_college_view(request, college_id):
    try:
        courses = list(Course.objects.filter(college_id=college_id).values('id', 'name'))
        return JsonResponse({'courses': courses})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)

def get_semesters_for_course_view(request, course_id):
    try:
        semesters = list(Semester.objects.filter(course_id=course_id).order_by('semester_number').values('id', 'semester_number'))
        return JsonResponse({'semesters': semesters})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=404)