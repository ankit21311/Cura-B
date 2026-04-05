<<<<<<< HEAD
=======
import logging

>>>>>>> ace957e61389140a650be7d1ed8d65cf978084f0
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .forms import (
    AppointmentForm,
    BedBookingUploadForm,
    BedBookingPaymentForm,
    CartAddItemForm,
    MedicineOrderContactForm,
    MedicineOrderItemForm,
    OxygenBookingForm,
    PatientRegistrationForm,
    SupportRequestForm,
    DoctorForm,
    InsurancePolicyForm,
    AdminOxygenStockForm,
    AdminHospitalBedForm,
)
from .models import (
    Appointment,
    BedBooking,
    Cart,
    CartItem,
    Doctor,
    Hospital,
    HospitalBed,
    Medicine,
    MedicineOrder,
    MedicineOrderItem,
    Notification,
    OxygenBooking,
    OxygenCylinderStock,
    OxygenSupplier,
    Pharmacy,
    SupportRequest,
    UserProfile,
    Wallet,
    Transaction,
    InsurancePolicy,
)
from decimal import Decimal


<<<<<<< HEAD
=======
logger = logging.getLogger(__name__)


>>>>>>> ace957e61389140a650be7d1ed8d65cf978084f0
def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('dashboard')


def register(request):
    if request.method == 'POST':
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
<<<<<<< HEAD
            form.save()
            messages.success(request, 'Registration successful. Please log in.')
            return redirect('login')
=======
            try:
                form.save()
            except Exception:
                logger.exception('Registration failed while creating a new user')
                messages.error(
                    request,
                    'Registration is temporarily unavailable. Please try again in a minute.'
                )
            else:
                messages.success(request, 'Registration successful. Please log in.')
                return redirect('login')
>>>>>>> ace957e61389140a650be7d1ed8d65cf978084f0
    else:
        form = PatientRegistrationForm()
    return render(request, 'core/register.html', {'form': form})

"""
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')

        
    return render(request, 'core/login.html')
"""
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # 🔑 ROLE-BASED REDIRECT
            if user.is_superuser:
                return redirect('admin_dashboard')

            elif user.is_staff:
                return redirect('hospital_admin_dashboard')

            else:
                return redirect('patient_dashboard')
        else:
             messages.error(request, 'Invalid credentials')
    else:
        form = AuthenticationForm()

    return render(request, 'core/login.html', {'form': form})

def is_super_admin(user):
    return user.is_authenticated and user.is_superuser

@login_required
@user_passes_test(is_super_admin)
def manage_doctors(request):
    doctors = Doctor.objects.select_related('hospital').order_by('name')
    return render(request, 'core/manage/doctors_list.html', {
        'doctors': doctors
    })

@login_required
@user_passes_test(is_super_admin)
def edit_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)

    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor updated successfully.')
            return redirect('manage_doctors')
    else:
        form = DoctorForm(instance=doctor)

    return render(request, 'core/manage/doctor_form.html', {
        'form': form,
        'title': 'Edit Doctor'
    })

