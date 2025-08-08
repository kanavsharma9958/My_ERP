from django.db import models
from admissions.models import AdmissionApplication
from core.models import College

class Course(models.Model):
    SUBJECT_SELECTION_CHOICES = [
        ('NONE', 'No Subjects (e.g., LLB)'),
        ('MAJOR_MINOR', 'Major/Minor Selection (e.g., B.A.)'),
        ('TOTAL_COUNT', 'Total Subject Count Only'),
        ('MANUAL_ENTRY', 'Manual Subject Entry'),
    ]

    college = models.ForeignKey(College, on_delete=models.CASCADE, verbose_name="College")
    name = models.CharField(max_length=100, unique=True, verbose_name="Course Name")
    code = models.CharField(max_length=20, unique=True, verbose_name="Course Code")
    subject_selection_type = models.CharField(
        max_length=20, 
        choices=SUBJECT_SELECTION_CHOICES, 
        default='NONE',
        verbose_name="Subject Selection Type"
    )

    def __str__(self):
        return f"{self.name} ({self.college.code})"

class StudentInvoice(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PARTIALLY_PAID', 'Partially Paid'),
        ('PAID', 'Paid'),
    ]

    college = models.ForeignKey(College, on_delete=models.CASCADE, verbose_name="College", null=True)
    student = models.ForeignKey('admissions.AdmissionApplication', on_delete=models.CASCADE, verbose_name="Student")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Amount Paid")
    due_date = models.DateField(verbose_name="Due Date")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status")

    def __str__(self):
        return f"Invoice for {self.student.full_name} - Rs. {self.total_amount}"

    @property
    def amount_due(self):
        return self.total_amount - self.amount_paid

    def save(self, *args, **kwargs):
        if not self.college:
            self.college = self.student.college
        super().save(*args, **kwargs)

class Payment(models.Model):
    invoice = models.ForeignKey(StudentInvoice, on_delete=models.CASCADE, related_name='payments', verbose_name="Invoice")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Installment Amount")
    payment_date = models.DateField(auto_now_add=True, verbose_name="Payment Date")

    def __str__(self):
        return f"Rs. {self.amount} paid for Invoice #{self.invoice.id} on {self.payment_date}"