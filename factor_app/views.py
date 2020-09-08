from django.shortcuts import render
from django.db.models import Sum
from decimal import *
from .filters import InvoiceFilter

from django.http import HttpResponse
from .models import Invoice
from django.db.models import FloatField

def home(request):
    invoice = Invoice.objects.all()
    invoice_number = list()

    total_amount = 0.00
    
    for invoice in invoice:
  
    #response_html = '<br>'.join(invoice_number, invoiceamount)
        invoice_number.append(invoice.invoice_number)

    response_html = '<br>'.join(map(str, invoice_number))
    #resp_html = '<div>'.join(str(Invoice.objects.values('total_amount').aggregate(Sum('total_amount',output_field=FloatField()))))
    
    return HttpResponse(response_html)

def search(request):
    invoice_list = Invoice.objects.all()
    total = Invoice.objects.aggregate(invoice_total=Sum('total_amount',output_field=FloatField()))
    #total[0].invoice_total
    invoice_filter = InvoiceFilter(request.GET, queryset=invoice_list)
    #invoice_total = InvoiceFilter(request.GET, queryset=total)

    return render(request, 'search/invoice_list.html', {'filter': invoice_filter, 'total': total})