@login_required
@user_passes_test(is_super_admin)
def toggle_doctor_status(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.is_active = not doctor.is_active
    doctor.save()

    status = "activated" if doctor.is_active else "deactivated"
    messages.success(request, f'Doctor {status}.')
    return redirect('manage_doctors')


@login_required
@user_passes_test(is_super_admin)
def create_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor created successfully.')
            return redirect('manage_doctors')
    else:
        form = DoctorForm()

    return render(request, 'core/manage/doctor_form.html', {
        'form': form,
        'title': 'Add Doctor'
    })


@require_POST
def logout_view(request):
    logout(request)
    return redirect('home')


def role_required(allowed_roles):
    def decorator(view_func):
        @login_required
        def _wrapped(request, *args, **kwargs):
            try:
                role = request.user.userprofile.role
            except UserProfile.DoesNotExist:
                # Allow staff/superusers to bypass explicit role assignment.
                if request.user.is_staff or request.user.is_superuser:
                    return view_func(request, *args, **kwargs)
                messages.error(request, 'Role not assigned. Contact admin.')
                return redirect('home')
            if role not in allowed_roles:
                messages.error(request, 'You are not authorized to view this page.')
                return redirect('dashboard')
            return view_func(request, *args, **kwargs)
        return _wrapped
    return decorator


@login_required
def dashboard(request):
    try:
        role = request.user.userprofile.role
    except UserProfile.DoesNotExist:
        role = None

    if role == 'PATIENT':
        return redirect('patient_dashboard')
    elif role == 'ADMIN':
        return redirect('admin_dashboard')
    elif role == 'HOSPITAL_ADMIN':
        return redirect('hospital_admin_dashboard')
    elif role == 'PHARMACY_ADMIN':
        return redirect('pharmacy_admin_dashboard')
    elif role == 'OXYGEN_SUPPLIER':
        return redirect('oxygen_supplier_dashboard')
    elif request.user.is_staff or request.user.is_superuser:
        return redirect('admin_dashboard')
    else:
        # Fallback for users with no profile and no staff status (shouldn't happen with default PATIENT role)
        return redirect('patient_dashboard')


@login_required
@role_required(['PATIENT'])
def patient_dashboard(request):
    appointments = request.user.appointments.select_related('doctor').order_by('-created_at')[:5]
    medicine_orders = request.user.medicine_orders.select_related('pharmacy').order_by('-created_at')[:5]
    oxygen_bookings = request.user.oxygen_bookings.select_related('stock').order_by('-created_at')[:5]
    notifications = request.user.notifications.order_by('-created_at')[:10]
    bed_bookings = request.user.bed_bookings.select_related('hospital_bed__hospital').order_by('-created_at')[:5]
    return render(request, 'core/dashboards/patient_dashboard.html', {
        'appointments': appointments,
        'medicine_orders': medicine_orders,
        'oxygen_bookings': oxygen_bookings,
        'notifications': notifications,
        'bed_bookings': bed_bookings,
    })



@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Doctor created successfully')
            return redirect('manage_doctors')
    else:
        form = DoctorForm()

    return render(request, 'core/manage/doctor_form.html', {'form': form})

@login_required
@user_passes_test(is_super_admin)
@require_POST
def admin_update_appointment_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    status = request.POST.get('status')
    valid_statuses = {choice[0] for choice in Appointment.STATUS_CHOICES}
    if status in valid_statuses:
        appointment.status = status
        appointment.save()
        Notification.objects.create(
            user=appointment.patient,
            message=f'Your appointment with {appointment.doctor.name if appointment.doctor.name.startswith("Dr") else "Dr. " + appointment.doctor.name} on {appointment.date} is now {status}.',
            notification_type='APPOINTMENT',
        )
        messages.success(request, 'Appointment status updated.')
    else:
        messages.error(request, 'Invalid status.')
    return redirect('admin_dashboard')


@login_required
@user_passes_test(is_super_admin)
@require_POST
def admin_update_medicine_order_status(request, pk):
    order = get_object_or_404(MedicineOrder, pk=pk)
    status = request.POST.get('status')
    valid_statuses = {choice[0] for choice in MedicineOrder.STATUS_CHOICES}
    if status in valid_statuses:
        old_status = order.status
        order.status = status
        order.save()

        # If approved, reduce stock
        if status == 'CONFIRMED' and old_status != 'CONFIRMED':
            all_available = True
            # First check all items
            for item in order.items.all():
                if item.quantity > item.medicine.stock:
                    all_available = False
                    break
            
            if all_available:
                for item in order.items.all():
                    item.medicine.stock -= item.quantity
                    item.medicine.save()
            else:
                 messages.warning(request, f'Stock insufficient for some items in Order #{order.id}, but marked CONFIRMED.')

        Notification.objects.create(
            user=order.patient,
            message=f'Medicine order #{order.id} status updated to {status}.',
            notification_type='MEDICINE',
        )
        messages.success(request, 'Medicine order status updated.')
    else:
        messages.error(request, 'Invalid status.')
    return redirect('admin_dashboard')


@login_required
@user_passes_test(is_super_admin)
@require_POST
def admin_update_oxygen_booking_status(request, pk):
    booking = get_object_or_404(OxygenBooking, pk=pk)
    status = request.POST.get('status')
    valid_statuses = {choice[0] for choice in OxygenBooking.STATUS_CHOICES}
    if status in valid_statuses:
        old_status = booking.status
        booking.status = status
        booking.save()
        
        # If approved, reduce available cylinders
        if status == 'CONFIRMED' and old_status != 'CONFIRMED':
            stock = booking.stock
            if stock.available_cylinders >= booking.quantity:
                stock.available_cylinders -= booking.quantity
                stock.save()
            else:
                messages.warning(request, f'Stock is insufficient, but booking was marked confirmed.')

        Notification.objects.create(
            user=booking.patient,
            message=f'Your oxygen booking from {booking.stock.supplier.name} is now {status}.',
            notification_type='OXYGEN',
        )
        messages.success(request, 'Oxygen booking status updated.')
    else:
        messages.error(request, 'Invalid status.')
    return redirect('admin_dashboard')


@login_required
@user_passes_test(is_super_admin)
@require_POST
def admin_update_support_request_status(request, pk):
    support = get_object_or_404(SupportRequest, pk=pk)
    status = request.POST.get('status')
    valid_statuses = {choice[0] for choice in SupportRequest.STATUS_CHOICES}
    if status in valid_statuses:
        support.status = status
        support.save()
        # Optional: notify linked user
        if support.user:
            Notification.objects.create(
                user=support.user,
                message=f'Your support request "{support.subject}" is now {status}.',
                notification_type='SUPPORT',
            )
        messages.success(request, 'Support request status updated.')
    else:
        messages.error(request, 'Invalid status.')
    return redirect('admin_dashboard')


@login_required
@role_required(['HOSPITAL_ADMIN'])
def hospital_admin_dashboard(request):
    hospitals = Hospital.objects.all()
    appointments = Appointment.objects.select_related('doctor', 'patient').order_by('-created_at')[:10]
    return render(request, 'core/dashboards/hospital_admin_dashboard.html', {
        'hospitals': hospitals,
        'appointments': appointments,
    })


@login_required
@role_required(['PHARMACY_ADMIN'])
def pharmacy_admin_dashboard(request):
    pharmacy = getattr(request.user, 'pharmacy', None)
    medicines = pharmacy.medicines.all() if pharmacy else Medicine.objects.none()
    orders = pharmacy.orders.order_by('-created_at')[:10] if pharmacy else MedicineOrder.objects.none()
    return render(request, 'core/dashboards/pharmacy_admin_dashboard.html', {
        'pharmacy': pharmacy,
        'medicines': medicines,
        'orders': orders,
    })


@login_required
@role_required(['OXYGEN_SUPPLIER'])
def oxygen_supplier_dashboard(request):
    supplier = getattr(request.user, 'oxygen_supplier', None)
    stocks = supplier.stocks.all() if supplier else OxygenCylinderStock.objects.none()
    bookings_flat = OxygenBooking.objects.filter(stock__supplier=supplier).order_by('-created_at')[:20] if supplier else OxygenBooking.objects.none()
    return render(request, 'core/dashboards/oxygen_supplier_dashboard.html', {
        'supplier': supplier,
        'stocks': stocks,
        'bookings': bookings_flat,
    })


@login_required
@user_passes_test(is_super_admin)
def admin_dashboard(request):
    # Fetch pending items for admin review
    appointments = Appointment.objects.filter(status='PENDING').select_related('doctor', 'patient').order_by('created_at')
    orders = MedicineOrder.objects.filter(status='PENDING').select_related('patient', 'pharmacy').order_by('created_at')
    oxygen_bookings = OxygenBooking.objects.filter(status='PENDING').select_related('patient', 'stock').order_by('created_at')
    support_requests = SupportRequest.objects.filter(status='OPEN').select_related('user').order_by('created_at')
    bed_bookings = BedBooking.objects.filter(status='PENDING').select_related('patient', 'hospital_bed__hospital').order_by('created_at')

    return render(request, 'core/dashboards/admin_dashboard.html', {
        'appointments': appointments,
        'orders': orders,
        'oxygen_bookings': oxygen_bookings,
        'support_requests': support_requests,
        'bed_bookings': bed_bookings,
    })


def hospital_list(request):
    city = request.GET.get('city')
    bed_type = request.GET.get('bed_type')
    min_rating = request.GET.get('min_rating')

    hospitals = Hospital.objects.all()

    if city:
        hospitals = hospitals.filter(city__icontains=city)
    if min_rating:
        hospitals = hospitals.filter(rating__gte=min_rating)
    if bed_type:
        hospitals = hospitals.filter(beds__bed_type=bed_type).distinct()

    context = {
        'hospitals': hospitals.prefetch_related('beds'),
        'selected_city': city or '',
        'selected_bed_type': bed_type or '',
        'selected_min_rating': min_rating or '',
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []
        for hospital in context['hospitals']:
            beds = []
            for b in hospital.beds.all():
                beds.append({
                    'bed_type': b.bed_type,
                    'total_beds': b.total_beds,
                    'available_beds': b.available_beds,
                })
            data.append({
                'id': hospital.id,
                'name': hospital.name,
                'city': hospital.city,
                'rating': float(hospital.rating),
                'beds': beds,
            })
        return JsonResponse({'hospitals': data})
    return render(request, 'core/hospitals/hospital_list.html', context)


def hospital_detail(request, pk):
    hospital = get_object_or_404(Hospital, pk=pk)
    beds = hospital.beds.all()
    doctors = hospital.doctors.all()
    return render(request, 'core/hospitals/hospital_detail.html', {
        'hospital': hospital,
        'beds': beds,
        'doctors': doctors,
    })


@login_required
@login_required
@role_required(['PATIENT'])
def bed_booking_create(request, bed_id):
    bed = get_object_or_404(HospitalBed, id=bed_id)
    if bed.available_beds <= 0:
        messages.error(request, 'No beds of this type are currently available.')
        return redirect('hospital_detail', pk=bed.hospital.id)

    if request.method == 'POST':
        form = BedBookingUploadForm(request.POST, request.FILES)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.patient = request.user
            booking.hospital_bed = bed
            booking.status = 'AWAITING_PAYMENT'
            booking.save()
            return redirect('bed_booking_payment', booking_id=booking.id)
        else:
            # If form errors, redirect back to modal (or show error efficiently)
            # For simplicity in this modal flow, we might need to render a dedicated page or pass errors.
            # But the user asked for a modal. If modal submission fails, standard practice is to return errors.
            # Since the modal is on hospital_detail, we might need to handle this gracefully.
            # For now, let's render a standalone page if it fails, or re-render hospital detail with the form errors.
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = BedBookingUploadForm()
    
    # If not POST, we shouldn't really be here unless someone hit the URL directly.
    # But the modal will POST here.
    return render(request, 'core/hospitals/bed_booking_form.html', {
        'bed': bed,
        'form': form,
    })


@login_required
@role_required(['PATIENT'])
def bed_booking_payment(request, booking_id):
    booking = get_object_or_404(BedBooking, id=booking_id, patient=request.user)
    
    if booking.status != 'AWAITING_PAYMENT':
        messages.info(request, 'This booking has already been processed.')
        return redirect('patient_dashboard')

    bed = booking.hospital_bed
    # Determine price (Mock logic)
    price_map = {'ICU': 5000, 'GENERAL': 1000, 'EMERGENCY': 3000}
    price = price_map.get(bed.bed_type, 1000)

    if request.method == 'POST':
        form = BedBookingPaymentForm(request.POST, instance=booking)
        if form.is_valid():
            final_booking = form.save(commit=False)
            payment_option = final_booking.payment_option
            
            # Payment Processing
            if payment_option == 'INSURANCE':
                verified_policy = request.user.insurance_policies.filter(status='VERIFIED', valid_until__gte=timezone.now().date()).first()
                if not verified_policy:
                    messages.error(request, 'No active verified insurance policy found.')
                    return redirect('manage_insurance')
                
                if not verified_policy.debit(price):
                    messages.error(request, f'Insufficient insurance coverage. Limit exceeded. Price: {price}')
                    return redirect('bed_booking_payment', booking_id=booking.id)
                    
            elif payment_option == 'WALLET':
                wallet, _ = Wallet.objects.get_or_create(user=request.user)
                if not wallet.debit(price, content_object=booking):
                    messages.error(request, f'Insufficient wallet balance. Price: {price}')
                    return redirect('wallet_dashboard')

            final_booking.status = 'PENDING' # Now wait for Admin
            final_booking.save()
            
            Notification.objects.create(
                user=request.user,
                message=f'Bed booking request for {bed.get_bed_type_display()} at {bed.hospital.name} submitted. Prescription uploaded.',
                notification_type='BED',
            )
            messages.success(request, 'Booking submitted successfully. Waiting for admin approval.')
            return redirect('patient_dashboard')
    else:
        form = BedBookingPaymentForm(instance=booking)

    return render(request, 'core/hospitals/bed_booking_payment.html', {
         'form': form,
         'booking': booking,
         'price': price
    })


@login_required
@user_passes_test(is_super_admin)
@require_POST
def admin_update_bed_booking_status(request, pk):
    booking = get_object_or_404(BedBooking, pk=pk)
    status = request.POST.get('status')
    valid_statuses = {choice[0] for choice in BedBooking.STATUS_CHOICES}
    if status in valid_statuses:
        old_status = booking.status
        booking.status = status
        booking.save()
        
        # If approved, reduce available beds
        if status == 'CONFIRMED' and old_status != 'CONFIRMED':
            bed = booking.hospital_bed
            if bed.available_beds > 0:
                bed.available_beds -= 1
                bed.save()
            else:
                messages.warning(request, f'Bed count is already 0, but booking was marked confirmed.')

        Notification.objects.create(
            user=booking.patient,
            message=f'Your bed booking at {booking.hospital_bed.hospital.name} is now {status}.',
            notification_type='BED',
        )
        messages.success(request, 'Bed booking status updated.')
    else:
        messages.error(request, 'Invalid status.')
    return redirect('admin_dashboard')


def doctor_search(request):
    speciality = request.GET.get('speciality')
    city = request.GET.get('city')
    doctors = Doctor.objects.filter(is_active=True)

    if speciality:
        doctors = doctors.filter(speciality__iexact=speciality)
    if city:
        doctors = doctors.filter(city__icontains=city)

    return render(request, 'core/doctors/doctor_search.html', {
        'doctors': doctors.select_related('hospital'),
        'selected_speciality': speciality or '',
        'selected_city': city or '',
    })


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'core/doctors/doctor_detail.html', {'doctor': doctor})


@login_required
@role_required(['PATIENT'])
def book_appointment(request, doctor_id):
    doctor = get_object_or_404(Doctor, id=doctor_id, is_active=True)
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            fee = doctor.fees
            
            # 1. Verification (Pre-save)
            if appointment.payment_option == 'WALLET':
                wallet, _ = Wallet.objects.get_or_create(user=request.user)
                if not wallet.can_transact(fee):
                    messages.error(request, f'Insufficient wallet balance to book appointment. Fee: ₹{fee}')
                    return redirect('wallet_dashboard')

            elif appointment.payment_option == 'INSURANCE':
                verified_policy = request.user.insurance_policies.filter(status='VERIFIED', valid_until__gte=timezone.now().date()).first()
                if not verified_policy:
                    messages.error(request, 'No active verified insurance policy found.')
                    return redirect('manage_insurance')
                if not verified_policy.can_cover(fee):
                    messages.error(request, f'Insufficient insurance coverage limit. Fee: ₹{fee}')
                    return redirect('manage_insurance')

            # 2. Save Appointment
            appointment.patient = request.user
            appointment.doctor = doctor
            appointment.save()

            # 3. Debit (Post-save)
            if appointment.payment_option == 'WALLET':
                request.user.wallet.debit(fee, content_object=appointment)
            elif appointment.payment_option == 'INSURANCE':
                # Re-fetch to be safe or use cached verify_policy if valid
                verified_policy = request.user.insurance_policies.filter(status='VERIFIED', valid_until__gte=timezone.now().date()).first()
                verified_policy.debit(fee)

            Notification.objects.create(
                user=request.user,
                message=f'Appointment booked with {doctor.name if doctor.name.startswith("Dr") else "Dr. " + doctor.name} on {appointment.date}. Payment: {appointment.get_payment_option_display()}',
                notification_type='APPOINTMENT',
            )
            messages.success(request, 'Appointment booked successfully.')
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'core/doctors/book_appointment.html', {
        'doctor': doctor,
        'form': form,
    })


