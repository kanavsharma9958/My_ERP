from django.db import models
from django.utils import timezone
from encrypted_model_fields.fields import EncryptedCharField
import datetime

class AdmissionApplication(models.Model):
    STATUS_CHOICES = [('SUBMITTED', 'Submitted'), ('VERIFIED', 'Documents Verified'), ('CONFIRMED', 'Admission Confirmed'), ('REJECTED', 'Rejected')]
    CATEGORY_CHOICES = [('GENERAL', 'General'), ('OBC', 'OBC'), ('SC', 'SC'), ('ST', 'ST'), ('EWS', 'EWS'), ('MANAGEMENT', 'Management Quota'), ('SPORTS', 'Sports Quota')]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED', verbose_name="Application Status")
    college = models.ForeignKey('core.College', on_delete=models.CASCADE, verbose_name="College")
    roll_number = models.CharField(max_length=20, unique=True, blank=True, null=True, verbose_name="Roll Number / Unique ID")
    samarth_registration_no = models.CharField(max_length=50, unique=True, verbose_name="Samarth Portal Registration No.")
    full_name = models.CharField(max_length=100, verbose_name="Student Name")
    father_name = models.CharField(max_length=100, verbose_name="Father's Name")
    mother_name = models.CharField(max_length=100, verbose_name="Mother's Name")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    mobile_number = models.CharField(max_length=15, verbose_name="Mobile Number")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='GENERAL', verbose_name="Category")
    course_enrolled = models.CharField(max_length=100, verbose_name="Course Enrolled")
    major_subjects = models.ManyToManyField('academics.Subject', verbose_name="Major Subjects", limit_choices_to={'subject_type': 'MAJOR'}, blank=True, related_name="major_applications")
    minor_subjects = models.ManyToManyField('academics.Subject', verbose_name="Minor Subjects", limit_choices_to={'subject_type': 'MINOR'}, blank=True, related_name="minor_applications")
    total_subjects_count = models.PositiveIntegerField(null=True, blank=True, verbose_name="Total Subjects Count")
    manually_entered_subjects = models.TextField(blank=True, verbose_name="Manually Entered Subjects")
    samarth_password = EncryptedCharField(max_length=100, verbose_name="Samarth Portal Password (Encrypted)")
    application_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.college: return f"{self.full_name} ({self.college.code})"
        return self.full_name
        
    def save(self, *args, **kwargs):
        if self.status == 'CONFIRMED' and not self.roll_number and self.college:
            current_year = datetime.date.today().strftime('%Y')[2:]
            college_code = self.college.code.upper()
            last_student_count = AdmissionApplication.objects.filter(college=self.college, roll_number__startswith=f"{college_code}{current_year}").count()
            new_id_number = last_student_count + 1
            self.roll_number = f"{college_code}{current_year}{new_id_number:03d}"
        super().save(*args, **kwargs)