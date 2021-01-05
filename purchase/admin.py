from django.contrib import admin
from .models import PurchaseModel, PurchaseStatusModel


class PurchaseModelAdmin(admin.ModelAdmin):
    fields = ('purchaser_name', 'quantity')


class PurchaseStatusModelAdmin(admin.ModelAdmin):
    list_display = ('purchase', 'created_at',)
    fields = ('purchase', 'status', )


admin.site.register(PurchaseModel, PurchaseModelAdmin)
admin.site.register(PurchaseStatusModel, PurchaseStatusModelAdmin)
