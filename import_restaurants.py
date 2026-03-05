import csv
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "food_delivery_project.settings")
django.setup()

from restaurants.models import Restaurant

with open("restaurants.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        Restaurant.objects.create(
            name=row["name"],
            slug=row["slug"],
            description=row["description"],
            min_order=row["min_order"],
            delivery_fee=row["delivery_fee"],
            rating=row["rating"],
        )

print("Restaurants imported successfully!")