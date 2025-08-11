from django.db import models
from django.contrib.auth.models import User
from core.models import College

class Faculty(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    college = models.ForeignKey(College, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name() or self.user.username

class Semester(models.Model):
    course = models.ForeignKey('fees.Course', on_delete=models.CASCADE, related_name='semesters')
    semester_number = models.PositiveIntegerField()
    semester_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Fee for this Semester (if semester-wise)")

    class Meta:
        unique_together = ('course', 'semester_number')
        ordering = ['course__name', 'semester_number']

    def __str__(self):
        return f"{self.course.name} - Semester {self.semester_number}"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    college = models.ForeignKey(College, on_delete=models.CASCADE)
    course = models.ForeignKey('fees.Course', on_delete=models.CASCADE, related_name='subjects')
    
    def __str__(self):
        return f"{self.name} ({self.course.code})"

class ClassSchedule(models.Model):
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')])
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.subject.name} on {self.day_of_week}"

class Attendance(models.Model):
    student = models.ForeignKey('admissions.AdmissionApplication', on_delete=models.CASCADE)
    scheduled_class = models.ForeignKey(ClassSchedule, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10, choices=[('PRESENT', 'Present'), ('ABSENT', 'Absent')])

    class Meta:
        unique_together = ('student', 'scheduled_class', 'date')

    def __str__(self):
        if self.student:
            return f"{self.student.full_name} - {self.date} - {self.status}"
        return f"Attendance on {self.date} - {self.status}"