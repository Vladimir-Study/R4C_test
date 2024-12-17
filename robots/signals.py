from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string

from robots.models import Robot
from orders.models import Order


@receiver(post_save, sender=Robot)
def create_notification_for_consumer(sender, instance, created, **kwargs):
    """
    В случае создания робота буде получен сигнал,
    после чего происходит проверка заказа на данный робот,
    если есть заказ без серийного номера, заказу присваивается
    номер робота, и заказчику отправляется Email.
    """
    if created:
        orders = Order.objects.filter(model=instance.model, version=instance.version)
        if not orders:
            return
        for order in orders:
            if not order.robot_serial:
                order.robot_serial = instance.serial
                order.save()
                message = render_to_string(
                    "templates/email/email.html",
                    {"model": instance.model, "version": instance.version},
                )
                send_mail(
                    "Welcome!",
                    message,
                    "Yasoob@mail.ru",
                    [order.customer.email],
                    fail_silently=False)
                break

