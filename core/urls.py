# urls.py
from django.urls import path
from .views import UserListCreateAPIView,RegisterView, UserLoginView,UserDetailAPIView,PatientListCreateView,PatientDetailsView,AppointmentListCreateView,AppointmentDetailsView,DoctorAvailabilityListCreateView,DoctorListCreateView,DoctorDetailsView, DoctorAvailabilityDetailsView

urlpatterns = [
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('patients', PatientListCreateView.as_view(), name = ' patient-list-create'),
    path('patients/<int:pk>/', PatientDetailsView.as_view(), name ='patient-details'),
    path('appointments/', AppointmentListCreateView.as_view(), name ='create appointments'),
    path('appointments/<int:pk>/', AppointmentDetailsView.as_view(), name ='appointments create'),
    path('doctors/', DoctorListCreateView.as_view(), name = 'create doctors'),
    path('doctors/<int:pk>', DoctorDetailsView.as_view(), name = 'doctors - details'),
    path('availability', DoctorAvailabilityListCreateView.as_view(), name ="doctors-availability"),
    path('availability/<int:pk>', DoctorAvailabilityDetailsView.as_view(), name="doctor availability"),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name = "login")
]
