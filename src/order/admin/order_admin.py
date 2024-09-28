from django.contrib import admin, messages
from django.utils.html import format_html
from django_q.tasks import async_task

from order.models.order import OrderInfo, OrderInfoHistory
from utils.services.stripe import StripePayment


@admin.register(OrderInfo)
class OrderInfoAdmin(admin.ModelAdmin):
    change_form_template = 'order/order_details.html'
    list_display = ['order_id', 'customer', 'subtotal', 'total', 'payment_method', 'transaction_id', 'tax', 'status',
                    'tracking_number']
    list_editable = ('status', 'tracking_number')
    search_fields = ('order_id', 'user__username', 'payment_method', 'payment_info__id', 'status', 'tracking_number')
    list_filter = ['payment_method', 'status']
    list_per_page = 25
    actions = ['make_received', 'make_processing', 'make_processed', 'make_shipped', 'make_delivered', 'make_returned',
               'make_canceled']

    def has_add_permission(self, request):
        return False

    @admin.action(description='customer')
    def customer(self, obj: OrderInfo):
        if not obj.user:
            return ''
        link = format_html(
            f'<a  '
            f'href="/super-admin/authentication/user/{obj.user.id}/change/"> '
            f'{obj.user.first_name + " " + obj.user.last_name}<br>{obj.user.company_name}</a>&nbsp;'
        )
        return link

    @admin.action(description='transaction_id')
    def transaction_id(self, obj: OrderInfo):
        if obj.payment_info:
            return obj.payment_info['id']
        return 'Not Paid'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        order_info = OrderInfo.objects.filter(id=object_id).first()
        extra_context = {
            'order': order_info,
            'title': ''
        }
        return super(OrderInfoAdmin, self).change_view(request, object_id, form_url, extra_context)

    @admin.action(description='Change selected status received')
    def make_received(self, request, queryset):
        queryset.update(status='received')

    @admin.action(description='Change selected status processing')
    def make_processing(self, request, queryset):
        queryset.update(status='processing')
        # for obj in queryset:
        #     user = obj.user
        #     if user and obj.status != 'in_review':
        #         async_task('order.jobs.emails.send_email_to_customers_order_in_review', user)
        # queryset.update(status='in_review')

    @admin.action(description='Change selected status processed')
    def make_processing(self, request, queryset):
        queryset.update(status='processed')

    @admin.action(description='Change selected status delivered')
    def make_delivered(self, request, queryset):
        queryset.update(status='delivered')

    @admin.action(description='Change selected status Cancel')
    def make_canceled(self, request, queryset):
        stripe = StripePayment()
        for item in queryset:
            response = stripe.refund(item)
            if response is True:
                item.status = 'canceled'
                item.save()

    @admin.action(description='Change selected status shipped')
    def make_shipped(self, request, queryset):
        for obj in queryset:
            if obj.tracking_number is None:
                messages.warning(request, "Tracking number field is required")
            else:
                obj.status = 'shipped'
                obj.save()
        # queryset.update(status='shipped')

    def check_tracking_number(self, obj, status):
        if obj.tracking_number is None:
            return 'tracking_number'
        else:
            self.status_changer(obj, status)
            return True

    def status_changer(self, obj, status):
        obj.status = status
        obj.save()
        return True

    def status_cancel(self, obj, status):
        stripe = StripePayment()
        response = stripe.refund(obj)
        if response is True:
            obj.status = status
            obj.save()
            return True
        return "already_refund"

    def save_model(self, request, obj, form, change):
        if obj.status == 'processing':
            async_task('order.jobs.emails.send_email_to_customers_order_in_review', obj.user)
        status_switcher = {
            'received': self.status_changer,
            'processing': self.status_changer,
            'processed': self.status_changer,
            'shipped': self.check_tracking_number,
            'delivered': self.status_changer,
            # 'returned': self.status_cancel,
            'canceled': self.status_cancel,
        }
        switcher_obj = status_switcher.get(obj.status)
        state = False
        if switcher_obj:
            state = switcher_obj(obj, obj.status)

        if state is True:
            super().save_model(request, obj, form, change)
        elif state == 'tracking_number':
            messages.warning(request, "Tracking number field is required")
        elif state == 'already_refund':
            messages.warning(request, "Already refunded. that's why you can't cancel the order")


@admin.register(OrderInfoHistory)
class OrderHistoryAdmin(admin.ModelAdmin):
    change_form_template = 'order/order_details.html'
    list_display = ['order', 'customer', 'subtotal', 'total', 'tax', 'payment_method', 'status']
    list_filter = ['payment_method', 'status']
    list_per_page = 25
    search_fields = ('order_id', 'status', 'user__username', 'payment_method')

    def has_add_permission(self, request):
        return False

    @admin.action(description='Order ID')
    def order(self, obj: OrderInfoHistory):
        if obj.modified_number > 0:
            return f'{obj.order_id} m-{obj.modified_number}'
        return obj.order_id

    @admin.action(description='customer')
    def customer(self, obj: OrderInfoHistory):
        if not obj.user:
            return ''
        link = format_html(
            f'<a  '
            f'href="/super-admin/authentication/user/{obj.user.id}/change/"> '
            f'{obj.user.first_name + " " + obj.user.last_name}<br>{obj.user.company_name}</a>&nbsp;'
        )
        return link

    def change_view(self, request, object_id, form_url='', extra_context=None):
        order_info = OrderInfoHistory.objects.filter(id=object_id).first()
        extra_context = {
            'order': order_info,
            'title': ''
        }
        return super().change_view(request, object_id, form_url, extra_context)
