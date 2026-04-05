
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cura.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import UserProfile, Pharmacy, OxygenSupplier, Hospital, Doctor, HospitalBed

def create_user(username, password, role, email=''):
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    user.set_password(password)
    user.save()
    
    # Create or update profile
    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.role = role
    profile.save()
    
    print(f"User {username} ({role}) ready.")
    return user


def create_patient_user(username='test_patient', password='patient123', email='patient@example.com'):
    user, created = User.objects.get_or_create(username=username, defaults={'email': email})
    user.set_password(password)
    user.is_staff = False
    user.is_superuser = False
    user.save()

    profile, _ = UserProfile.objects.get_or_create(user=user)
    profile.role = 'PATIENT'
    profile.save()

    print(f"Patient user {username} ready.")
    return user

# 1. Pharmacy Admin
pharm_user = create_user('pharmacy_admin', 'admin123', 'PHARMACY_ADMIN', 'pharmacy@example.com')
pharmacy, _ = Pharmacy.objects.get_or_create(
    user=pharm_user,
    defaults={
        'name': 'City Care Pharmacy',
        'city': 'Mumbai',
        'address': '123 Main St, Mumbai',
        'contact_phone': '9998887777'
    }
)
print(f"Linked to Pharmacy: {pharmacy.name}")

# 2. Oxygen Supplier
oxy_user = create_user('oxygen_admin', 'admin123', 'OXYGEN_SUPPLIER', 'oxygen@example.com')
supplier, _ = OxygenSupplier.objects.get_or_create(
    user=oxy_user,
    defaults={
        'name': 'OxyLife Supplies',
        'city': 'Mumbai',
        'contact_phone': '8887776666'
    }
)
print(f"Linked to Oxygen Supplier: {supplier.name}")

# 3. Hospital Admin
hosp_user = create_user('hospital_admin', 'admin123', 'HOSPITAL_ADMIN', 'hospital@example.com')
# NOTE: In current views logic, Hospital Admin sees ALL hospitals. 
# But for completeness, let's ensure at least one hospital exists.
hospital, _ = Hospital.objects.get_or_create(
    name='City General Hospital',
    defaults={
        'city': 'Mumbai',
        'address': '456 Health Ave',
        'state': 'Maharashtra',
        'contact_phone': '1112223333',
        'emergency_contact': '102'
    }
)
print(f"Ensured Hospital exists: {hospital.name}")

# 4. Super Admin
admin_user = create_user('admin', 'admin123', 'ADMIN', 'admin@example.com')
admin_user.is_superuser = True
admin_user.is_staff = True
admin_user.save()
print("Superuser 'admin' ready.")

# 5. Patient Test User
create_patient_user('test_patient', 'patient123', 'patient@example.com')

print("\n--- DEMO ACCOUNTS ---")
print("1. Pharmacy Admin: pharmacy_admin / admin123")
print("2. Oxygen Supplier: oxygen_admin / admin123")
print("3. Hospital Admin: hospital_admin / admin123")
print("4. Super Admin: admin / admin123")
print("5. Patient: test_patient / patient123")