def oxygen_list(request):
    city = request.GET.get('city')
    suppliers = OxygenSupplier.objects.all().select_related('user')
    if city:
        suppliers = suppliers.filter(city__icontains=city)
    suppliers = suppliers.prefetch_related('stocks')
    return render(request, 'core/oxygen/oxygen_list.html', {
        'suppliers': suppliers,
        'selected_city': city or '',
    })


@login_required
@role_required(['PATIENT'])
def oxygen_booking_create(request, stock_id):
    stock = get_object_or_404(OxygenCylinderStock, id=stock_id)
    if request.method == 'POST':
        form = OxygenBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            
            # Determine price
            price = stock.price_per_cylinder * booking.quantity

            # Payment Processing
            if booking.payment_option == 'INSURANCE':
                verified_policy = request.user.insurance_policies.filter(status='VERIFIED', valid_until__gte=timezone.now().date()).first()
                if not verified_policy:
                    messages.error(request, 'No active verified insurance policy found.')
                    return redirect('manage_insurance')
                
                if not verified_policy.debit(price):
                    messages.error(request, f'Insufficient insurance coverage. Price: {price}')
                    return redirect('oxygen_list')

            elif booking.payment_option == 'WALLET':
                wallet, _ = Wallet.objects.get_or_create(user=request.user)
                if not wallet.debit(price, content_object=booking):
                    messages.error(request, f'Insufficient wallet balance. Price: {price}')
                    return redirect('wallet_dashboard')

            booking.patient = request.user
            booking.stock = stock
            if booking.quantity > stock.available_cylinders:
                messages.error(request, 'Not enough cylinders available.')
            else:
                booking.save()
                Notification.objects.create(
                    user=request.user,
                    message=f'Oxygen booking request for {stock.capacity_litres}L from {stock.supplier.name} submitted.',
                    notification_type='OXYGEN',
                )
                messages.success(request, 'Oxygen booking request submitted. Waiting for approval.')
                return redirect('patient_dashboard')
    else:
        form = OxygenBookingForm()
        
    verified_policy = request.user.insurance_policies.filter(status='VERIFIED', valid_until__gte=timezone.now().date()).first()

    return render(request, 'core/oxygen/oxygen_booking_form.html', {
        'stock': stock,
        'form': form,
        'verified_policy': verified_policy,
    })


