from django.contrib import admin

from .models import Invoice, Debtor, Client, NOA, Terms

admin.site.register(Invoice)
admin.site.register(Debtor)
admin.site.register(Client)
admin.site.register(NOA)
admin.site.register(Terms)
