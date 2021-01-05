from django.shortcuts import render
from .utils.populate_db import populate_db
from .models import PurchaseModel, PurchaseStatusModel
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
import json
from datetime import datetime
from django.http import HttpResponse


def home_view(request):
    # Given minimum date in problem statement is January 1st, 2019
    min_date = datetime(2019, 1, 1, 0, 0)
    min_date = min_date.strftime("%Y-%m-%d")

    # Given maximum date in problem statement is March 31st, 2020
    max_date = datetime(2020, 3, 31, 0, 0)
    max_date = max_date.strftime("%Y-%m-%d")

    # get how many objects are present in DB tables
    purchase_models_count = PurchaseModel.objects.all().count()
    purchase_status_models_count = PurchaseStatusModel.objects.all().count()

    if not purchase_models_count or not purchase_status_models_count:
        # if no entries in DB, populate DB
        populate_db()

    # get quantity list and months list to show in UI
    quantity_list, months_list = fetch_quantity_month_list()

    return render(request, "home.html", {
        "months_list": months_list,
        "quantity_list": quantity_list,
        "min_date": min_date,
        "max_date": max_date,
    })


def fetch_transactions(request):
    if request.method == "GET":
        start_date = request.GET["start_date"]
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

        end_date = request.GET["end_date"]
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        quantity_list, months_list = fetch_quantity_month_list(start_date, end_date)

        data = {
            "quantity_list": quantity_list,
            "months_list": months_list
        }
        return HttpResponse(json.dumps(data), content_type='application/json')

    return HttpResponse(status=500)


def fetch_quantity_month_list(start_date=None, end_date=None):
    if not start_date and not end_date:
        """
            Below query fetches PurchaseStatusModel objects
            Based on month and year and gives us total quantity
            in those intervals as well
        """
        purchase_status_models = PurchaseStatusModel.objects \
            .annotate(month=ExtractMonth('created_at'), year=ExtractYear('created_at'), ) \
            .values('year', 'month') \
            .annotate(quantity_sum=Sum('purchase__quantity')) \
            .order_by('year', 'month')

    else:
        """
            Below query fetches PurchaseStatusModel objects
            Based on month and year and gives us total quantity 
            in those intervals as well
        """
        purchase_status_models = PurchaseStatusModel.objects \
            .filter(created_at__gte=start_date, created_at__lte=end_date) \
            .annotate(month=ExtractMonth('created_at'), year=ExtractYear('created_at'), ) \
            .values('year', 'month') \
            .annotate(quantity_sum=Sum('purchase__quantity')) \
            .order_by('year', 'month')

    # List of quantities based on month
    quantity_list = [str(purchase_status_model["quantity_sum"]) for purchase_status_model in purchase_status_models]

    # Need to show only one year data
    if len(quantity_list) > 12:
        quantity_list = quantity_list[:12]

    quantity_list = json.dumps(quantity_list)

    # get months list; Format: MM/YY eg: 1/19, 12/20
    months_list = [str(purchase_status_model["month"]) + "/" + str(purchase_status_model["year"])[2:]
                   for purchase_status_model in purchase_status_models]

    # Need to show only one year data
    if len(months_list) > 12:
        months_list = months_list[:12]

    months_list = json.dumps(months_list)

    return quantity_list, months_list
