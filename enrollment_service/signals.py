from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Enrollment, Payment

@receiver(post_save, sender=Enrollment)
def create_payment(sender, instance, created, **kwargs):
    enrollment = instance
    if created:
        Payment.objects.create(enrollment=enrollment, amount=enrollment.course.price)
