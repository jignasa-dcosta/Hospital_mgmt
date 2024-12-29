from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, PatientProfile, DoctorProfile, Appointment, AppointmentDetail,Department

# Gender Choices
GENDER_CHOICES = [
    ('', 'Select Gender'),
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
]

DEPARTMENT_CATEGORY_CHOICES = [
    ('', 'Select Department'),
    ('cardiology', 'Cardiology'),
    ('neurology', 'Neurology'),
    ('orthopedics', 'Orthopedics'),
    ('pediatrics', 'Pediatrics'),
    ('radiology', 'Radiology'),
    ('emergency', 'Emergency'),
    ('oncology', 'Oncology'),
    ('anaesthesiology', 'Anaesthesiology'),
    ('gastroenterology', 'Gastroenterology'),
]


TIME_SLOT_CHOICES = [
        ('', 'Select Time Slot'),
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

STATUS_CHOICES = [
        ('Scheduled', 'Scheduled'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

class PatientSignUpForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control control rounded-0'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control control rounded-0'}))
    contact_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control control rounded-0'}))
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Enter your password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'date_of_birth', 'gender', 'contact_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control control rounded-0','placeholder': 'Enter first name','autofocus': 'autofocus'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control control rounded-0','placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control control rounded-0','placeholder': 'Enter email address'}),
        }

class DoctorSignUpForm(UserCreationForm):
    gender = forms.ChoiceField(choices=GENDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control rounded-0'}))
    contact_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Enter contact number'}))
    role = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Enter role'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label="Select Department", widget=forms.Select(attrs={'class': 'form-control rounded-0'}))
    fees = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter consultation fees'}))
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Enter your password'})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Confirm your password'})
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2', 'gender', 'contact_number', 'role', 'department','fees', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Enter first name','autofocus': 'autofocus'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control rounded-0', 'placeholder': 'Enter email address'}),
            
        }

class SigninForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control rounded-0 py-3',
                'placeholder': 'Enter your email',
                'autocomplete': 'email',  # Added for better accessibility
            }
        ),
        required=True,
        label='Email Address',
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control rounded-0 py-3',
                'placeholder': 'Enter your password',
                'autocomplete': 'current-password',  # Added for better accessibility
            }
        ),
        required=True,
        label='Password',
    )

from django.contrib.auth import get_user_model
User = get_user_model()

class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=CustomUser.objects.filter(is_doctor=True), widget=forms.Select(attrs={'class': 'form-control rounded-0 form-select','placeholder': 'Select Doctor'}),label='Doctor')
    # department = forms.ChoiceField(choices=SPECIALITY_CHOICES, widget=forms.Select(attrs={'class': 'form-control rounded-0 form-select','placeholder': 'Select Department'}),label='Department')
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control rounded-0'}))
    time = forms.ChoiceField(choices=TIME_SLOT_CHOICES, widget=forms.Select(attrs={'class': 'form-control rounded-0 form-select'}))
    
    class Meta:
        model = Appointment
        fields = ['doctor', 'date', 'time']

    def clean(self):
        cleaned_data = super().clean()
        doctor = cleaned_data.get('doctor')
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')

        if Appointment.objects.filter(doctor=doctor, date=date, time=time).exists():
            raise forms.ValidationError("This time slot is already booked for the selected doctor.")
        return cleaned_data

class AppointmentDetailForm(forms.ModelForm):
    class Meta:
        model = AppointmentDetail
        fields = ['diagnosis', 'prescription', 'fee_status', 'additional_notes', 'revisit_required', 'revisit_date']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'class': 'form-control'}),
            'prescription': forms.Textarea(attrs={'class': 'form-control'}),
            'fee_status': forms.Select(attrs={'class': 'form-control'}),
            'additional_notes': forms.Textarea(attrs={'class': 'form-control'}),
            'revisit_required': forms.Select(attrs={'class': 'form-control'}),
            'revisit_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    def clean_revisit_date(self):
        revisit_required = self.cleaned_data.get('revisit_required')
        revisit_date = self.cleaned_data.get('revisit_date')

        if revisit_required and not revisit_date:
            raise forms.ValidationError("Please specify a revisit date if revisit is required.")
        return revisit_date
    
class DepartmentFilterForm(forms.Form):
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False, empty_label="All Departments", widget=forms.Select(attrs={'class': 'form-control form-select rounded-0'}))