def medicine_search(request):
    name = request.GET.get('name')
    city = request.GET.get('city')
    medicines = Medicine.objects.select_related('pharmacy').all()

    if name:
        medicines = medicines.filter(name__icontains=name)
    if city:
        medicines = medicines.filter(pharmacy__city__icontains=city)

    add_form = CartAddItemForm()

    return render(
        request,
        'core/medicines/medicine_search.html',
        {
            'medicines': medicines,
            'selected_name': name or '',
            'selected_city': city or '',
            'cart_add_form': add_form,
        },
    )


@login_required
@role_required(['PATIENT'])
def medicine_order_create(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    if request.method == 'POST':
        item_form = MedicineOrderItemForm(request.POST)
        contact_form = MedicineOrderContactForm(request.POST)
        if item_form.is_valid() and contact_form.is_valid():
            quantity = item_form.cleaned_data['quantity']
            if quantity > medicine.stock:
                messages.error(request, 'Not enough stock.')
            else:
                order = MedicineOrder.objects.create(
                    patient=request.user,
                    pharmacy=medicine.pharmacy,
                    status='PENDING',
                    contact_phone=contact_form.cleaned_data['contact_phone'],
                    shipping_address=contact_form.cleaned_data['shipping_address'],
                )
                MedicineOrderItem.objects.create(
                    order=order,
                    medicine=medicine,
                    quantity=quantity,
                    price_at_order=medicine.price,
                )
                # Removed immediate stock deduction
                # medicine.stock -= quantity
                # medicine.save()
                Notification.objects.create(
                    user=request.user,
                    message=f'Medicine order #{order.id} created.',
                    notification_type='MEDICINE',
                )
                messages.success(request, 'Your order has been placed. You can track it from your dashboard.')
                return redirect('patient_dashboard')
    else:
        item_form = MedicineOrderItemForm()
        contact_form = MedicineOrderContactForm()
    return render(request, 'core/medicines/medicine_order_form.html', {
        'medicine': medicine,
        'item_form': item_form,
        'contact_form': contact_form,
    })


def _get_or_create_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user, is_active=True)
    return cart


