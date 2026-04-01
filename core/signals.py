from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Wallet

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_wallet(sender, instance, created, **kwargs):
    """
    Auto-create a Wallet for every new user.
    """
    if created:
        Wallet.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_wallet(sender, instance, **kwargs):
    """
    Ensure wallet is saved when user is saved.
    """
    if hasattr(instance, 'wallet'):
        instance.wallet.save()

from .models import BedBooking, InsurancePolicy, Notification

@receiver(post_save, sender=BedBooking)
def notify_bed_booking_approval(sender, instance, created, **kwargs):
    """
    Notify patient when BedBooking is approved (CONFIRMED).
    """
    if not created and instance.status == 'CONFIRMED':
        # Check if we recently sent this to avoid spam (optional, but good practice)
        # For now, we just create it.
        Notification.objects.create(
            user=instance.patient,
            message=f"Your bed booking at {instance.hospital_bed.hospital.name} has been APPROVED.",
            notification_type='BED'
        )

@receiver(post_save, sender=InsurancePolicy)
def notify_insurance_approval(sender, instance, created, **kwargs):
    """
    Notify patient when InsurancePolicy is verified (VERIFIED).
    """
    if not created and instance.status == 'VERIFIED':
        Notification.objects.create(
            user=instance.user,
            message=f"Your insurance policy {instance.policy_number} has been VERIFIED.",
            notification_type='SUPPORT' # Using SUPPORT type as generic, or could add INSURANCE type
        )
