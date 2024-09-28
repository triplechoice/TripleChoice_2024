from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from authentication.models import User


def send_email_to_suppliers_review(part):
    suppliers = []
    for supplier in part.supplier.all():
        suppliers.append(supplier.email)
    mail_subject = 'Email to the supplier'
    message = render_to_string('emails/email_to_suppliers.html', {
        'test': 'test message'
    })
    email = EmailMessage(
        mail_subject, message, to=suppliers
    )
    email.content_subtype = "html"
    email.send()


def send_email_to_customers_order_in_review(user):
    mail_subject = 'Email to the Customer'
    message = render_to_string('emails/email_to_customer.html', {
        'test': 'test message to the customer'
    })
    email = EmailMessage(
        mail_subject, message, to=[user.email]
    )
    email.content_subtype = "html"
    email.send()
