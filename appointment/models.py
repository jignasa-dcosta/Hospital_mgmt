# models.py
from django.contrib.auth.models import AbstractUser,Group, Permission
from django.db import models

# Gender Choices
GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

DEPARTMENT_CATEGORY_CHOICES = [
    ('Cardiology', 'Cardiology'),
    ('Neurology', 'Neurology'),
    ('Orthopedics', 'Orthopedics'),
    ('Pediatrics', 'Pediatrics'),
    ('Radiology', 'Radiology'),
    ('Emergency', 'Emergency'),
    ('Oncology', 'Oncology'),
    ('Anaesthesiology', 'Anaesthesiology'),
    ('Gastroenterology', 'Gastroenterology'),
]

TIME_SLOT_CHOICES = [
        ('08:00 AM', '08:00 AM'),
        ('08:30 AM', '08:30 AM'),
        ('09:00 AM', '09:00 AM'),
        ('09:30 AM', '09:30 AM'),
        ('10:00 AM', '10:00 AM'),
        ('10:30 Am', '10:30 AM'),
        ('11:00 AM', '11:00 AM'),
        ('11:30 AM', '11:30 AM'),
        ('12:00 PM', '12:00 PM'),
        ('12:30 PM', '12:30 PM'),
        ('01:00 PM', '01:00 PM'),
        ('01:30 PM', '01:30 PM'),
        ('02:00 PM', '02:00 PM'),
        ('02:30 PM', '02:30 PM'),
        ('03:00 PM', '03:00 PM'),
        ('03:30 PM', '03:30 PM'),
        ('04:00 PM', '04:00 PM'),
        ('04:30 PM', '04:30 PM'),
        ('05:00 PM', '05:00 PM'),
        ('05:30 PM', '05:30 PM'),
]


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Use email as the unique identifier
    is_patient = models.BooleanField(default=False, db_index=True)
    is_doctor = models.BooleanField(default=False, db_index=True)
    user_permissions=models.ManyToManyField('auth.Permission',related_name='account_user_permission_set',blank=True)
    groups = models.ManyToManyField('auth.Group',related_name='account_user_set',blank=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        if self.is_doctor:
            return f"{self.first_name} {self.last_name}"
        return self.email

    class Meta:
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]

class PatientProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='patient_profile')
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return self.user.get_full_name()
    
# Specialization model
class Department(models.Model):
    name = models.CharField(max_length=100, choices=DEPARTMENT_CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class DoctorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor_profile')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=15)
    role = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='departemnt')    
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    profile_picture = models.ImageField(upload_to='doctor_profiles/', blank=True, null=True)
    description = models.TextField(default="No description available.")  # Add description field

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} - {self.department}"
    
from django.contrib.auth import get_user_model
CustomUser = get_user_model()

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments', limit_choices_to={'is_patient': True})
    doctor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appointments_as_doctor', limit_choices_to={'is_doctor': True})
    # department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='department')
    date = models.DateField()
    time = models.CharField(max_length=10, choices=TIME_SLOT_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Scheduled')

    def save(self, *args, **kwargs):
        # Add any custom logic here if needed
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Appointment with {self.doctor.get_full_name()} on {self.date} at {self.time}"

class AppointmentDetail(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='details')
    diagnosis = models.TextField()
    prescription = models.TextField()
    fee_status = models.CharField(max_length=10, choices=[('', 'Select Status'),('Paid', 'Paid'), ('Unpaid', 'Unpaid')],)
    additional_notes = models.TextField(blank=True, null=True)
    revisit_required = models.CharField(max_length=10, choices=[('Yes', 'Yes'), ('No', 'No')],)
    revisit_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Details for {self.appointment}"