@login_required
@role_required(['PATIENT'])
@require_POST
def cart_add(request, medicine_id):
    medicine = get_object_or_404(Medicine, id=medicine_id)
    form = CartAddItemForm(request.POST)
    if form.is_valid():
        quantity = form.cleaned_data['quantity']
        if quantity <= 0:
            messages.error(request, 'Quantity must be at least 1 pack.')
            return redirect('medicine_search')

        cart = _get_or_create_cart(request.user)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            medicine=medicine,
            defaults={'quantity': quantity},
        )
        if not created:
            item.quantity += quantity
            item.save()

        messages.success(
            request,
            f'Added {quantity} pack(s) of {medicine.name} to your cart.',
        )
    else:
        messages.error(request, 'Could not add this medicine to the cart.')
    return redirect('cart_detail')


@login_required
@role_required(['PATIENT'])
def cart_detail(request):
    cart = (
        Cart.objects.filter(user=request.user, is_active=True)
        .prefetch_related('items__medicine__pharmacy')
        .first()
    )
    items = cart.items.all() if cart else []

    totals_by_pharmacy = {}
    if cart:
        for item in items:
            pharmacy = item.medicine.pharmacy
            totals_by_pharmacy.setdefault(pharmacy, 0)
            totals_by_pharmacy[pharmacy] += item.subtotal

    return render(
        request,
        'core/medicines/cart_detail.html',
        {
            'cart': cart,
            'items': items,
            'totals_by_pharmacy': totals_by_pharmacy,
        },
    )


@login_required
@role_required(['PATIENT'])
@require_POST
def cart_update(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user,
        cart__is_active=True,
    )
    try:
        quantity = int(request.POST.get('quantity', '1'))
    except ValueError:
        quantity = 1

    if quantity <= 0:
        item.delete()
        messages.success(request, f'Removed {item.medicine.name} from your cart.')
    else:
        item.quantity = quantity
        item.save()
        messages.success(
            request,
            f'Updated {item.medicine.name} to {quantity} pack(s) in your cart.',
        )

    return redirect('cart_detail')


@login_required
@role_required(['PATIENT'])
@require_POST
def cart_remove(request, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=request.user,
        cart__is_active=True,
    )
    name = item.medicine.name
    item.delete()
    messages.success(request, f'Removed {name} from your cart.')
    return redirect('cart_detail')


@login_required
@role_required(['PATIENT'])
def cart_checkout(request):
    cart = (
        Cart.objects.filter(user=request.user, is_active=True)
        .prefetch_related('items__medicine__pharmacy')
        .first()
    )
    if not cart or not cart.items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('medicine_search')

    items = list(cart.items.all())

    contact_form = MedicineOrderContactForm(request.POST or None)

    if request.method == 'POST':
        if not contact_form.is_valid():
            messages.error(request, 'Please provide a valid phone number and delivery address.')
        else:
            # Payment Processing
            payment_method = request.POST.get('payment_method', 'WALLET')
            total_amount = cart.total_price()

            if payment_method == 'INSURANCE':
                verified_policy = request.user.insurance_policies.filter(status='VERIFIED', valid_until__gte=timezone.now().date()).first()
                if not verified_policy:
                    messages.error(request, 'No active verified insurance policy found.')
                    return redirect('cart_detail')
                
                if not verified_policy.debit(total_amount):
                    messages.error(request, f'Insufficient insurance coverage for medicine order. Total: {total_amount}')
                    return redirect('cart_detail')
            
            elif payment_method == 'WALLET':
                wallet, _ = Wallet.objects.get_or_create(user=request.user)
                # Create a temporary/placeholder order or generic transaction for the whole cart?
                # Ideally we link to the Order(s), but we have multiple orders.
                # Let's link to the Cart for now or just generic.
                if not wallet.debit(total_amount):
                     messages.error(request, f'Insufficient wallet balance. Total: {total_amount}')
                     return redirect('wallet_dashboard')

            # Validate stock for each item
            for item in items:
                medicine = item.medicine
                if item.quantity > medicine.stock:
                    messages.error(
                        request,
                        f'Not enough stock for {medicine.name}. Available: {medicine.stock}',
                    )
                    return redirect('cart_detail')

            # Group items by pharmacy and create MedicineOrder(s)
            orders_created = []
            by_pharmacy = {}
            for item in items:
                by_pharmacy.setdefault(item.medicine.pharmacy, []).append(item)

            for pharmacy, pharmacy_items in by_pharmacy.items():
                order = MedicineOrder.objects.create(
                    patient=request.user,
                    pharmacy=pharmacy,
                    status='PENDING',
                    contact_phone=contact_form.cleaned_data['contact_phone'],
                    shipping_address=contact_form.cleaned_data['shipping_address'],
                )
                for item in pharmacy_items:
                    medicine = item.medicine
                    MedicineOrderItem.objects.create(
                        order=order,
                        medicine=medicine,
                        quantity=item.quantity,
                        price_at_order=medicine.price,
                    )
                    # Removed immediate stock deduction
                    # medicine.stock -= item.quantity
                    # medicine.save()
                orders_created.append(order)

            # Clear cart
            cart.items.all().delete()
            cart.is_active = False
            cart.save()

            for order in orders_created:
                Notification.objects.create(
                    user=request.user,
                    message=f'Medicine order #{order.id} created from your cart.',
                    notification_type='MEDICINE',
                )

            messages.success(
                request,
                'Your order has been placed. You can track it from your dashboard.',
            )
            return redirect('patient_dashboard')

    # GET or invalid POST: show review/summary UI + contact form
    totals_by_pharmacy = {}
    for item in items:
        pharmacy = item.medicine.pharmacy
        totals_by_pharmacy.setdefault(pharmacy, 0)
        totals_by_pharmacy[pharmacy] += item.subtotal

    return render(
        request,
        'core/medicines/cart_detail.html',
        {
            'cart': cart,
            'items': items,
            'totals_by_pharmacy': totals_by_pharmacy,
            'is_checkout': True,
            'contact_form': contact_form,
        },
    )


@login_required
def notifications_list(request):
    notifications = request.user.notifications.order_by('-created_at')
    return render(request, 'core/notifications/notification_list.html', {
        'notifications': notifications,
    })


@login_required
@require_POST
def notification_mark_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications_list')


def emergency_contacts(request):
    return render(request, 'core/support/emergency_contacts.html')


def support_request_create(request):
    if request.method == 'POST':
        form = SupportRequestForm(request.POST)
        if form.is_valid():
            support = form.save(commit=False)
            if request.user.is_authenticated:
                support.user = request.user
            support.save()
            if support.user:
                Notification.objects.create(
                    user=support.user,
                    message=f'Support request \"{support.subject}\" received.',
                    notification_type='SUPPORT',
                )
            messages.success(request, 'Support request submitted. Our team will contact you soon.')
            return redirect('home')
    else:
        form = SupportRequestForm()
    return render(request, 'core/support/support_request_form.html', {'form': form})


