from datetime import datetime
import random
from ..models import PurchaseModel, PurchaseStatusModel
from random import randrange
from datetime import timedelta
from dateutil import tz
from django.db.models import Count, Sum

RANDOM_NAMES_LIST = ["Liam", "Evelyn", "James", "Emma", "Oliver", "Ava", "William", "Sophia", "Ethan", "Isabella"]
PURCHASE_STATUS_CHOICES = (
    ("open", "Open"),
    ("verified", "Verified"),
    ("dispatched", "Dispatched"),
    ("delivered", "Delivered")
)
QUANTITY_LIST = range(1, 11)
SIZE = 5000
TARGET_AVG = 7
NAME_OCCURRENCE_COUNT_DICT = {}


def populate_db():
    global NAME_OCCURRENCE_COUNT_DICT
    NAME_OCCURRENCE_COUNT_DICT = {name: 0 for name in RANDOM_NAMES_LIST}
    populate_purchase_models()
    populate_purchase_status_models()


def populate_purchase_models():
    size = SIZE
    while size > 0:
        rand_num = random.choice(QUANTITY_LIST)
        num_inserts = process_data(rand_num, size)
        size = size - num_inserts

    # The final insert:
    # purchase_model_stats = PurchaseModel.objects.values('purchaser_name') \
    #     .annotate(quantity_sum=Sum('quantity'))
    #
    # new_list = sorted(list(purchase_model_stats), key=lambda k: k['quantity_sum'])


def process_data(rand_num, size):
    if rand_num == TARGET_AVG and size >= 1:
        num_inserts = 1
        rand_name = get_random_name()
        insert_to_db(rand_name, rand_num)
        return num_inserts
    else:
        if 2 * TARGET_AVG - rand_num in QUANTITY_LIST and size >= 2:
            num_inserts = 2

            rand_name1 = get_random_name()
            insert_to_db(rand_name1, rand_num)

            rand_name2 = get_random_name()
            insert_to_db(rand_name2, 2 * TARGET_AVG - rand_num)

            return num_inserts
        else:
            if size >= 3:
                num_inserts = 3
                rand_num2 = 0
                rand_num3 = 0

                new_target = 3 * TARGET_AVG - rand_num

                for i in QUANTITY_LIST:
                    if new_target - i in QUANTITY_LIST:
                        rand_num2 = i
                        rand_num3 = new_target - i
                        break

                rand_name1 = get_random_name()
                insert_to_db(rand_name1, rand_num)

                rand_name2 = get_random_name()
                insert_to_db(rand_name2, rand_num2)

                rand_name3 = get_random_name()
                insert_to_db(rand_name3, rand_num3)

                return num_inserts
    return 0


def get_random_name():
    while True:
        rand_name = random.choice(RANDOM_NAMES_LIST)

        if NAME_OCCURRENCE_COUNT_DICT[rand_name] >= (SIZE // len(RANDOM_NAMES_LIST)):
            continue
        else:
            NAME_OCCURRENCE_COUNT_DICT[rand_name] += 1
            return rand_name


def insert_to_db(name, quantity):
    purchase_model = PurchaseModel()
    purchase_model.purchaser_name = name
    purchase_model.quantity = quantity
    purchase_model.save()


def populate_purchase_status_models():
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Asia/Kolkata')

    d1_utc = datetime.strptime('01/01/2019 17:00', '%d/%m/%Y %H:%M')
    d1_utc = d1_utc.replace(tzinfo=from_zone)
    d1 = d1_utc.astimezone(from_zone)

    d2_utc = datetime.strptime('31/03/2020 22:00', '%d/%m/%Y %H:%M')
    d2_utc = d2_utc.replace(tzinfo=to_zone)
    d2 = d2_utc.astimezone(to_zone)

    purchase_models = PurchaseModel.objects.all()

    for purchase_model in purchase_models:
        purchase_status_choices = []
        for i in range(random.choice(range(3))):
            """
                3 is a constant given in problem statement
                Hence this loop will NOT make the complexity O(n^2)
            """
            purchase_status_choices.append(random.choice(PURCHASE_STATUS_CHOICES))

        for choice in purchase_status_choices:
            date = generate_random_date(d1, d2)

            purchase_status_model = PurchaseStatusModel()
            purchase_status_model.purchase = purchase_model
            purchase_status_model.status = choice[0]
            purchase_status_model.save()
            PurchaseStatusModel.objects.filter(id=purchase_status_model.id).update(created_at=date)


def generate_random_date(start, end):
    """
        This function will return a random datetime
        between two datetime objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
