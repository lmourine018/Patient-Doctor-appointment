
from rest_framework import serializers
from .models import User, Patient, DoctorAvailability, Doctor,Appointment
from django.contrib.auth.hashers import check_password, make_password
from django.utils.crypto import get_random_string
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta
from django.contrib.auth import authenticate



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'user_type', 'phone_number', 'date_of_birth',
            'created_at', 'updated_at', 'is_active',
        ]
        read_only_fields = ('created_at', 'updated_at')


class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'
class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = '__all__'

class DoctorAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorAvailability
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'user_type', 'phone_number', 'date_of_birth']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def create_token(self, user):
        """Generate JWT tokens with custom expiration times."""
        # Create a refresh token with a custom expiration time
        refresh = RefreshToken.for_user(user)
        refresh["user_id"] = user.id

        # Set the expiration time for the refresh token (e.g., 7 days)
        refresh.set_exp(lifetime=timedelta(days=7))

        # Create an access token with a custom expiration time (e.g., 15 minutes)
        access_token = refresh.access_token
        access_token.set_exp(lifetime=timedelta(minutes=20))

        return {
            "refresh": str(refresh),
            "access": str(access_token),
        }

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        # Authenticate the user based on the email and password
        user = authenticate(
            request=self.context.get("request"), email=email, password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        # Generate tokens using the create_token method
        tokens = self.create_token(user)

        # Return user instance and tokens
        return {
            "user": user,  # Directly return the user instance
            "tokens": tokens,  # Return tokens
        }

