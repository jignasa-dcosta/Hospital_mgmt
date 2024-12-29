from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import PatientSignUpForm, DoctorSignUpForm,SigninForm,AppointmentForm,AppointmentDetailForm,DepartmentFilterForm
from .models import CustomUser,DoctorProfile,PatientProfile,Appointment,Department,AppointmentDetail
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import PermissionDenied


def index(request):
    return render(request,"index.html")

def patient_index(request):
    return render(request,"patient_index.html")

def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_patient = True
            user.username = user.email  # Ensure username is set to email or another unique value
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
            return redirect('signin')  # Redirect to patient dashboard
        else:
            messages.error(request, form.errors)  # Display validation errors using Django messages framework
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
            user.username = user.email  # Ensure username is set to email or another unique value
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
            return redirect('signin')  # Redirect to doctor dashboard
        else:
            messages.error(request, form.errors)  # Display validation errors using Django messages framework
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
            # Authenticate using the email (mapped as username)
            user = authenticate(username=email, password=password)
            
            if user is not None:
                # Log in the user
                login(request, user)
                # return redirect('index')  # Redirect to patient index page 

                # Redirect based on user type
                if user.is_doctor:
                    return redirect('doctor_dashboard')  # Replace with your doctor's dashboard URL
                elif user.is_patient:
                    return redirect('patient_dashboard')  # Replace with your patient's dashboard URL
                else:
                    messages.error(request, "User role is not assigned.")
                    return redirect('signin')
            else:
                # Add error if authentication fails
                form.add_error(None, "Invalid email or password.")
    else:
        form = SigninForm()

    return render(request, 'signin.html', {'form': form})


@login_required
def patient_dashboard(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'patient_dashboard.html', {'appointments': appointments})

@login_required
def doctor_dashboard(request):
    appointments = Appointment.objects.filter(doctor=request.user)
    return render(request, 'doctor_dashboard.html', {'appointments': appointments})


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
            # Auto-fill the speciality based on the selected doctor
            
            appointment.save()
            return redirect('patient_dashboard')  
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})



@login_required
def appointment_history(request):
    print(f"Current User: {request.user}")  # Debugging line
    # Fetch all appointments for the logged-in patient
    appointments = Appointment.objects.filter(patient=request.user.id).order_by('-date', '-time')

    print(f"Appointments Found: {appointments}")  # Debugging line
    print(request.session.items()) # Debugging line

    return render(request, 'patient_dashboard.html', {
        'appointments': appointments
    })


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

# @login_required
# def doctor_appointment_detail(request, pid):
#     appointment = get_object_or_404(Appointment, id=pid)

#     if request.method == 'POST':
#         form = AppointmentDetailForm(request.POST)
#         if form.is_valid():
#             appointment_detail = form.save(commit=False)
#             appointment_detail.appointment = appointment
#             appointment_detail.save()
#             AppointmentDetail.objects.create(
#                 appointment=appointment,
#                 diagnosis=form.cleaned_data['diagnosis'],
#                 prescription=form.cleaned_data['prescription'],
#                 fee_status=form.cleaned_data['fee_status'],
#                 additional_notes=form.cleaned_data['additional_notes'],
#                 revisit_required=form.cleaned_data['revisit_required'],
#                 revisit_date=form.cleaned_data['revisit_date'],
#             )
#             return redirect('doctor_dashboard')  # Redirect to appointment history or another appropriate page
#     else:
#         form = AppointmentDetailForm()

#     return render(request, 'doctor_appointment_detail.html', {
#         'form': form,
#         'appointment': appointment,
#     })

@login_required
def doctor_appointment_detail(request, pid):
    appointment = get_object_or_404(Appointment, id=pid)
    appointment_detail, created = AppointmentDetail.objects.get_or_create(appointment=appointment)

    if request.method == 'POST':
        form = AppointmentDetailForm(request.POST, instance=appointment_detail)
        if form.is_valid():
            form.save()
            return redirect('doctor_dashboard')  # Redirect to doctor dashboard or another appropriate page
    else:
        form = AppointmentDetailForm(instance=appointment_detail)

    return render(request, 'doctor_appointment_detail.html', {
        'form': form,
        'appointment': appointment,
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


@login_required
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
                return redirect('patient_dashboard')  # Redirect to patient dashboard or another appropriate page

    return render(request, 'doctor_profile.html', {
        'doctor': doctor,
        'form': form,
    })

