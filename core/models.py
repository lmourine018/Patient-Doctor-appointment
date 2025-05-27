from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager, AbstractBaseUser

from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import datetime


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


  
class User(AbstractBaseUser):
    USER_TYPE_CHOICES = [
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('admin', 'Admin'),
    ]
    first_name = models.CharField(max_length=255, blank=False)
    last_name = models.CharField(max_length=255, blank= False)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    email = models.CharField(unique=True)
    phone_number = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', 
                   message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")]
    )
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()
    USERNAME_FIELD = 'email'  # what field will be used to log in
    REQUIRED_FIELDS = ['first_name', 'last_name', 'user_type', 'phone_number']  # required for createsuperuser



    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.user_type})"



class Patient(models.Model):
    """Patient profile model"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('P', 'Prefer not to say'),
    ]

    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True)
    address = models.CharField(max_length=255)
    insurance_provider = models.CharField( 
        null=True, 
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


    class Meta:
        ordering = ['user__last_name', 'user__first_name']

class Doctor(models.Model):
    """Doctor profile model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    # Professional Information
    license_number = models.CharField(max_length=50, unique=True)
    specializations = models.CharField(blank=True)
    years_of_experience = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(50)]
    )
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2)
    appointment_duration = models.PositiveIntegerField(
        default=30, 
        help_text="Default appointment duration in minutes"
    )
    
    is_accepting_patients = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name}"

    def get_specializations_display(self):
        return ", ".join([spec.name for spec in self.specializations.all()])

    class Meta:
        ordering = ['user__last_name', 'user__first_name']


class DoctorAvailability(models.Model):
    """Doctor availability schedule"""
    WEEKDAY_CHOICES = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availability_schedule')
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")

    def __str__(self):
        return f"{self.doctor} - {self.get_weekday_display()}: {self.start_time}-{self.end_time}"

    class Meta:
        unique_together = ['doctor', 'weekday', 'start_time', 'end_time']
        ordering = ['doctor', 'weekday', 'start_time']


class DoctorTimeOff(models.Model):
    """Doctor time off/unavailable periods"""
    TIME_OFF_TYPES = [
        ('vacation', 'Vacation'),
        ('sick_leave', 'Sick Leave'),
        ('conference', 'Conference'),
        ('personal', 'Personal'),
        ('other', 'Other'),
    ]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='time_off')
    start_date = models.DateField()
    end_date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)  # For partial day off
    end_time = models.TimeField(null=True, blank=True)    # For partial day off
    time_off_type = models.CharField(max_length=20, choices=TIME_OFF_TYPES)
    reason = models.TextField(blank=True)
    is_full_day = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError("End date must be on or after start date")
        
        if not self.is_full_day:
            if not self.start_time or not self.end_time:
                raise ValidationError("Start and end times are required for partial day off")
            if self.start_time >= self.end_time:
                raise ValidationError("End time must be after start time")

    def __str__(self):
        return f"{self.doctor} - {self.time_off_type}: {self.start_date} to {self.end_date}"

    class Meta:
        ordering = ['doctor', 'start_date']


class Appointment(models.Model):
    """Appointment model"""
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
        ('rescheduled', 'Rescheduled'),
    ]

    APPOINTMENT_TYPE_CHOICES = [
        ('consultation', 'Consultation'),
        ('follow_up', 'Follow-up'),
        ('check_up', 'Check-up'),
        ('procedure', 'Procedure'),
        ('emergency', 'Emergency'),
    ]

    
    # Core appointment details
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    appointment_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPE_CHOICES, default='consultation')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    reason_for_visit = models.TextField()
    notes = models.TextField(blank=True, help_text="Doctor's notes")
    cancellation_reason = models.TextField(blank=True)
    cancelled_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='cancelled_appointments'
    )
    cancelled_at = models.DateTimeField(null=True, blank=True)
    follow_up_required = models.BooleanField(default=False)
    follow_up_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_appointments'
    )

    def clean(self):
        """Validate appointment data"""
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")
        
        if self.appointment_date < timezone.now().date():
            raise ValidationError("Cannot schedule appointments in the past")
        
        if self.pk is None:  # Only for new appointments
            conflicts = Appointment.objects.filter(
                doctor=self.doctor,
                appointment_date=self.appointment_date,
                status__in=['scheduled', 'confirmed', 'in_progress']
            ).exclude(pk=self.pk if self.pk else None)
            
            for conflict in conflicts:
                if (self.start_time < conflict.end_time and 
                    self.end_time > conflict.start_time):
                    raise ValidationError(
                        f"Appointment conflicts with existing appointment from "
                        f"{conflict.start_time} to {conflict.end_time}"
                    )

    def get_datetime(self):
        """Get appointment as datetime object"""
        return timezone.make_aware(
            datetime.combine(self.appointment_date, self.start_time)
        )

    def is_past(self):
        """Check if appointment is in the past"""
        return self.get_datetime() < timezone.now()

    def can_be_cancelled(self):
        """Check if appointment can be cancelled (not in past, not already cancelled)"""
        return (not self.is_past() and 
                self.status not in ['cancelled', 'completed', 'no_show'])

    def cancel(self, cancelled_by, reason=""):
        """Cancel the appointment"""
        if self.can_be_cancelled():
            self.status = 'cancelled'
            self.cancelled_by = cancelled_by
            self.cancelled_at = timezone.now()
            self.cancellation_reason = reason
            self.save()
            return True
        return False

    def __str__(self):
        return f"{self.patient} with {self.doctor} on {self.appointment_date} at {self.start_time}"

    class Meta:
        ordering = ['appointment_date', 'start_time']
        unique_together = ['doctor', 'appointment_date', 'start_time']




