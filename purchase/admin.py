from django.contrib import admin
from .models import PurchaseModel, PurchaseStatusModel


class PurchaseModelAdmin(admin.ModelAdmin):    # For PurchaseModelAdmin show below fields only in details
    fields = ('purchaser_name', 'quantity',)


class PurchaseStatusModelAdmin(admin.ModelAdmin):
    # For PurchaseStatusModelAdmin show below fields only in details
    fields = ('purchase', 'status',)


# Register the Models and Admins configurations
admin.site.register(PurchaseModel, PurchaseModelAdmin)
admin.site.register(PurchaseStatusModel, PurchaseStatusModelAdmin)
