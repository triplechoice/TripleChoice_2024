from django.contrib import admin, messages
from django.utils.html import format_html
from order.models.request import Request, RequestHistory, RequestReview, SelectedRequestReview, RequstReviewAttachment
from order.admin.request_status_handler.status_switcher import update_request_status


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    change_form_template = 'request_details.html'
    list_display = ['request_id', 'reference_request', 'quantity', 'type', 'customer', 'created_at', 'admin_status']
    list_editable = ('admin_status',)
    actions = ['make_pending', 'sent_to_supplier', 'received_results_from_supplier', 'completed', 'cancelled']
    list_per_page = 10
    list_filter = ['admin_status', 'type']
    search_fields = ('order_id',)

    def has_add_permission(self, request):
        return False

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'admin_status':
            kwargs['choices'] = (
                ("pending", "Pending"),
                ("sent_to_supplier", "Sent to supplier"),
                ("received_results_from_supplier", "Received results from supplier"),
                ("completed", "Completed"),
                ("cancelled", "Cancelled"),
            )
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def changelist_view(self, request, extra_context=None):
        response = super(RequestAdmin, self).changelist_view(request, extra_context)
        total_request = Request.objects.all().count()
        total_pending = Request.objects.filter(admin_status='pending').count()
        total_sent_to_supplier = Request.objects.filter(admin_status='sent_to_supplier').count()
        total_supplier_send_review = Request.objects.filter(admin_status='received_results_from_supplier').count()
        total_completed = Request.objects.filter(admin_status='completed').count()
        total_cancelled = Request.objects.filter(admin_status='cancelled').count()

        extra_context = {
            'total_request': total_request,
            'total_pending': total_pending,
            'total_sent_to_supplier': total_sent_to_supplier,
            'total_supplier_send_review': total_supplier_send_review,
            'total_completed': total_completed,
            'total_cancelled': total_cancelled
        }
        try:
            response.context_data.update(extra_context)
        except Exception as e:
            pass
        return response

    @admin.action(description='reference request')
    def reference_request(self, obj: Request):
        if not obj.ref_request:
            return ""

        object_id = Request.objects.filter(order_id=obj.ref_request).first()
        if object_id:
            link = format_html(
                f'<a  '
                f'href="/super-admin/order/request/{object_id.id}/change/"> '
                f'{obj.ref_request}</a>&nbsp;'
            )
            return link
        return ""

    def request_id(self, obj: Request):
        return obj.order_id

    @admin.action(description='customer')
    def customer(self, obj: Request):
        if not obj.user:
            return ""

        link = format_html(
            f'<a  '
            f'href="/super-admin/authentication/user/{obj.user.id}/change/"> '
            f'{obj.user.first_name + " " + obj.user.last_name}<br>{obj.user.company_name}</a>&nbsp;'
        )
        return link

    def change_view(self, request, object_id, form_url='', extra_context=None):
        order_info = Request.objects.filter(id=object_id).first()
        extra_context = {
            "order": order_info,
            'title': '',
        }
        return super(RequestAdmin, self).change_view(request, object_id, form_url, extra_context)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            obj.soft_delete()

    def save_model(self, request, obj, form, change):
        update_request_status(request, obj)
        # super().save_model(request, obj, form, change)

    # TODO:need to add for save button action also

    @admin.action(description='Change selected status pending')
    def make_pending(self, request, queryset):
        for obj in queryset:
            obj.admin_status = 'pending'
            update_request_status(request, obj)

    @admin.action(description='Send to the suppliers')
    def sent_to_supplier(self, request, queryset):
        for obj in queryset:
            obj.admin_status = 'sent_to_supplier'
            update_request_status(request, obj)

    @admin.action(description='Received results from supplier')
    def received_results_from_supplier(self, request, queryset):
        for obj in queryset:
            obj.admin_status = 'received_results_from_supplier'
            update_request_status(request, obj)

    @admin.action(description='Change status as completed')
    def completed(self, request, queryset):
        for obj in queryset:
            obj.admin_status = 'completed'
            update_request_status(request, obj)

    @admin.action(description='Change selected status cancelled')
    def cancelled(self, request, queryset):
        for obj in queryset:
            obj.admin_status = 'cancelled'
            update_request_status(request, obj)


@admin.register(RequestHistory)
class RequestHistoryAdmin(admin.ModelAdmin):
    list_display = ['order', 'quantity', 'type', 'updated_at', 'cost']
    list_per_page = 25
    search_fields = ('order_id', 'type')
    list_filter = ['type']
    change_form_template = 'request_details.html'

    @admin.action(description='Order ID')
    def order(self, obj: RequestHistory):
        if obj.modified_number > 0:
            return f'{obj.order_id} m-{obj.modified_number}'
        return obj.order_id

    def has_add_permission(self, request):
        return False

    def change_view(self, request, object_id, form_url='', extra_context=None):
        order_info = RequestHistory.objects.filter(id=object_id).first()
        extra_context = {
            "order": order_info,
            'title': '',
        }
        return super(RequestHistoryAdmin, self).change_view(request, object_id, form_url, extra_context)


