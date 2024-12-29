from django.contrib import admin
from .models import CustomUser, PatientProfile, DoctorProfile,Appointment,Department,AppointmentDetail
from django.contrib.auth.admin import UserAdmin

class CustomUserAdimn(UserAdmin):
    list_display = ['username','email','first_name', 'last_name', 'is_patient', 'is_doctor']
admin.site.register(CustomUser, CustomUserAdimn)

class PatientAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'gender', 'contact_number']
admin.site.register(PatientProfile, PatientAdmin)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'gender', 'contact_number','role','fees','profile_picture','description']
admin.site.register(DoctorProfile, DoctorAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['patient','doctor', 'date', 'time','status']
admin.site.register(Appointment, AppointmentAdmin)

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id','name'] 
admin.site.register(Department,DepartmentAdmin)

class AppointmentDetailAdmin(admin.ModelAdmin):
    list_display = ['appointment','diagnosis','prescription','fee_status','additional_notes','revisit_required','revisit_date']
admin.site.register(AppointmentDetail,AppointmentDetailAdmin)

