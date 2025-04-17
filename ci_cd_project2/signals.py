from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Good, Notification, CustomUser

@receiver(post_save, sender=Good)
def notify_subscribers_when_available(sender, instance, **kwargs):
    """
    Якщо товар з'явився в наявності (count > 0) і раніше був відсутній,
    надсилаємо повідомлення підписаним користувачам.
    """
    if instance.count > 0:  # Товар став доступним
        subscribers = instance.subscribers.all()

        for user in subscribers:
            Notification.objects.create(
                message=f"Товар '{instance.name}' знову доступний у продажу!",
                status="unread",
                user=user,
                good=instance
            )
