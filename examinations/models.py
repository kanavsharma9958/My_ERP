from django.db import models
from core.models import College
from admissions.models import AdmissionApplication
from academics.models import Subject

class UnitTest(models.Model):
    college = models.ForeignKey(College, on_delete=models.CASCADE, verbose_name="College")
    name = models.CharField(max_length=100, verbose_name="Unit Test Name") # e.g., First Unit Test - August
    date = models.DateField(verbose_name="Test Date")

    def __str__(self):
        return f"{self.name} ({self.college.code})"

class Marks(models.Model):
    student = models.ForeignKey(AdmissionApplication, on_delete=models.CASCADE, verbose_name="Student")
    unit_test = models.ForeignKey(UnitTest, on_delete=models.CASCADE, verbose_name="Unit Test")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, verbose_name="Subject")
    marks_obtained = models.FloatField(verbose_name="Marks Obtained")
    max_marks = models.FloatField(default=100, verbose_name="Maximum Marks")

    class Meta:
        # A student can have only one marks entry per subject per unit test
        unique_together = ('student', 'unit_test', 'subject')

    def __str__(self):
        return f"{self.student.full_name} - {self.subject.code}: {self.marks_obtained}/{self.max_marks}"