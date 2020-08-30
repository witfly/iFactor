from rest_framework import serializers
from factor_app.models import Invoice, InvoiceLineItems

class InvoiceLineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceLineItems
        fields = ('invoice_line_item_id','invoice_id','line_item', 'amount')
        
class InvoiceSerializer(serializers.ModelSerializer):
    line_items = InvoiceLineItemSerializer(many=True)
    class Meta:
        model = Invoice
        fields = ('invoice_id', 'invoice_number', 'load_number', 'bol_number', 'purchase_option', 'processing_stage', 'is_document_ready',
                  'job_number', 'load_lable','track_number', 'pickup_date', 'pickup_address', 'pickup_city', 'pickup_state', 'pickup_zip',
                  'delivery_date', 'delivery_address', 'delivery_city', 'delivery_state', 'delivery_zip', 
                  'total_amount', 'document_path','document_file_name', 'line_items')