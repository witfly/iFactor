#from django_filters.rest_framework import djangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.pagination import LimitOffsetPagination
# from rest_framework import django_filters
# from rest_framework.response import response
from rest_framework import status
from factor_app.models import Client, Invoice, ProcessingItem, Basket
from .serializers.processing_serializers import ProcessingSerializer, ProcessingClientInvoiceSerializer,ProcessingTermSerializer,ProcessingInvoiceDetailSerializer




class ProcessingListView(ListAPIView):
    #serializer_class = ProcessingSerializer
    #context_object_name = 'client_pending_purchase_summary'
    #def get_queryset(self):
    #    return Processing.objects.all()
    serializer_class = ProcessingSerializer
    def get_queryset(self):
        return ProcessingItem.objects.filter(invoices__id=invoice.invoice_id).count()
            
    
class ProcessingClientInvoicesListView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ProcessingClientInvoiceSerializer
    def get_queryset(self):
        queryset = Client.objects.all()
        this_client = self.kwargs['client_id']
        return queryset.filter(client_id = this_client)

class ProcessingInvoiceDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = ProcessingInvoiceDetailSerializer
    def get_queryset(self):
        queryset = Invoice.objects.all()
        #this_invoice = self.kwargs['invoice_id']
        return queryset # .filter(invoice_id = this_invoice)
    def update(self, validated_data, pk):
        data = validated_data
        line_items_validated_data = data.pop('line_items')
        invoice = Invoice.objects.update(**data)
        line_items_serializer = self.fields['line_items']
        for each in line_items_data:
            each['invoice'] = invoice
        line_items = line_items_serializer.update(line_items_data)
        return invoice