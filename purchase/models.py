from django.db import models
from datetime import datetime
from django.db import connection


class PurchaseModel(models.Model):
    purchaser_name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        super(PurchaseModel, self).save(*args, **kwargs)


class PurchaseStatusModel(models.Model):
    purchase = models.ForeignKey(PurchaseModel)
    status = models.CharField(max_length=25, choices=(
        ("open", "Open"),
        ("verified", "Verified"),
        ("dispatched", "Dispatched"),
        ("delivered", "Delivered")
    ), default="open")
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.id)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = datetime.now()
        super(PurchaseStatusModel, self).save(*args, **kwargs)
