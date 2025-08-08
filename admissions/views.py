from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import AdmissionApplicationForm
from .models import AdmissionApplication
import json # json को इम्पोर्ट करें

def admission_form_view(request):
    if request.method == 'POST':
        form = AdmissionApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admission_success') 
    else:
        form = AdmissionApplicationForm()
    
    # सभी कोर्सेज और उनकी सेटिंग्स का एक डेटा बनाना
    from fees.models import Course
    courses_with_subject_requirement = {
        course.id: course.requires_subject_selection 
        for course in Course.objects.all()
    }

    context = {
        'form': form,
        'courses_data': json.dumps(courses_with_subject_requirement) # डेटा को JavaScript के लिए तैयार करना
    }
    return render(request, 'admissions/admission_form.html', context)

# ... बाकी के views (success_view, id_card_view) वैसे ही रहेंगे ...
def success_view(request):
    return render(request, 'admissions/success.html')

def id_card_view(request, roll_number):
    student = get_object_or_404(AdmissionApplication, roll_number=roll_number)
    context = {'student': student}
    return render(request, 'admissions/id_card.html', context)