def assistant_home(request):
    """
    Optional landing page (the assistant is also available site-wide via the widget).
    """
    return render(request, 'core/assistant/assistant.html')


def _assistant_live_stats(user):
    """
    'Real-time' here means live DB-backed numbers (not external APIs).
    Keep this cheap and safe to compute.
    """
    stats = {
        "hospitals": Hospital.objects.count(),
        "doctors_active": Doctor.objects.filter(is_active=True).count(),
        "oxygen_suppliers": OxygenSupplier.objects.count(),
        "medicines": Medicine.objects.count(),
        "server_time": timezone.localtime().strftime("%d %b %Y, %H:%M"),
    }
    if user and getattr(user, "is_authenticated", False):
        stats["your_unread_notifications"] = Notification.objects.filter(user=user, is_read=False).count()
    return stats


from django.conf import settings

@csrf_exempt
@require_POST
def assistant_api(request):
    """
    Intelligent Assistant powered by OpenAI (ChatGPT).
    Falls back to simple logic if no key is configured or API fails.
    """
    try:
        payload = request.POST or {}
        message = (payload.get("message") or "").strip()
    except Exception:
        message = ""

    if not message:
        return JsonResponse({"reply": "I'm listening. Ask me anything about CURA or healthcare resources."})

    # Fallback/Default suggestions
    default_suggestions = ["Show live stats", "How do I book?", "Emergency contacts", "Oxygen availability"]
    
    # Check for API Key
    api_key = getattr(settings, 'OPENAI_API_KEY', None)
    
    if not api_key:
        # Fallback to simple static logic if no key
        return _static_assistant_reply(request, message)

    try:
        import openai
        # 1. Get Live Context
        stats = _assistant_live_stats(request.user)
        user_context = f"User: {request.user.username}" if request.user.is_authenticated else "User: Guest"
        
        # 2. Construct System Prompt
        system_prompt = (
            "You are the CURA Assistant, an AI for a hospital resource platform. "
            "Your goal is to help users find beds, doctors, oxygen, and medicines. "
            "Be concise, professional, and helpful. "
            "Strictly use the following LIVE DATA to answer questions about availability. "
            "Do not make up numbers. "
            f"\n\nLIVE DATA CONTEXT:\n{stats}\n"
            f"\nUSER CONTEXT:\n{user_context}\n"
            "\nIf the user asks for actions (like booking), explain the steps on the website. "
            "For general medical advice, include a disclaimer that you are an AI and they should see a doctor."
        )

        # 3. Call OpenAI API
        client = openai.OpenAI(api_key=api_key)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message},
            ],
            max_tokens=150,
            temperature=0.7,
        )
        
        reply_text = completion.choices[0].message.content.strip()
        
        return JsonResponse({
            "reply": reply_text,
            "suggestions": default_suggestions,
            "stats": stats
        })

    except Exception as e:
        # Log error in real app; here we just fall back
        print(f"OpenAI Error: {e}")
        return _static_assistant_reply(request, message)


def _static_assistant_reply(request, message):
    """
    Original static logic for fallback.
    """
    msg = message.lower()
    stats = _assistant_live_stats(request.user)

    def reply(text, suggestions=None):
        return JsonResponse({
            "reply": text,
            "suggestions": suggestions or ["How does CURA work?", "Where do I book a doctor?", "Show live stats", "Emergency help"],
            "stats": stats,
        })

    # Quick intents
    if any(k in msg for k in ["stats", "live data", "real time", "realtime", "updates", "update"]):
        return reply(
            "Here are your live platform stats (from the database):\n"
            f"- Hospitals: {stats['hospitals']}\n"
            f"- Active doctors: {stats['doctors_active']}\n"
            f"- Oxygen suppliers: {stats['oxygen_suppliers']}\n"
            f"- Medicines listed: {stats['medicines']}\n"
            + (f"- Your unread notifications: {stats.get('your_unread_notifications', 0)}\n" if "your_unread_notifications" in stats else "")
            + f"- Server time: {stats['server_time']}"
        , suggestions=["Hospital beds", "Doctors", "Medicines", "Oxygen"])

    if any(k in msg for k in ["how does", "how do", "workflow", "website work", "works", "use cura"]):
        return reply(
            "CURA is a single place to discover healthcare resources and take action:\n"
            "1) Dashboard: you see your latest activity (appointments, medicine orders, oxygen bookings, notifications).\n"
            "2) Resources: search hospitals (beds), doctors (appointments), medicines (orders), and oxygen suppliers (bookings).\n"
            "3) Notifications: CURA posts updates after you book/order.\n"
            "Tip: the numbers you see are live from the database and update as admins/suppliers change inventory or status."
        , suggestions=["Go to Dashboard", "Show live stats", "Emergency contacts", "24/7 Support"])

    if any(k in msg for k in ["doctor", "appointment", "book a doctor", "book doctor"]):
        return reply(
            "To book a doctor: open Resources → Doctors, filter by city/speciality, open a doctor profile, then choose a slot to book.\n"
            "After booking, you’ll see it on your Dashboard and in Notifications."
        , suggestions=["Search doctors", "View dashboard", "Show live stats"])

    if any(k in msg for k in ["hospital", "beds", "bed", "icu"]):
        return reply(
            "To find hospital beds: open Resources → Hospital beds and filter by city/bed type.\n"
            "Bed availability is shown per hospital and updates when hospital admins change it."
        , suggestions=["Hospital beds", "Emergency contacts", "Show live stats"])

    if any(k in msg for k in ["oxygen", "cylinder", "cylinders"]):
        return reply(
            "To book oxygen: open Resources → Oxygen, select a supplier, then book a cylinder capacity and quantity.\n"
            "Availability updates as suppliers adjust stock and as bookings are placed."
        , suggestions=["Oxygen", "Show live stats", "Emergency contacts"])

    if any(k in msg for k in ["medicine", "medicines", "pharmacy", "order"]):
        return reply(
            "To order medicines: open Resources → Medicines, filter by name/city, then place an order.\n"
            "Stock reduces when you order; you’ll get a notification update."
        , suggestions=["Medicines", "View dashboard", "Show live stats"])

    if any(k in msg for k in ["emergency", "ambulance", "112", "108", "police", "fire"]):
        return reply(
            "If this is an emergency, call the official numbers immediately:\n"
            "- National Emergency: 112\n- Ambulance: 102 / 108\n- Fire: 101\n- Police: 100\n"
            "Then use Emergency page → “Submit Support Request” for assistance and tracking inside CURA."
        , suggestions=["Open Emergency page", "Submit support request", "Show live stats"])

    # Fallback
    return reply(
        "I can guide you through CURA. Try asking about: hospital beds, booking doctors, medicines, oxygen, notifications, or type “stats”."
    )


