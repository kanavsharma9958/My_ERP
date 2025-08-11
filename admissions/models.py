from django.db import models
from django.utils import timezone
from django.utils.html import format_html # <-- यह इम्पोर्ट ज़रूरी है
from encrypted_model_fields.fields import EncryptedCharField
import datetime

class AdmissionApplication(models.Model):
    status = models.CharField(max_length=20, choices=[('SUBMITTED', 'Submitted'), ('CONFIRMED', 'Admission Confirmed')], default='SUBMITTED')
    college = models.ForeignKey('core.College', on_delete=models.CASCADE)
    course = models.ForeignKey('fees.Course', on_delete=models.SET_NULL, null=True)
    current_semester = models.ForeignKey('academics.Semester', on_delete=models.SET_NULL, null=True, blank=True)
    roll_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    full_name = models.CharField(max_length=100)
    father_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    whatsapp_number = models.CharField(max_length=15, blank=True, null=True)
    samarth_registration_no = models.CharField(max_length=50, unique=True, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=20, choices=[('GENERAL', 'General'), ('OBC', 'OBC')], default='GENERAL')
    major_subjects = models.ManyToManyField('academics.Subject', blank=True, related_name="major_applications")
    minor_subjects = models.ManyToManyField('academics.Subject', blank=True, related_name="minor_applications")
    total_subjects_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total Subjects Count")
    manually_entered_subjects = models.TextField(blank=True, verbose_name="Manually Entered Subjects")
    samarth_password = EncryptedCharField(max_length=100, blank=True, null=True)
    application_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        if self.status == 'CONFIRMED' and not self.roll_number and self.course:
            current_year = datetime.date.today().strftime('%y')
            college_code = self.course.college.code.upper()
            last_student_count = AdmissionApplication.objects.filter(
                course__college=self.course.college, 
                roll_number__startswith=f"{college_code}{current_year}"
            ).count()
            new_id_number = last_student_count + 1
            self.roll_number = f"{college_code}{current_year}{new_id_number:04d}"
        
        super().save(*args, **kwargs)

class UploadedDocument(models.Model):
    application = models.ForeignKey(AdmissionApplication, on_delete=models.CASCADE, related_name='documents')
    document_type = models.ForeignKey('reception.DocumentType', on_delete=models.CASCADE)
    file = models.FileField(upload_to='student_documents/')

    def __str__(self):
        return f"{self.application.full_name} - {self.document_type.name}"

    # --- यह फंक्शन वापस जोड़ा गया है ---
    def get_preview(self):
        if self.file:
            if any(self.file.name.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
                return format_html('<a href="{0}" target="_blank"><img src="{0}" width="100" /></a>', self.file.url)
            else:
                return format_html('<a href="{0}" target="_blank">View Document</a>', self.file.url)
        return "No file uploaded"
    get_preview.short_description = "Preview"