from django.db import models
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

    @classmethod
    def truncate(cls):
        """
            USE WITH CAUTION!!
        """
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {} CASCADE'.format(cls._meta.db_table))


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
        super(PurchaseStatusModel, self).save(*args, **kwargs)

    @classmethod
    def truncate(cls):
        """
            USE WITH CAUTION!!
        """
        with connection.cursor() as cursor:
            cursor.execute('TRUNCATE TABLE {} CASCADE'.format(cls._meta.db_table))