# --- WALLET & INSURANCE VIEWS ---

@login_required
@role_required(['PATIENT'])
def wallet_dashboard(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user)
    transactions = wallet.transactions.all()[:20]
    return render(request, 'core/wallet/wallet_dashboard.html', {
        'wallet': wallet,
        'transactions': transactions,
    })


@login_required
@role_required(['PATIENT'])
@require_POST
def wallet_recharge(request):
    wallet = request.user.wallet
    amount = request.POST.get('amount')
    try:
        amount = Decimal(amount)
        if amount <= 0:
            raise ValueError
    except (TypeError, ValueError, Exception):
        messages.error(request, 'Invalid amount.')
        return redirect('wallet_dashboard')

    # Simulate payment success
    wallet.credit(amount)
    messages.success(request, f'Wallet recharged by {wallet.currency} {amount} successfully.')
    return redirect('wallet_dashboard')


def verify_policy(policy_number):
    """
    Mock verification logic:
    - Ends with even digit -> VERIFIED
    - Ends with odd digit -> REJECTED
    """
    try:
        last_digit = int(policy_number[-1])
        return last_digit % 2 == 0
    except (ValueError, IndexError):
        return False


@login_required
@role_required(['PATIENT'])
def manage_insurance(request):
    policies = request.user.insurance_policies.order_by('-created_at')
    
    if request.method == 'POST':
        form = InsurancePolicyForm(request.POST)
        if form.is_valid():
            policy = form.save(commit=False)
            policy.user = request.user
            
            # Verify Policy
            is_valid = verify_policy(policy.policy_number)
            policy.status = 'VERIFIED' if is_valid else 'REJECTED'
            
            policy.save()
            
            if is_valid:
                messages.success(request, 'Insurance policy verified and added successfully.')
            else:
                messages.error(request, 'Insurance verification failed. Policy rejected.')
                
            return redirect('manage_insurance')
    else:
        form = InsurancePolicyForm()

    return render(request, 'core/insurance/manage_insurance.html', {
        'policies': policies,
        'form': form,
    })


@login_required
@role_required(['PATIENT'])
def purchase_history(request):
    filter_type = request.GET.get('type')
    history = []

    # Helper to add items
    def add_items(source, type_label, get_details_func, get_price_func, get_payment_func):
        for item in source:
            history.append({
                'type': type_label,
                'date': item.created_at if hasattr(item, 'created_at') else item.date, # Handle appointment date
                'details': get_details_func(item),
                'price': get_price_func(item),
                'status': item.get_status_display(),
                'payment': get_payment_func(item)
            })

    # 1. Medicine Orders
    if not filter_type or filter_type == 'medicine':
        orders = MedicineOrder.objects.filter(patient=request.user).order_by('-created_at')
        add_items(
            orders, 
            'Medicine Order', 
            lambda x: f"Order #{x.id} ({x.items.count()} items)", 
            lambda x: sum(i.price_at_order * i.quantity for i in x.items.all()), 
            lambda x: 'Wallet/Insurance'
        )

    # 2. Bed Bookings
    if not filter_type or filter_type == 'bed':
        beds = BedBooking.objects.filter(patient=request.user).order_by('-created_at')
        price_map = {'ICU': 5000, 'GENERAL': 1000, 'EMERGENCY': 3000} # Mock logic
        add_items(
            beds,
            'Bed Booking',
            lambda x: f"{x.hospital_bed.get_bed_type_display()} at {x.hospital_bed.hospital.name}",
            lambda x: price_map.get(x.hospital_bed.bed_type, 1000),
            lambda x: x.get_payment_option_display()
        )

    # 3. Oxygen Bookings
    if not filter_type or filter_type == 'oxygen':
        oxy = OxygenBooking.objects.filter(patient=request.user).order_by('-created_at')
        add_items(
            oxy,
            'Oxygen Booking',
            lambda x: f"{x.stock.capacity_litres}L Cylinder x {x.quantity}",
            lambda x: x.stock.price_per_cylinder * x.quantity,
            lambda x: x.get_payment_option_display()
        )

    # 4. Doctor Appointments (New)
    if not filter_type or filter_type == 'appointment':
        appts = Appointment.objects.filter(patient=request.user).order_by('-created_at')
        add_items(
            appts,
            'Doctor Appointment',
            lambda x: f"{(x.doctor.name if x.doctor.name.startswith('Dr') else 'Dr. ' + x.doctor.name)} ({x.doctor.speciality})",
            lambda x: x.doctor.fees,
            lambda x: x.get_payment_option_display() if hasattr(x, 'get_payment_option_display') else 'Cash'
        )

    # Sort by date descending
    history.sort(key=lambda x: x['date'], reverse=True)

    # Optional: support "clear" query flag to not show any existing history
    if request.GET.get('clear') == '1':
        history = []

    return render(request, 'core/purchase_history.html', {
        'history': history,
        'filter_type': filter_type
    })


# --- PHARMACY ADMIN MANAGEMENT ---

@login_required
@role_required(['PHARMACY_ADMIN'])
def manage_medicines(request):
    try:
        pharmacy = request.user.pharmacy
    except Pharmacy.DoesNotExist:
        messages.error(request, 'You do not have a pharmacy profile associated.')
        return redirect('dashboard')

    medicines = pharmacy.medicines.all().order_by('-id')
    return render(request, 'core/medicines/manage_medicines.html', {
        'medicines': medicines,
        'pharmacy': pharmacy
    })

@login_required
@role_required(['PHARMACY_ADMIN'])
def add_medicine(request):
    try:
        pharmacy = request.user.pharmacy
    except Pharmacy.DoesNotExist:
        return redirect('dashboard')

    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.pharmacy = pharmacy
            medicine.save()
            messages.success(request, f'{medicine.name} added successfully.')
            return redirect('manage_medicines')
    else:
        form = MedicineForm()
    
    return render(request, 'core/medicines/medicine_form.html', {'form': form, 'title': 'Add Medicine'})

