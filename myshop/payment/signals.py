from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from io import BytesIO
import weasyprint

from orders.models import Order


def payment_notification(sender, **kwargs):
    ipb_obj = sender
    if ipb_obj.payment_status == ST_PP_COMPLETED:
        order = get_object_or_404(Order, id=ipb_obj.invoice)
        order.paid = True
        order.save()
        subject = "My shop - invoice no {}".format(order.id)
        message = "Please find the invoice for your last order attached."
        email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])
        html = render_to_string('admin/orders/order/pdf.html', {'order': order})
        out = BytesIO()
        stylesheets = [weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')]
        weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)
        email.attach('order_{}.pdf'.format(order.id), out.getvalue(), 'application/pdf')
        email.send()


valid_ipn_received.connect(payment_notification)
