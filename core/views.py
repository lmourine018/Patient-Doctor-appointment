# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializer import UserSerializer,PatientSerializer,RegisterSerializer, UserLoginSerializer, DoctorSerializer, DoctorAvailabilitySerializer,AppointmentSerializer
from django.shortcuts import get_object_or_404
from .models import User, Patient,Doctor,DoctorAvailability,Appointment
from django.contrib.auth import login as django_login


class UserListCreateAPIView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "user_type": user.user_type,
                    "phone_number": user.phone_number,
                    "password":user.password,
                    "date_of_birth": user.date_of_birth
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            # Extract user and token data from validated data
            user_data = serializer.validated_data
            # Now, this is the actual User model instance
            user = user_data["user"]
            tokens = user_data["tokens"]

            # Perform login with the actual User instance
            django_login(request, user)

            # Construct response with user details and tokens
            response_data = {
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                      "last_name" :user.last_name, },
                "tokens": tokens,
            }

            # Return response with user details and tokens
            return Response(response_data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailAPIView(APIView):
    def get_object(self, pk):
        return get_object_or_404(User, pk=pk)

    def get(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def put(self, request, pk):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class PatientListCreateView(APIView):
    """
    GET: List all patients
    POST: Create a new patient
    """
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PatientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDetailsView(APIView):
    """
    GET: Retrieve a patient by ID
    PUT/PATCH: Update a patient
    DELETE: Delete a patient
    """
    def get_object(self, pk):
        return get_object_or_404(Patient, pk=pk)

    def get(self, request, pk):
        patient = self.get_object(pk)
        serializer = PatientSerializer(patient)
        return Response(serializer.data)

    def put(self, request, pk):
        patient = self.get_object(pk)
        serializer = PatientSerializer(patient, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        patient = self.get_object(pk)
        serializer = PatientSerializer(patient, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        patient = self.get_object(pk)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class DoctorListCreateView(APIView):
    """
    GET: List all patients
    POST: Create a new patient
    """
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DoctorSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorDetailsView(APIView):
    """
    GET: Retrieve a patient by ID
    PUT/PATCH: Update a patient
    DELETE: Delete a patient
    """
    def get_object(self, pk):
        return get_object_or_404(Doctor, pk=pk)

    def get(self, request, pk):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor)
        return Response(serializer.data)

    def put(self, request, pk):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        doctor = self.get_object(pk)
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class DoctorAvailabilityListCreateView(APIView):
    """
    GET: List all patients
    POST: Create a new patient
    """
    def get(self, request):
        doctorAvailability = DoctorAvailability.objects.all()
        serializer = DoctorAvailabilitySerializer(doctorAvailability, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DoctorAvailabilitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DoctorAvailabilityDetailsView(APIView):
    """
    GET: Retrieve a patient by ID
    PUT/PATCH: Update a patient
    DELETE: Delete a patient
    """
    def get_object(self, pk):
        return get_object_or_404(DoctorAvailability, pk=pk)

    def get(self, request, pk):
        doctorAvailability = self.get_object(pk)
        serializer = DoctorAvailabilitySerializer(doctorAvailability)
        return Response(serializer.data)

    def put(self, request, pk):
        doctorAvailability = self.get_object(pk)
        serializer = DoctorAvailabilitySerializer(doctorAvailability, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        doctorAvailability = self.get_object(pk)
        serializer = DoctorAvailabilitySerializer(doctorAvailability, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        doctorAvailability = self.get_object(pk)
        doctorAvailability.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
class AppointmentListCreateView(APIView):
    """
    GET: List all patients
    POST: Create a new patient
    """
    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDetailsView(APIView):
    """
    GET: Retrieve a patient by ID
    PUT/PATCH: Update a patient
    DELETE: Delete a patient
    """
    def get_object(self, pk):
        return get_object_or_404(Appointment, pk=pk)

    def get(self, request, pk):
        appointments = self.get_object(pk)
        serializer = AppointmentSerializer(appointments)
        return Response(serializer.data)

    def put(self, request, pk):
        appointments = self.get_object(pk)
        serializer = AppointmentSerializer(appointments, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        appointments = self.get_object(pk)
        serializer = AppointmentSerializer(appointments, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        appointments = self.get_object(pk)
        appointments.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)