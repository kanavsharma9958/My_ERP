from django import forms
from .models import AdmissionApplication
from core.models import College
from fees.models import Course

class AdmissionApplicationForm(forms.ModelForm):
    college = forms.ModelChoiceField(
        queryset=College.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_college'})
    )
    
    course = forms.ModelChoiceField(
        queryset=Course.objects.none(),
        empty_label="--- Select a College First ---",
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_course'})
    )

    class Meta:
        model = AdmissionApplication
        fields = [
            'college', 'course', 'samarth_registration_no', 'full_name', 'father_name', 
            'mother_name', 'date_of_birth', 'contact_number', 'whatsapp_number', 'category', 
            'major_subjects', 'minor_subjects', 'total_subjects_count', 'manually_entered_subjects'
        ]
        widgets = {
            'samarth_registration_no': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'contact_number': forms.TextInput(attrs={'class': 'form-control'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'total_subjects_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'manually_entered_subjects': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['major_subjects'].required = False
        self.fields['minor_subjects'].required = False
        self.fields['total_subjects_count'].required = False
        self.fields['manually_entered_subjects'].required = False

        if 'college' in self.data:
            try:
                college_id = int(self.data.get('college'))
                self.fields['course'].queryset = Course.objects.filter(college_id=college_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['course'].queryset = self.instance.college.course_set.order_by('name')