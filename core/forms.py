from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import (
    Appointment,
    BedBooking,
    CartItem,
    MedicineOrder,
    MedicineOrderItem,
    OxygenBooking,
    SupportRequest,
    UserProfile,
    Appointment,
    BedBooking,
    CartItem,
    MedicineOrder,
    MedicineOrderItem,
    OxygenBooking,
    SupportRequest,
    UserProfile,
    Doctor,
    InsurancePolicy,
    Medicine,
    OxygenCylinderStock,
    HospitalBed,
    Pharmacy,
    OxygenSupplier,
    Hospital
)

class DoctorForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = [
            'name',
            'qualification',
            'speciality',
            'experience_years',
            'hospital',
            'city',
            'languages_spoken',
            'fees',
            'available_from',
            'available_to',
            'rating',
            'is_active',
        ]

        widgets = {
            'available_from': forms.TimeInput(attrs={'type': 'time'}),
            'available_to': forms.TimeInput(attrs={'type': 'time'}),
        }
class PatientRegistrationForm(UserCreationForm):
    phone = forms.CharField(required=False)
    city = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'city', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.role = 'PATIENT'
            profile.phone = self.cleaned_data.get('phone')
            profile.city = self.cleaned_data.get('city')
            profile.save()
        return user


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date', 'time_slot', 'payment_option']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time_slot': forms.TimeInput(attrs={'type': 'time'}),
            'payment_option': forms.Select(attrs={'class': 'form-select'}),
        }


class OxygenBookingForm(forms.ModelForm):
    class Meta:
        model = OxygenBooking
        fields = ['quantity', 'delivery_address', 'scheduled_date', 'time_slot', 'payment_option']
        widgets = {
            'scheduled_date': forms.DateInput(attrs={'type': 'date'}),
            'time_slot': forms.TimeInput(attrs={'type': 'time'}),
        }


class MedicineOrderItemForm(forms.ModelForm):
    class Meta:
        model = MedicineOrderItem
        fields = ['quantity']


class CartAddItemForm(forms.ModelForm):
    """
    Simple form used on the medicine listing page to add packs to cart.
    """

    class Meta:
        model = CartItem
        fields = ['quantity']


class MedicineOrderContactForm(forms.ModelForm):
    """
    Captures patient contact phone and delivery address at checkout.
    """

    class Meta:
        model = MedicineOrder
        fields = ['contact_phone', 'shipping_address']


class SupportRequestForm(forms.ModelForm):
    class Meta:
        model = SupportRequest
        fields = ['name', 'contact', 'subject', 'description', 'is_emergency']

class BedBookingUploadForm(forms.ModelForm):
    prescription = forms.FileField(
        required=True,
        help_text="Upload Doctor Prescription (Max 5MB, PDF/JPG/PNG only)"
    )

    class Meta:
        model = BedBooking
        fields = ['booking_date', 'time_slot', 'prescription']
        widgets = {
            'booking_date': forms.DateInput(attrs={'type': 'date'}),
            'time_slot': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_prescription(self):
        file = self.cleaned_data.get('prescription')
        if file:
            if file.size > 5 * 1024 * 1024:  # 5MB
                raise forms.ValidationError("File size too large ( > 5MB )")
            if not file.name.lower().endswith(('.pdf', '.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Invalid file type. Only PDF, JPG, PNG allowed.")
        return file


class BedBookingPaymentForm(forms.ModelForm):
    class Meta:
        model = BedBooking
        fields = ['payment_option']
        widgets = {
            'payment_option': forms.Select(attrs={'class': 'form-select'}),
        }

class InsurancePolicyForm(forms.ModelForm):
    class Meta:
        model = InsurancePolicy
        fields = ['provider_name', 'policy_number', 'coverage_limit', 'valid_until']
        widgets = {
            'valid_until': forms.DateInput(attrs={'type': 'date'}),
        }


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'brand', 'form', 'strength', 'pack_size', 'price', 'stock', 'description', 'is_essential']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class OxygenStockForm(forms.ModelForm):
    class Meta:
        model = OxygenCylinderStock
        fields = ['capacity_litres', 'price_per_cylinder', 'available_cylinders']


class AdminOxygenStockForm(forms.ModelForm):
    class Meta:
        model = OxygenCylinderStock
        fields = ['supplier', 'capacity_litres', 'price_per_cylinder', 'available_cylinders']


class AdminHospitalBedForm(forms.ModelForm):
    class Meta:
        model = HospitalBed
        fields = ['hospital', 'bed_type', 'total_beds', 'available_beds']
