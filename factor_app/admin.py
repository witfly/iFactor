from django.contrib import admin

from .models import Invoice, Debtor, Client, NOA, Terms, InvoiceLineItems

admin.site.register(Invoice)
admin.site.register(Debtor)
admin.site.register(Client)
admin.site.register(NOA)
admin.site.register(Terms)
admin.site.register(InvoiceLineItems)
