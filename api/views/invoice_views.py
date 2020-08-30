""" 
#from django_filters.rest_framework import djangoFilterBackend
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from rest_framework.pagination import LimitOffsetPagination
# from rest_framework import django_filters
# from rest_framework.response import response
from rest_framework import status
from factor_app.models import  Invoice, InvoiceLineItems
from ..serializers.invoice_serializers import (
    InvoiceSerializer
)



class InvoiceView(RetrieveUpdateDestroyAPIView):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    def get_queryset(self):
        queryset = Invoice.objects.all()
        return queryset
    
    def create(self, validated_data):
        line_items = validated_data.pop('line_items', [])
        invoice = Invoice.objects.create(**validated_data)
        for line_items_dict in invoice:
            line_items_dict['invoice'] = invoice
            InvoiceLineItems.objects.create(**line_items_dict)
        return invoice
    
    
    
    def update(self, validated_data, pk):
        data = validated_data
        line_items_validated_data = data.pop('line_items')
        invoice = Invoice.objects.update(**data)
        line_items_serializer = self.fields['line_items']
        for each in line_items_data:
            each['invoice'] = invoice
        line_items = line_items_serializer.update(line_items_data)
        return invoice """
        
from factor_app.models import Invoice, InvoiceLineItems
from ..serializers.invoice_serializers import InvoiceSerializer
from rest_framework import viewsets
from rest_framework.response import Response


    
class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    
