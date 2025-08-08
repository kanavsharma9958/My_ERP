from django import forms
# बदला हुआ: Subject को academics.models से इम्पोर्ट किया
from .models import AdmissionApplication
from academics.models import Subject
from core.models import College

class AdmissionApplicationForm(forms.ModelForm):
    college = forms.ModelChoiceField(
        queryset=College.objects.all(),
        empty_label="--- Select a College ---",
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    # Major और Minor सब्जेक्ट्स के लिए नए फील्ड्स
    major_subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.filter(subject_type='MAJOR'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    minor_subjects = forms.ModelMultipleChoiceField(
        queryset=Subject.objects.filter(subject_type='MINOR'),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = AdmissionApplication
        # 'major_subjects' और 'minor_subjects' को लिस्ट में जोड़ा गया
        fields = [
            'college', 'samarth_registration_no', 'full_name', 'father_name', 
            'mother_name', 'date_of_birth', 'mobile_number', 'category', 
            'course_enrolled', 'major_subjects', 'minor_subjects'
        ]

        widgets = {
            'samarth_registration_no': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'mobile_number': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'course_enrolled': forms.TextInput(attrs={'class': 'form-control'}),
        }