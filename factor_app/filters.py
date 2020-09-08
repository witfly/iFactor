from django.contrib.auth.models import User
import django_filters
from factor_app.models import Invoice

class InvoiceFilter(django_filters.FilterSet):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'total_amount', 'purchase_option', 'invoice_status']