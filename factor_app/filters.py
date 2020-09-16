from django_filters import rest_framework as filters
from factor_app.models import Invoice
from factor_app.api.serializers import ClientDetailSerializer

class InvoiceFilter(filters.FilterSet):
    serializer_class = ClientDetailSerializer
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'total_amount', 'purchase_option', 'invoice_status']