class RequestReviewAttachmentInline(admin.TabularInline):
    model = RequstReviewAttachment


@admin.register(RequestReview)
class RequestReviewAdmin(admin.ModelAdmin):
    list_display = ['request_id', 'action', 'title', 'user_name', 'review_in_selected', 'quantity', 'cost', 'cost_unit',
                    'lead_time', 'unit', 'show_supplier_cost', 'show_supplier_lead_time', 'attachments']
    search_fields = ['order_id']
    list_filter = ('user',)
    list_display_links = ()
    inlines = [
        RequestReviewAttachmentInline
    ]
    actions = ['make_selected_review', 'remove_selected_review']
    list_editable = ['cost', 'lead_time', 'unit', 'cost_unit']
    list_per_page = 25

    @admin.action(description='Supplier cost')
    def show_supplier_cost(self, obj: RequestReview):
        return f"{obj.supplier_cost} {obj.supplier_cost_unit.capitalize()}"

    @admin.action(description='Supplier Lead Time')
    def show_supplier_lead_time(self, obj: RequestReview):
        return f"{obj.supplier_lead_time} {obj.supplier_unit.capitalize()}"

    def get_list_display_links(self, request, list_display):
        return None

    def get_queryset(self, request):
        if request.GET.get('e'):
            queryset = RequestReview.objects.filter(request__order_id=request.GET.get('q'))
        else:
            queryset = Request.objects.all()
        return queryset

    def get_list_filter(self, request):
        list_filters = list(self.list_filter)
        if request.GET.get('e'):
            return []
        return list_filters

    def get_search_fields(self, request):
        search_fields = list(self.search_fields)
        if request.GET.get('e'):
            search_fields = None
            return search_fields
        return search_fields

    def get_actions(self, request):
        actions = super().get_actions(request)
        if request.GET.get('e'):
            return actions
        return None

    def get_list_display(self, request):
        list_display = list(self.list_display)
        if request.GET.get('e'):
            list_display.remove('request_id')
            list_display.remove('action')
        else:
            list_display.remove('title')
            list_display.remove('user_name')
            list_display.remove('review_in_selected')
            list_display.remove('attachments')
            list_display.remove('quantity')
            list_display.remove('lead_time')
            list_display.remove('cost')
            list_display.remove('show_supplier_lead_time')
            list_display.remove('show_supplier_cost')
            list_display.remove('cost_unit')
            list_display.remove('unit')

        return list_display

    @admin.action(description='Action')
    def action(self, obj: Request):
        button = format_html(
            f'<a class="button" '
            f'href="/super-admin/order/requestreview/?q={obj.order_id}&&e=1"> '
            f'Show reviews</a>&nbsp;'
        )
        return button

    def review_in_selected(self, obj):
        if SelectedRequestReview.objects.filter(review=obj).exists():
            return "Yes"
        return "No"

    def request_id(self, obj):
        return obj.order_id

    @admin.action(description='Make review as selected review')
    def make_selected_review(self, request, queryset):
        if queryset:
            obj = SelectedRequestReview.objects.filter(request=queryset[0].request).first()
            if not obj:
                obj = SelectedRequestReview.objects.create(request=queryset[0].request)
                obj.save()

            request_order_id = obj.request.order_id
            request_obj = Request.objects.get(order_id=request_order_id)
            obj.review.add(*queryset)
            request_obj.admin_status = 'completed'
            request_obj.moderator_status = 'completed'
            request_obj.customer_status = 'results'
            request.supplier_status = 'submitted'
            request_obj.save()

    @admin.action(description='Remove review from selected review')
    def remove_selected_review(self, request, queryset):
        if queryset:
            obj = SelectedRequestReview.objects.filter(request=queryset[0].request).first()
            if obj:
                obj.review.remove(*queryset)
            if len(obj.review.all()) < 1:
                # queryset[0].request.customer_status = 'in_review'
                # queryset[0].request.admin_status = 'supplier_sent_review'
                queryset[0].request.admin_status = 'received_results_from_supplier'
                queryset[0].request.moderator_status = 'new_review'
                queryset[0].request.customer_status = 'in_review'
                queryset[0].request.supplier_status = 'submitted'
                queryset[0].request.save()

    def user_name(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name

    def attachments(self, obj):
        items = list(obj.attachments.all())
        button = ''
        for item in items:
            if item.file:
                button += f'<a class="button" target="_blank" ' f'href="/media/{item.file}">' f'Attachment</a>&nbsp;'
        return format_html(button)

    def save_model(self, request, obj, form, change):
        if obj.id is None:
            obj.save()
            request_obj = obj.request
            if request_obj:
                request_obj.admin_status = 'received_results_from_supplier'
                request_obj.moderator_status = 'new_review'
                request_obj.customer_status = 'in_review'
                request_obj.supplier_status = 'submitted'
                request_obj.save()
        else:
            if obj.lead_time < 0.0:
                messages.warning(request, 'Lead time cannot be negative')
            if obj.cost < 0.0:
                messages.warning(request, 'Cost cannot be negative')
            if obj.lead_time > 0.0 and obj.cost > 0.0:
                super().save_model(request, obj, form, change)
