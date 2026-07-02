from django.db import models
from django.utils import timezone

class Employee(models.Model):
    DEPARTMENT_CHOICES = [
        ('HR', 'Human Resources'),
        ('IT', 'Information Technology'),
        ('Finance', 'Finance'),
        ('Marketing', 'Marketing'),
        ('Sales', 'Sales'),
        ('Operations', 'Operations'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    ]

    # Primary key custom ID auto-generated as EMP0001, EMP0002...
    id = models.CharField(max_length=20, primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    designation = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    address = models.TextField()
    joining_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    photo = models.ImageField(upload_to='employee_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.id:
            # Find the last record by creation order to maintain sequence
            last_emp = Employee.objects.all().order_by('created_at').last()
            if not last_emp:
                self.id = 'EMP0001'
            else:
                try:
                    # Extract the numerical part from the last ID
                    last_num = int(last_emp.id.replace('EMP', ''))
                    self.id = f'EMP{last_num + 1:04d}'
                except ValueError:
                    # Fallback unique string if format isn't parseable
                    import uuid
                    self.id = f'EMP-{uuid.uuid4().hex[:6].upper()}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.id})"