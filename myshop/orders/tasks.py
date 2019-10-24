from celery import task
from django.core.mail import send_mail
from .models import Order


@task
def order_created(order_id):
    """
    Task sending e-mail notification after a successful order
    :param order_id:
    :return:
    """
    order = Order.objects.get(id=order_id)
    subject = 'Order {}'.format(order_id)
    message = 'Hello, {}!\n\nYou successfully ordered from our shop. Your order number is {}.'.format(order.first_name, order.id)

    mail_sent = send_mail(subject, message, 'admin@myshop.com', [order.email])
    return mail_sent
