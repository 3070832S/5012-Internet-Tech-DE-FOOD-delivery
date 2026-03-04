"""创建示例餐厅与菜品：python manage.py seed_restaurants"""
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
                'description': '美式汉堡与快餐',
                'min_order': Decimal('15'),
                'delivery_fee': Decimal('2.99'),
                'estimate_minutes_min': 25,
                'estimate_minutes_max': 35,
                'rating': Decimal('4.8'),
                'tags': '汉堡, 快餐, 美式',
                'dishes': [
                    ('Classic Cheeseburger', '经典芝士堡', Decimal('12.99')),
                    ('Double Bacon Burger', '双层培根堡', Decimal('15.99')),
                    ('Chicken Wings (6pc)', '鸡翅 6只', Decimal('8.99')),
                ],
            },
            {
                'name': 'Sushi Place',
                'slug': 'sushi-place',
                'description': '日式寿司',
                'min_order': Decimal('20'),
                'delivery_fee': Decimal('3.99'),
                'estimate_minutes_min': 30,
                'estimate_minutes_max': 45,
                'rating': Decimal('4.9'),
                'tags': '日式, 寿司, 海鲜',
                'dishes': [
                    ('Sushi Roll Set', '寿司卷套餐', Decimal('24.99')),
                    ('Salmon Nigiri', '三文鱼握寿司', Decimal('12.99')),
                    ('Miso Soup', '味噌汤', Decimal('3.99')),
                ],
            },
            {
                'name': 'Pizza King',
                'slug': 'pizza-king',
                'description': '意式披萨',
                'min_order': Decimal('12'),
                'delivery_fee': Decimal('2.49'),
                'estimate_minutes_min': 20,
                'estimate_minutes_max': 30,
                'rating': Decimal('4.7'),
                'tags': '披萨, 意式',
                'dishes': [
                    ('Margherita Pizza', '玛格丽特披萨', Decimal('18.99')),
                    ('Pepperoni Pizza', '辣肠披萨', Decimal('19.99')),
                    ('Garlic Bread', '蒜香面包', Decimal('5.99')),
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
