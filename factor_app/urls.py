from django.shortcuts import render
from django.conf.urls import url
from django.urls import path, include, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from  api.views.processing_views import ProcessingListView, ProcessingClientInvoicesListView, ProcessingInvoiceDetailView
from api.views.invoice_views import InvoiceViewSet

urlpatterns = [
    
    path('processing/client/<int:client_id>', ProcessingClientInvoicesListView.as_view(), name='processing_client_invoices'),
    # path('processing/invoice_detail/<int:invoice_id>/', ProcessingInvoiceDetailView.as_view(), name='processing_client_invoice_detail'),
    path('processing/invoice/<pk>/', ProcessingInvoiceDetailView.as_view(), name='processing_client_invoice_detail'),
    path('processing/', ProcessingListView.as_view(), name='processing'),
    
    path('invoice/<pk>/',InvoiceViewSet, name='invoice'),
    path('invoice/',InvoiceViewSet, name='invoice')
    
]
