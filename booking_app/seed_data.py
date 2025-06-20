from .models import FitnessClass
from django.utils.timezone import make_aware
from datetime import datetime, timedelta
import pytz

def run():
    ist = pytz.timezone('Asia/Kolkata')
    now = datetime.now(ist)

    FitnessClass.objects.all().delete()
    classes = [
        ('Yoga', 'Alice', now + timedelta(days=1)),
        ('Zumba', 'Bob', now + timedelta(days=2)),
        ('HIIT', 'Charlie', now + timedelta(days=3)),
    ]
    for name, instructor, dt in classes:
        FitnessClass.objects.create(
            name=name,
            instructor=instructor,
            datetime=dt,
            available_slots=10
        )