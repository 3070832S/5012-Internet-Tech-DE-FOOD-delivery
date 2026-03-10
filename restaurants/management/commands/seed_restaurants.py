"""Create sample restaurants and dishes. Usage: python manage.py seed_restaurants"""
from decimal import Decimal
from django.core.management.base import BaseCommand
from restaurants.models import Restaurant, Dish


class Command(BaseCommand):
    help = 'Create sample restaurants and dishes'

    def handle(self, *args, **options):
        data = [
            {
                'name': 'Burger House',
                'slug': 'burger-house',
                'description': 'American burgers and fast food',
                'min_order': Decimal('15'),
                'delivery_fee': Decimal('2.99'),
                'estimate_minutes_min': 25,
                'estimate_minutes_max': 35,
                'rating': Decimal('4.8'),
                'tags': 'Burgers, Fast food, American',
                'dishes': [
                    ('Classic Cheeseburger', 'Classic cheeseburger', Decimal('12.99')),
                    ('Double Bacon Burger', 'Double bacon burger', Decimal('15.99')),
                    ('Chicken Wings (6pc)', 'Chicken wings 6pc', Decimal('8.99')),
                ],
            },
            {
                'name': 'Sushi Place',
                'slug': 'sushi-place',
                'description': 'Japanese sushi',
                'min_order': Decimal('20'),
                'delivery_fee': Decimal('3.99'),
                'estimate_minutes_min': 30,
                'estimate_minutes_max': 45,
                'rating': Decimal('4.9'),
                'tags': 'Japanese, Sushi, Seafood',
                'dishes': [
                    ('Sushi Roll Set', 'Sushi roll set', Decimal('24.99')),
                    ('Salmon Nigiri', 'Salmon nigiri', Decimal('12.99')),
                    ('Miso Soup', 'Miso soup', Decimal('3.99')),
                ],
            },
            {
                'name': 'Pizza King',
                'slug': 'pizza-king',
                'description': 'Italian pizza',
                'min_order': Decimal('12'),
                'delivery_fee': Decimal('2.49'),
                'estimate_minutes_min': 20,
                'estimate_minutes_max': 30,
                'rating': Decimal('4.7'),
                'tags': 'Pizza, Italian',
                'dishes': [
                    ('Margherita Pizza', 'Margherita pizza', Decimal('18.99')),
                    ('Pepperoni Pizza', 'Pepperoni pizza', Decimal('19.99')),
                    ('Garlic Bread', 'Garlic bread', Decimal('5.99')),
                ],
            },
        ]
        for r_data in data:
            dishes_data = r_data.pop('dishes')
            r, created = Restaurant.objects.get_or_create(
                slug=r_data['slug'],
                defaults=r_data
            )
            for i, (name, desc, price) in enumerate(dishes_data):
                Dish.objects.get_or_create(
                    restaurant=r,
                    name=name,
                    defaults={'description': desc, 'price': price, 'sort_order': i}
                )
            self.stdout.write(self.style.SUCCESS(f'Restaurant: {r.name}'))
        self.stdout.write(self.style.SUCCESS('Done.'))
