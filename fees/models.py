from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

class Course(models.Model):
    FEE_STRUCTURE_CHOICES = [
        ('SEMESTER_WISE', 'Semester Wise Fee'),
        ('YEARLY', 'Yearly Fee'),
    ]
    SUBJECT_SELECTION_CHOICES = [
        ('NONE', 'No Subjects (e.g., LLB)'),
        ('MAJOR_MINOR', 'Major/Minor Selection (e.g., B.A.)'),
    ]

    college = models.ForeignKey('core.College', on_delete=models.CASCADE, verbose_name="College")
    name = models.CharField(max_length=100, unique=True, verbose_name="Course Name")
    code = models.CharField(max_length=20, unique=True, verbose_name="Course Code")
    duration_in_semesters = models.PositiveIntegerField(default=6, verbose_name="Duration in Semesters")
    fee_structure_type = models.CharField(max_length=20, choices=FEE_STRUCTURE_CHOICES, default='SEMESTER_WISE', verbose_name="Fee Structure Type")
    subject_selection_type = models.CharField(max_length=20, choices=SUBJECT_SELECTION_CHOICES, default='NONE', verbose_name="Subject Selection Type")
    required_documents = models.ManyToManyField('reception.DocumentType', blank=True, verbose_name="Required Documents")

    def __str__(self):
        return f"{self.name} ({self.college.code})"

class YearlyFee(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='yearly_fees')
    year = models.PositiveIntegerField()
    fee_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('course', 'year')
        ordering = ['course', 'year']

    def __str__(self):
        return f"{self.course.name} - Year {self.year} Fee: {self.fee_amount}"

class StudentInvoice(models.Model):
    STATUS_CHOICES = [('PENDING', 'Pending'), ('PAID', 'Paid')]
    student = models.ForeignKey('admissions.AdmissionApplication', on_delete=models.CASCADE, verbose_name="Student")
    semester = models.ForeignKey('academics.Semester', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Semester (if applicable)")
    description = models.CharField(max_length=255, help_text="e.g., 'Year 1 Fee' or 'Semester 1 Fee'")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount")
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Amount Paid")
    due_date = models.DateField(verbose_name="Due Date")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name="Status")

    @property
    def amount_due(self):
        return self.total_amount - self.amount_paid

    def __str__(self):
        return f"Invoice for {self.student.full_name} - {self.description}"

class Payment(models.Model):
    invoice = models.ForeignKey(StudentInvoice, on_delete=models.CASCADE, related_name='payments', verbose_name="Invoice")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Installment Amount")
    payment_date = models.DateField(auto_now_add=True, verbose_name="Payment Date")

    def __str__(self):
        return f"Rs. {self.amount} paid for Invoice #{self.invoice.id}"

@receiver(post_save, sender=Payment)
def update_invoice_on_payment(sender, instance, created, **kwargs):
    if created:
        invoice = instance.invoice
        total_paid = sum(p.amount for p in invoice.payments.all())
        invoice.amount_paid = total_paid
        if invoice.amount_paid >= invoice.total_amount:
            invoice.status = 'PAID'
        else:
            invoice.status = 'PENDING'
        invoice.save()