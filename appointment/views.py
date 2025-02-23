from datetime import date, timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PatientSignUpForm, DoctorSignUpForm,SigninForm,AppointmentForm,AppointmentDetailForm,DepartmentFilterForm
from .models import CustomUser,DoctorProfile,PatientProfile,Appointment,Department,AppointmentDetail
from datetime import date


def index(request):
    return render(request,"index.html")

def patient_index(request):
    return render(request,"patient_index.html")

def contact(request):
    return render(request,"contact.html")

def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_patient = True
            user.username = user.email  
            user.save()
            # Create PatientProfile instance
            PatientProfile.objects.create(
                user=user,
                date_of_birth=form.cleaned_data['date_of_birth'],
                gender=form.cleaned_data['gender'],
                contact_number=form.cleaned_data['contact_number'],
            )
            # Log the user in and redirect
            login(request, user)
            return redirect('signin') 
        else:
            messages.error(request, form.errors)  
            error = "Something went wrong"
            return render(request,'patient_signup.html',{'error':error,'form':form})
    else:
        form = PatientSignUpForm()
    return render(request,'patient_signup.html',{'form': form})

def doctor_signup(request):
    if request.method == 'POST':
        form = DoctorSignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_doctor = True
            user.username = user.email 
            user.save()
            # Create DoctorProfile instance
            DoctorProfile.objects.create(
                user=user,
                gender=form.cleaned_data['gender'],
                contact_number=form.cleaned_data['contact_number'],
                role=form.cleaned_data['role'],
                department=form.cleaned_data['department'],
                fees=form.cleaned_data['fees'],
                profile_picture=form.cleaned_data.get('profile_picture', None),
            )
            login(request, user)
            return redirect('signin')  
        else:
            messages.error(request, form.errors) 
            error = "Something went wrong"
            return render(request, 'doctor_signup.html', {'error': error, 'form': form})
    else:
        form = DoctorSignUpForm()
    return render(request, 'doctor_signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SigninForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(username=email, password=password)
            
            if user is not None:
                login(request, user)

                # Redirect based on user type
                if user.is_doctor:
                    return redirect('doctor_dashboard')
                elif user.is_patient:
                    return redirect('patient_dashboard') 
                else:
                    return redirect('signin')
            else:
                # Add error if authentication fails
                form.add_error(None, "Invalid email or password.")
    else:
        form = SigninForm()

    return render(request, 'signin.html', {'form': form})


@login_required
def patient_dashboard(request):
    today = date.today()

    # Get patient's appointments
    appointments = Appointment.objects.filter(patient=request.user)

    # Get unique filter values
    unique_doctors = appointments.values_list('doctor__first_name', 'doctor__last_name', flat=False).distinct()
    unique_departments = appointments.values_list('doctor__doctor_profile__department__name', flat=True).distinct()
    unique_times = appointments.values_list('time', flat=True).distinct()

    # Get selected filter values
    selected_date = request.GET.get('date', '')
    selected_doctor = request.GET.get('doctor', '')
    selected_department = request.GET.get('department', '')
    selected_time = request.GET.get('time', '')
    selected_status = request.GET.get('status', '')

    # Apply filters
    if selected_date:
        appointments = appointments.filter(date=selected_date)

    if selected_doctor:
        first_name, last_name = selected_doctor.split()
        appointments = appointments.filter(doctor__first_name=first_name, doctor__last_name=last_name)

    if selected_department:
        appointments = appointments.filter(doctor__doctor_profile__department__name=selected_department)

    if selected_time:
        appointments = appointments.filter(time=selected_time)

    if selected_status:
        appointments = appointments.filter(status=selected_status)

    return render(request, 'patient_dashboard.html', {
        'appointments': appointments,
        'unique_doctors': unique_doctors,
        'unique_departments': unique_departments,
        'unique_times': unique_times,
    })

@login_required
def doctor_dashboard(request):
    today = date.today()

    # Get counts for scheduled and cancelled appointments
    scheduled_count = Appointment.objects.filter(date=today, status='Scheduled').count()
    cancelled_count = Appointment.objects.filter(date=today, status='Cancelled').count()

    # Get unique time values for dropdown
    unique_times = Appointment.objects.values_list('time', flat=True).distinct()

    # Get filter values from request
    selected_date = request.GET.get('date', '')
    selected_patient = request.GET.get('patient_name', '')
    selected_contact = request.GET.get('contact', '')
    selected_time = request.GET.get('time', '')
    selected_status = request.GET.get('status', '')

    # Filter appointments based on user selection
    appointments = Appointment.objects.filter(doctor=request.user)

    if selected_date:
        appointments = appointments.filter(date=selected_date)

    if selected_patient:
        appointments = appointments.filter(
            patient__first_name__icontains=selected_patient
        ) | appointments.filter(patient__last_name__icontains=selected_patient)

    if selected_contact:
        appointments = appointments.filter(patient__patient_profile__contact_number__icontains=selected_contact)

    if selected_time:
        appointments = appointments.filter(time=selected_time)

    if selected_status:
        appointments = appointments.filter(status=selected_status)

    return render(request, 'doctor_dashboard.html', {
        'appointments': appointments,
        'scheduled_count': scheduled_count,
        'cancelled_count': cancelled_count,
        'unique_times': unique_times,  # Send unique time values to the template
    })


def signout(request):
    logout(request)
    return redirect('index')


@login_required
def book_appointment(request,):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user            
            appointment.save()
            return redirect('patient_dashboard')  
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})



