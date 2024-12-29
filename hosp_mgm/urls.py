"""
URL configuration for hosp_mgm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from appointment import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('patient_index',views.patient_index,name='patient_index'),
    path('patient_signup/',views.patient_signup,name='patient_signup'),
    path('doctor_signup/',views.doctor_signup,name='doctor_signup'),
    path('signin/',views.signin,name='signin'),
    path('signout/',views.signout,name='signout'),
    path('patient_dashboard/',views.patient_dashboard,name='patient_dashboard'),
    path('doctor_dashboard/',views.doctor_dashboard,name='doctor_dashboard'),
    path('book_appointment/',views.book_appointment,name='book_appointment'),
    path('appointment_history/', views.appointment_history, name='appointment_history'),
    path('cancel-appointment/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('doctor_appointment_detail/<int:pid>/', views.doctor_appointment_detail,name='doctor_appointment_detail'),
    path('doctor_list/',views.doctor_list,name='doctor_list'),
    path('appointment/<int:appointment_id>/details/', views.patient_appointment_detail, name='patient_appointment_detail'),
    path('doctor/<int:doctor_id>/profile/', views.doctor_profile, name='doctor_profile'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)