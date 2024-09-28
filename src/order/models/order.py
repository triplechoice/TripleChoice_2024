from django.db import models
from triple_choice.db.mixins import AuthorMixin, TimeStampMixin
from order.models.request import Request, RequestReview
from authentication.models import User
from order.models.request import SoftDeleteModel


class OrderAddress(AuthorMixin, TimeStampMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255)
    phone_no = models.CharField(max_length=255, blank=True, null=True)
    street_no = models.CharField(max_length=255)
    building_no = models.CharField(max_length=255, blank=True, null=True)
    state = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_code = models.CharField(max_length=20)

    class Meta:
        abstract = True


class BillingAddress(OrderAddress):
    pass


class ShippingAddress(OrderAddress):
    pass


class OrderAbstract(AuthorMixin, TimeStampMixin):
    PAYMENT_METHOD = (
        ('stripe', 'Stripe'),
    )
    ORDER_STATUS = (
        ("received", "Received"),
        ("processing", "Processing"),
        ("processed", "Processed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
        ("returned", "Returned"),
        ("canceled", "Canceled"),

    )
    order_id = models.CharField(max_length=255, blank=True)
    request = models.ForeignKey(Request, on_delete=models.DO_NOTHING)
    billing_address = models.OneToOneField(BillingAddress, on_delete=models.DO_NOTHING)
    shipping_address = models.OneToOneField(ShippingAddress, on_delete=models.DO_NOTHING)
    subtotal = models.DecimalField(max_digits=15, decimal_places=2)
    total = models.DecimalField(max_digits=15, decimal_places=2)
    tax = models.DecimalField(max_digits=15, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD)
    quantity = models.FloatField()
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=50, choices=ORDER_STATUS, blank=True, null=True)
    modified_number = models.IntegerField(default=0)
    review = models.ForeignKey(RequestReview, blank=True, null=True, on_delete=models.DO_NOTHING)
    payment_info = models.JSONField(null=True, blank=True)
    refund_info = models.JSONField(null=True, blank=True)
    tracking_number = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        abstract = True


class OrderInfo(OrderAbstract, SoftDeleteModel):
    pass

    def __str__(self):
        return f"{self.order_id}"


class OrderInfoHistory(OrderAbstract):
    pass

    def __str__(self):
        return f"{self.order_id}"