@login_required
@role_required(['PHARMACY_ADMIN'])
def delete_medicine(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk, pharmacy__user=request.user)
    name = medicine.name
    medicine.delete()
    messages.success(request, f'{name} deleted successfully.')
    return redirect('manage_medicines')


# --- OXYGEN SUPPLIER MANAGEMENT ---

@login_required
@role_required(['OXYGEN_SUPPLIER'])
def manage_oxygen(request):
    try:
        supplier = request.user.oxygen_supplier
    except OxygenSupplier.DoesNotExist:
        messages.error(request, 'You do not have a supplier profile associated.')
        return redirect('dashboard')

    stocks = supplier.stocks.all().order_by('-id')
    return render(request, 'core/oxygen/manage_oxygen.html', {
        'stocks': stocks,
        'supplier': supplier
    })

@login_required
@role_required(['OXYGEN_SUPPLIER'])
def add_oxygen_stock(request):
    try:
        supplier = request.user.oxygen_supplier
    except OxygenSupplier.DoesNotExist:
        return redirect('dashboard')

    if request.method == 'POST':
        form = OxygenStockForm(request.POST)
        if form.is_valid():
            stock = form.save(commit=False)
            stock.supplier = supplier
            stock.save()
            messages.success(request, 'Oxygen stock added successfully.')
            return redirect('manage_oxygen')
    else:
        form = OxygenStockForm()
    
    return render(request, 'core/oxygen/oxygen_stock_form.html', {'form': form, 'title': 'Add Oxygen Stock'})

@login_required
@role_required(['OXYGEN_SUPPLIER'])
def delete_oxygen_stock(request, pk):
    stock = get_object_or_404(OxygenCylinderStock, pk=pk, supplier__user=request.user)
    stock.delete()
    messages.success(request, 'Stock entry deleted successfully.')
    return redirect('manage_oxygen')

# --- HOSPITAL ADMIN (BEDS) MANAGEMENT ---

@login_required
@role_required(['HOSPITAL_ADMIN'])
def manage_beds(request):
    # Since Hospital Admin sees all, we list all beds groupings
    beds = HospitalBed.objects.select_related('hospital').all().order_by('hospital__name')
    return render(request, 'core/hospitals/manage_beds.html', {
        'beds': beds
    })

@login_required
@role_required(['HOSPITAL_ADMIN'])
def edit_bed_stock(request, pk):
    bed = get_object_or_404(HospitalBed, pk=pk)
    if request.method == 'POST':
        # Simple fallback form handling or direct Update
        try:
            available = int(request.POST.get('available_beds'))
            if available < 0: raise ValueError
            bed.available_beds = available
            bed.save()
            messages.success(request, f'Updated {bed.get_bed_type_display()} beds at {bed.hospital.name}.')
            return redirect('manage_beds')
        except (ValueError, TypeError):
            messages.error(request, 'Invalid bed count.')
    
    return render(request, 'core/hospitals/edit_bed_stock.html', {'bed': bed})


# --- ADMIN MANAGEMENT: OXYGEN (Platform Admin) ---

@login_required
@user_passes_test(is_super_admin)
def admin_manage_oxygen(request):
    stocks = OxygenCylinderStock.objects.select_related('supplier').all().order_by('-id')
    return render(request, 'core/manage/admin_oxygen_list.html', {
        'stocks': stocks
    })

@login_required
@user_passes_test(is_super_admin)
def admin_add_oxygen(request):
    if request.method == 'POST':
        form = AdminOxygenStockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oxygen stock added successfully.')
            return redirect('admin_manage_oxygen')
    else:
        form = AdminOxygenStockForm()
    
    return render(request, 'core/manage/admin_oxygen_form.html', {
        'form': form, 
        'title': 'Add Oxygen Stock (Admin)'
    })

@login_required
@user_passes_test(is_super_admin)
def admin_edit_oxygen_stock(request, pk):
    stock = get_object_or_404(OxygenCylinderStock, pk=pk)
    if request.method == 'POST':
        form = AdminOxygenStockForm(request.POST, instance=stock)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oxygen stock updated successfully.')
            return redirect('admin_manage_oxygen')
    else:
        form = AdminOxygenStockForm(instance=stock)
    
    return render(request, 'core/manage/admin_oxygen_form.html', {
        'form': form, 
        'title': 'Edit Oxygen Stock (Admin)'
    })

@login_required
@user_passes_test(is_super_admin)
def admin_delete_oxygen_stock(request, pk):
    stock = get_object_or_404(OxygenCylinderStock, pk=pk)
    stock.delete()
    messages.success(request, 'Oxygen stock deleted successfully.')
    return redirect('admin_manage_oxygen')



# --- ADMIN MANAGEMENT: BEDS (Platform Admin) ---

@login_required
@user_passes_test(is_super_admin)
def admin_manage_beds(request):
    beds = HospitalBed.objects.select_related('hospital').all().order_by('hospital__name', 'bed_type')
    return render(request, 'core/manage/admin_beds_list.html', {
        'beds': beds
    })

@login_required
@user_passes_test(is_super_admin)
def admin_add_bed(request):
    if request.method == 'POST':
        form = AdminHospitalBedForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hospital bed entry added successfully.')
            return redirect('admin_manage_beds')
    else:
        form = AdminHospitalBedForm()
    
    return render(request, 'core/manage/admin_bed_form.html', {
        'form': form, 
        'title': 'Add Hospital Bed (Admin)'
    })

@login_required
@user_passes_test(is_super_admin)
def admin_edit_bed_admin(request, pk):
    bed = get_object_or_404(HospitalBed, pk=pk)
    if request.method == 'POST':
        form = AdminHospitalBedForm(request.POST, instance=bed)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hospital bed entry updated successfully.')
            return redirect('admin_manage_beds')
    else:
        form = AdminHospitalBedForm(instance=bed)
    
    return render(request, 'core/manage/admin_bed_form.html', {
        'form': form, 
        'title': 'Edit Hospital Bed (Admin)'
    })

@login_required
@user_passes_test(is_super_admin)
def admin_delete_bed(request, pk):
    bed = get_object_or_404(HospitalBed, pk=pk)
    bed.delete()
    messages.success(request, 'Hospital bed entry deleted successfully.')
    return redirect('admin_manage_beds')
