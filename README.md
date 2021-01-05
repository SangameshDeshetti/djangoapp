Assignment – Backend Developer (Problem Statement)

NOTE: Python 3 has been used in the implementation

Consider the below Django Models:

    Class PurchaseModel(models.Model):    
        purchaser_name = models.CharField(...)
        quantity = models.IntegerField(...)

    Class PurchaseStatusModel(model.Model):
        purchase = models.ForeignKey(PurchaseModel)
        status = models.CharField(
                    max_length=25,
                    choices=(
                    (‘open’, ‘Open’),
                    (‘verified, ‘Verified’),
                    (‘dispatched’, ‘Dispatched’),
                    (‘delivered, ‘Delivered’),
                )
        created_at = models.DateTimeField(auto_now_add=True)


Use Django 1.11 and Postgresql 9.6 to make a project with single app called
“purchase” with the above two models. Write a script to populate the two
models with:
1. 5000 PurchaseModel entries with purchaser_name randomly chosen
from 10 random names. Quantity can be any random number between 1
and 10 such that:
a. Average quantity of all PurchaseModel entries is 7
b. No two purchasers will have the same average quantity
2. Each PurchaseModel object should have at most 4 out of the 5 statuses
from the available status choices.

a. The created dates for the PurchaseStatusModel objects must be
randomly distributed between 01 st Jan 2019 05 pm IST and 31 st
March 2020 10 pm ISTCreate a dashboard using echarts (https://echarts.apache.org/) showing a bar
chart of the PurchaseModel with a Date Filter.

• On Page load the bar chard should show 1year data with monthly
frequency.

• On changing date filter, trigger an ajax request and update the graph.
Criteria for filtering PurchaseModel with dates:

• If the latest status of PurchaseModel is dispatched, filter by created_at
date of dispatched status

• If the latest status of PurchaseModel is delivered and the PurchaseModel
also has a dispatched status, filter by created_at date of dispatched status

• If the latest status of PurchaseModel is delivered and the PurchaseModel
does not have a dispatched status, filter by created_at date of delivered
status


P.S. Queries should be written in a way that the time to load the graph is as less
as possible (E.g. minimum number of db calls)
