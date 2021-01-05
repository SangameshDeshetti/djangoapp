from datetime import datetime
import random
from ..models import PurchaseModel, PurchaseStatusModel
from random import randrange
from datetime import timedelta
from dateutil import tz
from django.db.models import Count, Sum

# List of 10 random names
RANDOM_NAMES_LIST = ["Liam", "Evelyn", "James", "Emma", "Oliver", "Ava", "William", "Sophia", "Ethan", "Isabella"]

# Choices for status field in PurchaseStatusModel
PURCHASE_STATUS_CHOICES = (
    ("open", "Open"),
    ("verified", "Verified"),
    ("dispatched", "Dispatched"),
    ("delivered", "Delivered")
)

# Range for quantity field for PurchaseModel
QUANTITY_LIST = range(1, 11)

# Maximum number of entries
SIZE = 5000

# Targeted average in problem statement
TARGET_AVG = 7

# This dictionary is used to restrict each user's entries to 5000 / 10 = 500 entries
NAME_OCCURRENCE_COUNT_DICT = {}


def populate_db():
    # Initialize counts to 0
    global NAME_OCCURRENCE_COUNT_DICT
    NAME_OCCURRENCE_COUNT_DICT = {name: 0 for name in RANDOM_NAMES_LIST}

    # Populate PurchaseModel table
    populate_purchase_models()

    # Populate PurchaseStatusModel table
    populate_purchase_status_models()


def populate_purchase_models():
    size = SIZE
    while size > 0:
        # While 5000 inserts are not yet done
        rand_num = random.choice(QUANTITY_LIST)
        num_inserts = process_data(rand_num, size)

        # Update size
        size = size - num_inserts

    # ToDo:
    """
         The final insert(s) for each user:
         We need to make 10 final inserts to make sure no two users average is same
    """


def process_data(rand_num, size):
    if rand_num == TARGET_AVG and size >= 1:
        """
            If random number is TARGET_AVG itself, 
            We need to make only one insert
            (to keep average as TARGET_AVG at any given time)
        """
        num_inserts = 1
        rand_name = get_random_name()
        insert_to_db(rand_name, rand_num)
        return num_inserts
    else:
        if 2 * TARGET_AVG - rand_num in QUANTITY_LIST and size >= 2:
            """
                If random number can couple with another number 
                in the QUANTITY_LIST, such that the two average 
                out to TARGET_AVG, then we make two inserts 
                (to keep average as TARGET_AVG at any given time)
                Catch: (x + y) / 2 = 7
            """
            num_inserts = 2

            rand_name1 = get_random_name()
            insert_to_db(rand_name1, rand_num)

            rand_name2 = get_random_name()
            insert_to_db(rand_name2, 2 * TARGET_AVG - rand_num)

            return num_inserts
        else:
            """
                In the worst case, we make 3 inserts
                so that the average can be maintained at TARGET_AVG
                Catch: (x + y + z) / 3 = 7
            """
            if size >= 3:
                num_inserts = 3
                rand_num2 = 0
                rand_num3 = 0

                new_target = 3 * TARGET_AVG - rand_num

                for i in QUANTITY_LIST:
                    """
                        Get two random numbers in the range QUANTITY_LIST
                        Such that (x + y + z) / 3 = 7
                    """
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
    """
        This method gets a random name from the RANDOM_NAMES_LIST
        and ensures that any user has utmost SIZE / no. of users inserts
        i.e. 5000 / 10 = utmost 500 inserts
    """
    while True:
        rand_name = random.choice(RANDOM_NAMES_LIST)

        if NAME_OCCURRENCE_COUNT_DICT[rand_name] >= (SIZE // len(RANDOM_NAMES_LIST)):
            continue
        else:
            NAME_OCCURRENCE_COUNT_DICT[rand_name] += 1
            return rand_name


def insert_to_db(name, quantity):
    """
        Insert a PurchaseModel into DB
    """
    purchase_model = PurchaseModel()
    purchase_model.purchaser_name = name
    purchase_model.quantity = quantity
    purchase_model.save()


def populate_purchase_status_models():
    # For time zone
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('Asia/Kolkata')

    # First date
    d1_utc = datetime.strptime('01/01/2019 17:00', '%d/%m/%Y %H:%M')
    d1_utc = d1_utc.replace(tzinfo=from_zone)
    d1 = d1_utc.astimezone(from_zone)

    # Second date
    d2_utc = datetime.strptime('31/03/2020 22:00', '%d/%m/%Y %H:%M')
    d2_utc = d2_utc.replace(tzinfo=to_zone)
    d2 = d2_utc.astimezone(to_zone)

    # Fetch all PurchaseModels
    purchase_models = PurchaseModel.objects.all()

    for purchase_model in purchase_models:
        """
            For each PurchaseModel create
            utmost 3 PurchaseStatusModels
            with random status
        """

        # Fetch 3 out of 4 choices of PurchaseStatusModel
        purchase_status_choices = []
        for i in range(random.choice(range(3))):
            """
                3 is a constant given in problem statement
                (at most 3 out of 4 choices)
                Hence this loop will NOT make the complexity O(n^2)
            """
            purchase_status_choices.append(random.choice(PURCHASE_STATUS_CHOICES))

        for choice in purchase_status_choices:
            # Fetch a random date
            date = generate_random_date(d1, d2)

            # create a PurchaseStatusModel for the PurchaseModel
            purchase_status_model = PurchaseStatusModel()
            purchase_status_model.purchase = purchase_model
            purchase_status_model.status = choice[0]
            purchase_status_model.save()

            # Update the created_at to the random date in given date range
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
