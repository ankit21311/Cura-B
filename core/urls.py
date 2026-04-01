from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('dashboard/hospital-admin/', views.hospital_admin_dashboard, name='hospital_admin_dashboard'),
    path('dashboard/pharmacy-admin/', views.pharmacy_admin_dashboard, name='pharmacy_admin_dashboard'),
    path('dashboard/oxygen-supplier/', views.oxygen_supplier_dashboard, name='oxygen_supplier_dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),

    path('hospitals/', views.hospital_list, name='hospital_list'),
    path('hospitals/<int:pk>/', views.hospital_detail, name='hospital_detail'),
    path('hospitals/book-bed/<int:bed_id>/', views.bed_booking_create, name='bed_booking_create'),
    path('hospitals/book-bed/payment/<int:booking_id>/', views.bed_booking_payment, name='bed_booking_payment'),

    path('doctors/search/', views.doctor_search, name='doctor_search'),
    path('doctors/<int:pk>/', views.doctor_detail, name='doctor_detail'),
    path('doctors/<int:doctor_id>/book/', views.book_appointment, name='book_appointment'),

    path('oxygen/', views.oxygen_list, name='oxygen_list'),
    path('oxygen/booking/<int:stock_id>/', views.oxygen_booking_create, name='oxygen_booking_create'),

    path('medicines/search/', views.medicine_search, name='medicine_search'),
    path('medicines/order/<int:medicine_id>/', views.medicine_order_create, name='medicine_order_create'),
    path('medicines/cart/', views.cart_detail, name='cart_detail'),
    path('medicines/cart/add/<int:medicine_id>/', views.cart_add, name='cart_add'),
    path('medicines/cart/update/<int:item_id>/', views.cart_update, name='cart_update'),
    path('medicines/cart/remove/<int:item_id>/', views.cart_remove, name='cart_remove'),
    path('medicines/cart/checkout/', views.cart_checkout, name='cart_checkout'),

    path('notifications/', views.notifications_list, name='notifications_list'),
    path('notifications/<int:pk>/read/', views.notification_mark_read, name='notification_mark_read'),

    # Wallet
    path('wallet/', views.wallet_dashboard, name='wallet_dashboard'),
    path('wallet/recharge/', views.wallet_recharge, name='wallet_recharge'),
    path('wallet/insurance/', views.manage_insurance, name='manage_insurance'),
    path('history/', views.purchase_history, name='purchase_history'),

    path('emergency-contacts/', views.emergency_contacts, name='emergency_contacts'),
    path('support-request/', views.support_request_create, name='support_request_create'),

    # CURA Assistant (AI-like helper)
    path('assistant/', views.assistant_home, name='assistant_home'),
    path('assistant/api/', views.assistant_api, name='assistant_api'),

    # Admin quick actions for requests
    path('manage/appointments/<int:pk>/status/', views.admin_update_appointment_status, name='admin_update_appointment_status'),
    path('manage/medicine-orders/<int:pk>/status/', views.admin_update_medicine_order_status, name='admin_update_medicine_order_status'),
    path('manage/oxygen-bookings/<int:pk>/status/', views.admin_update_oxygen_booking_status, name='admin_update_oxygen_booking_status'),
    path('manage/bed-bookings/<int:pk>/status/', views.admin_update_bed_booking_status, name='admin_update_bed_booking_status'),
    path('manage/support-requests/<int:pk>/status/', views.admin_update_support_request_status, name='admin_update_support_request_status'),

    # --- ADMIN MANAGEMENT: DOCTORS ---
    path('manage/doctors/', views.manage_doctors, name='manage_doctors'),
    path('manage/doctors/create/', views.create_doctor, name='create_doctor'),
    path('manage/doctors/<int:pk>/edit/', views.edit_doctor, name='edit_doctor'),
    path('manage/doctors/<int:pk>/toggle/', views.toggle_doctor_status, name='toggle_doctor_status'),

    # --- ADMIN MANAGEMENT: MEDICINES (Pharmacy Admin) ---
    path('manage/medicines/', views.manage_medicines, name='manage_medicines'),
    path('manage/medicines/add/', views.add_medicine, name='add_medicine'),
    path('manage/medicines/<int:pk>/delete/', views.delete_medicine, name='delete_medicine'),

    # --- ADMIN MANAGEMENT: OXYGEN (Oxygen Supplier) ---
    path('manage/oxygen/', views.manage_oxygen, name='manage_oxygen'),
    path('manage/oxygen/add/', views.add_oxygen_stock, name='add_oxygen_stock'),
    path('manage/oxygen/<int:pk>/delete/', views.delete_oxygen_stock, name='delete_oxygen_stock'),

    # --- ADMIN MANAGEMENT: OXYGEN (Platform Admin) ---
    path('manage/admin/oxygen/', views.admin_manage_oxygen, name='admin_manage_oxygen'),
    path('manage/admin/oxygen/add/', views.admin_add_oxygen, name='admin_add_oxygen'),
    path('manage/admin/oxygen/<int:pk>/edit/', views.admin_edit_oxygen_stock, name='admin_edit_oxygen_stock'),
    path('manage/admin/oxygen/<int:pk>/delete/', views.admin_delete_oxygen_stock, name='admin_delete_oxygen_stock'),

    # --- ADMIN MANAGEMENT: BEDS (Hospital Admin) ---
    path('manage/beds/', views.manage_beds, name='manage_beds'),
    path('manage/beds/<int:pk>/edit/', views.edit_bed_stock, name='edit_bed_stock'),

    # --- ADMIN MANAGEMENT: BEDS (Platform Admin) ---
    path('manage/admin/beds/', views.admin_manage_beds, name='admin_manage_beds'),
    path('manage/admin/beds/add/', views.admin_add_bed, name='admin_add_bed'),
    path('manage/admin/beds/<int:pk>/edit/', views.admin_edit_bed_admin, name='admin_edit_bed_admin'),
    path('manage/admin/beds/<int:pk>/delete/', views.admin_delete_bed, name='admin_delete_bed'),

]

