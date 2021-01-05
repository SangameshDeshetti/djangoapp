from django.shortcuts import render
from .utils.populate_db import populate_db
from .models import PurchaseModel, PurchaseStatusModel
from django.db.models import Sum
from django.db.models.functions import ExtractMonth, ExtractYear
import json
from datetime import datetime
from django.http import HttpResponse


def home_view(request):
    min_date = datetime(2019, 1, 1, 0, 0)
    min_date = min_date.strftime("%Y-%m-%d")

    max_date = datetime(2020, 3, 31, 0, 0)
    max_date = max_date.strftime("%Y-%m-%d")

    today = datetime.today().strftime('%Y-%m-%d')

    purchase_models_count = PurchaseModel.objects.all().count()
    purchase_status_models_count = PurchaseStatusModel.objects.all().count()

    if not purchase_models_count or not purchase_status_models_count:
        populate_db()

    purchase_status_models = PurchaseStatusModel.objects \
        .annotate(month=ExtractMonth('created_at'), year=ExtractYear('created_at'), ) \
        .values('year', 'month') \
        .annotate(quantity_sum=Sum('purchase__quantity')) \
        .order_by('year', 'month')

    quantity_list = [str(purchase_status_model["quantity_sum"]) for purchase_status_model in purchase_status_models]

    # Need to show only one year data
    if len(quantity_list) > 12:
        quantity_list = quantity_list[:12]

    quantity_list = json.dumps(quantity_list)

    months_list = [str(purchase_status_model["month"]) + "/" + str(purchase_status_model["year"])[2:]
                   for purchase_status_model in purchase_status_models]

    # Need to show only one year data
    if len(months_list) > 12:
        months_list = months_list[:12]

    months_list = json.dumps(months_list)

    return render(request, "home.html", {
        "months_list": months_list,
        "quantity_list": quantity_list,
        "min_date": min_date,
        "max_date": max_date,
        "today": today
    })


def fetch_transactions(request):
    if request.method == "GET":
        start_date = request.GET["start_date"]
        start_date = datetime.strptime(start_date, "%Y-%m-%d")

        end_date = request.GET["end_date"]
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        purchase_status_models = PurchaseStatusModel.objects \
            .filter(created_at__gte=start_date, created_at__lte=end_date) \
            .annotate(month=ExtractMonth('created_at'), year=ExtractYear('created_at'), ) \
            .values('year', 'month') \
            .annotate(quantity_sum=Sum('purchase__quantity')) \
            .order_by('year', 'month')

        quantity_list = json.dumps([str(purchase_status_model["quantity_sum"]) \
                                    for purchase_status_model in purchase_status_models])

        months_list = json.dumps([str(purchase_status_model["month"]) + "/" + str(purchase_status_model["year"])[2:] \
                                  for purchase_status_model in purchase_status_models])
        data = {
            "quantity_list": quantity_list,
            "months_list": months_list
        }
        return HttpResponse(json.dumps(data), content_type='application/json')

    return HttpResponse(status=500)
