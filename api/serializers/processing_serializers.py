from rest_framework import serializers
from factor_app.models import Processing, Client, Terms, Invoice, InvoiceLineItems


class ProcessingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Processing
        fields = ('__all__')
        
        
class ProcessingInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ('invoice_id', 'invoice_number', 'load_number', 'total_amount', 'purchase_option', 'date_due')


class ProcessingClientInvoiceSerializer(serializers.ModelSerializer):
    invoices = ProcessingInvoiceSerializer(source='invoice_set', many=True)
    class Meta:
        model = Client
        fields = ('client_id', 'client_name', 'credit_limit','invoices')
        
class ProcessingTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = Terms
        fields = ('terms_id', 'transaction_fee_rate_type', 'advance_percentage', 'security_percentage', 'invoice_fee', 'flat_rate', 
                 'express_processing_fee', 'priority_processing_fee', 'standard_processing_fee')
        
class ProcessingInvoiceLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLineItems
        fields = ('invoice_id','line_item', 'amount')

class ProcessingInvoiceDetailSerializer(serializers.ModelSerializer):
    line_items = ProcessingInvoiceLineItemSerializer(many=True)
    term = ProcessingTermSerializer(source='terms')
    class Meta:
        model = Invoice
        fields = ('invoice_id', 'invoice_number', 'load_number', 'bol_number', 'purchase_option', 'processing_stage', 'is_document_ready',
                  'job_number', 'load_lable','track_number', 'pickup_date', 'pickup_address', 'pickup_city', 'pickup_state', 'pickup_zip',
                  'delivery_date', 'delivery_address', 'delivery_city', 'delivery_state', 'delivery_zip', 
                  'total_amount', 'document_path','document_file_name', 'line_items', 'term')

    