@login_required
def appointment_history(request):
    # Get today's date
    today = date.today()

    # Get the counts for scheduled and cancelled appointments today
    scheduled_count = Appointment.objects.filter(date=today, status='Scheduled').count()
    cancelled_count = Appointment.objects.filter(date=today, status='Cancelled').count()

    if request.user.is_doctor:
        appointments = Appointment.objects.filter(doctor=request.user).order_by('-date', '-time')
        return render(request, 'doctor_dashboard.html', {
            'appointments': appointments,
            'scheduled_count': scheduled_count,
            'cancelled_count': cancelled_count,
        })
    elif request.user.is_patient:
        appointments = Appointment.objects.filter(patient=request.user).order_by('-date', '-time')
        return render(request, 'patient_dashboard.html', {
            'appointments': appointments
        })
    else:
        return redirect('index') 


@login_required
def cancel_appointment(request, appointment_id):
    # Fetch the appointment object
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        if appointment.patient == request.user or appointment.doctor == request.user:
            if appointment.status == 'Scheduled':
                appointment.status = 'Cancelled'
                appointment.save()
                messages.success(request, "The appointment has been successfully cancelled.")
            else:
                messages.error(request, "You can only cancel scheduled appointments.")
        else:
            messages.error(request, "You do not have permission to cancel this appointment.")
    except Appointment.DoesNotExist:
        messages.error(request, "Appointment not found.")

    return redirect('appointment_history')



@login_required
def doctor_appointment_detail(request, pid):
    appointment = get_object_or_404(Appointment, id=pid)
    appointment_detail, created = AppointmentDetail.objects.get_or_create(appointment=appointment)

    # Split the prescription into a list of lines
    prescription_lines = appointment_detail.prescription.splitlines() if appointment_detail.prescription else []

    if request.method == 'POST':
        form = AppointmentDetailForm(request.POST, instance=appointment_detail)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')  
    else:
        form = AppointmentDetailForm(instance=appointment_detail)

    return render(request, 'doctor_appointment_detail.html', {
        'form': form,
        'appointment': appointment,
        'prescription_lines': prescription_lines,
    })

@login_required
def patient_appointment_detail(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    appointment_detail,created = AppointmentDetail.objects.get_or_create(appointment=appointment)

    return render(request, 'patient_appointment_detail.html', {
        'appointment': appointment,
        'appointment_detail': appointment_detail,
    })



def doctor_list(request):
    doctors = CustomUser.objects.filter(is_doctor=True)
    form = DepartmentFilterForm(request.GET or None)

    if form.is_valid():
        department = form.cleaned_data.get('department')
        if department:
            doctors = doctors.filter(doctor_profile__department=department)

    return render(request, 'doctor_list.html', {
        'form': form,
        'doctors': doctors,
    })



def doctor_profile(request, doctor_id):
    doctor = get_object_or_404(CustomUser, id=doctor_id, is_doctor=True)
    form = AppointmentForm(initial={'doctor': doctor})
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
                appointment = form.save(commit=False)
                appointment.patient = request.user
                appointment.doctor = doctor
                appointment.save()
                return redirect('patient_dashboard')  

    return render(request, 'doctor_profile.html', {
        'doctor': doctor,
        'form': form,
    })

