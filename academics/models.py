from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User Account")
    college = models.ForeignKey('core.College', on_delete=models.CASCADE, verbose_name="College")
    employee_id = models.CharField(max_length=20, unique=True, verbose_name="Employee ID")
    full_name = models.CharField(max_length=100, verbose_name="Full Name")
    department = models.CharField(max_length=100, verbose_name="Department")

    def __str__(self):
        return self.full_name

class Subject(models.Model):
    SUBJECT_TYPE_CHOICES = [('MAJOR', 'Major'), ('MINOR', 'Minor')]
    college = models.ForeignKey('core.College', on_delete=models.CASCADE, verbose_name="College")
    course = models.ForeignKey('fees.Course', on_delete=models.CASCADE, verbose_name="Course")
    name = models.CharField(max_length=100, verbose_name="Subject Name")
    code = models.CharField(max_length=20, unique=True, verbose_name="Subject Code")
    subject_type = models.CharField(max_length=10, choices=SUBJECT_TYPE_CHOICES, default='MAJOR', verbose_name="Subject Type")

    def __str__(self):
        return f"{self.name} ({self.code}) - {self.get_subject_type_display()}"

class ClassSchedule(models.Model):
    DAY_CHOICES = [('MONDAY', 'Monday'), ('TUESDAY', 'Tuesday'), ('WEDNESDAY', 'Wednesday'), ('THURSDAY', 'Thursday'), ('FRIDAY', 'Friday'), ('SATURDAY', 'Saturday'), ('SUNDAY', 'Sunday')]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Subject")
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, verbose_name="Faculty")
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES, verbose_name="Day of the Week")
    start_time = models.TimeField(verbose_name="Start Time")
    end_time = models.TimeField(verbose_name="End Time")

    def __str__(self):
        return f"{self.subject.code} - {self.faculty.full_name} on {self.day_of_week}"

class Attendance(models.Model):
    STATUS_CHOICES = [('PRESENT', 'Present'), ('ABSENT', 'Absent')]
    student = models.ForeignKey('admissions.AdmissionApplication', on_delete=models.CASCADE, verbose_name="Student")
    scheduled_class = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE, verbose_name="Class")
    date = models.DateField(verbose_name="Date")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, verbose_name="Status")

    class Meta:
        unique_together = ('student', 'scheduled_class', 'date')

    def __str__(self):
        if self.student: return f"{self.student.full_name} - {self.status} on {self.date}"
        return f"Attendance on {self.date}"