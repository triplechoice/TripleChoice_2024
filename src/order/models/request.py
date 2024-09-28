from abc import abstractproperty
from datetime import datetime

from django.core.validators import FileExtensionValidator

from authentication.models import User
from django.db import models

# Create your models here.
from product.models.product_models import Part, Classification
from triple_choice.db.mixins import AuthorMixin, TimeStampMixin


class RequestAbstract(AuthorMixin, TimeStampMixin):
    TYPE = (
        ("query", "Query"),
        ("quote", "Quote"),
    )
    REQUEST_STATUS = (
        ("pending", "Pending"),
        ("in_review", "In Review"),
        ("sent_to_supplier", "Sent to supplier"),
        ("processing", "Processing"),
        ("new_request", "New request"),
        ("received_results_from_supplier", "Received results from supplier"),
        ("new_review", "New review"),
        ("completed", "Completed"),
        ("results", "Results"),
        ("submitted", "Submitted"),
        ("cancelled", "Cancelled"),
        ("quote_submitted", "Quote Submitted"),
        ("query_submitted", "Query Submitted"),

    )

    part = models.ForeignKey(Part, null=True, on_delete=models.SET_NULL)
    answer = models.JSONField()
    comment = models.CharField(max_length=1000, blank=True, null=True)
    image_comment = models.FileField(upload_to="media/post/", null=True, blank=True)
    contact_info = models.JSONField()
    quantity = models.PositiveIntegerField()
    type = models.CharField(max_length=10, choices=TYPE)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    modified_number = models.IntegerField(default=0)
    lead_time = models.CharField(max_length=255, blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    is_estimated = models.BooleanField(default=False, blank=True, null=True)
    ref_request = models.CharField(max_length=255, blank=True)
    review_id = models.IntegerField(blank=True, null=True)
    admin_status = models.CharField(max_length=50, choices=REQUEST_STATUS, blank=True, null=True)
    customer_status = models.CharField(max_length=50, choices=REQUEST_STATUS, blank=True, null=True)
    supplier_status = models.CharField(max_length=50, choices=REQUEST_STATUS, blank=True, null=True)
    moderator_status = models.CharField(max_length=50, choices=REQUEST_STATUS, blank=True, null=True)
    zip_code = models.CharField(max_length=50)

    class Meta:
        abstract = True


class RequestHistory(RequestAbstract):
    order_id = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.order_id


class SoftDeleteManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class SoftDeletedDataManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)


class SoftDeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)
    objects = SoftDeleteManager()
    all_objects = models.Manager()
    deleted_objects = SoftDeletedDataManager()

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def restore(self):
        self.is_deleted = False
        self.save()

    class Meta:
        abstract = True


# TODO:show choice field value in template
class Request(RequestAbstract, SoftDeleteModel):
    order_id = models.CharField(max_length=255, blank=True, unique=True)

    def __str__(self):
        return self.order_id


class RequestReview(AuthorMixin, TimeStampMixin, SoftDeleteModel):
    UNIT_CHOICE = (
        ('day', 'Day'),
        ('week', 'Week'),
        ('month', 'Month')
    )
    COST_UNIT_CHOICE = (
        ('EUR', '€-EUR'),
        ('USD', '$-USD'),
        ('CNY', '¥-CNY'),
    )
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    lead_time = models.FloatField(blank=True, null=True)
    cost = models.FloatField(blank=True, null=True)
    cost_unit = models.CharField(max_length=10, choices=COST_UNIT_CHOICE, default='USD')
    supplier_cost_unit = models.CharField(max_length=10, choices=COST_UNIT_CHOICE, default='USD')
    supplier_lead_time = models.FloatField()
    supplier_cost = models.FloatField()
    unit = models.CharField(max_length=255, choices=UNIT_CHOICE, default='day')
    supplier_unit = models.CharField(max_length=255, choices=UNIT_CHOICE, default='day')

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(cost__gt=('0.0')), name='cost_gt_0'),
            models.CheckConstraint(check=models.Q(supplier_cost__gt=('0.0')), name='supplier_cost_gt_0'),
            models.CheckConstraint(check=models.Q(lead_time__gt=('0.0')), name='lead_time_gt_0'),
            models.CheckConstraint(check=models.Q(supplier_lead_time__gt=('0.0')), name='supplier_lead_time_gt_0'),
        ]

    def __str__(self):
        return self.request.order_id


class RequstReviewAttachment(TimeStampMixin):
    file = models.FileField(help_text='Allow PDF file only', validators=[FileExtensionValidator(['pdf'])])
    request_review = models.ForeignKey(RequestReview, related_name='attachments', on_delete=models.CASCADE)


class SelectedRequestReview(AuthorMixin, TimeStampMixin):
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    review = models.ManyToManyField(RequestReview)

    def __str__(self):
        return self.request.order_id
