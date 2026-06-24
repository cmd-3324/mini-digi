# shop/management/commands/seed_products.py
from django.core.management.base import BaseCommand
from shop.models import Category, Product


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        electronics = Category.objects.get_or_create(
            name="Electronics", slug="electronics"
        )[0]
        clothing = Category.objects.get_or_create(name="Clothing", slug="clothing")[0]
        home = Category.objects.get_or_create(name="Home & Kitchen", slug="home")[0]
        books = Category.objects.get_or_create(name="Books", slug="books")[0]

        products = [
            (
                "Laptop ASUS",
                electronics,
                25000000,
                "Powerful laptop for work and gaming",
                15,
            ),
            ("iPhone 15", electronics, 45000000, "Latest Apple smartphone", 8),
            ('Samsung TV 55"', electronics, 32000000, "4K Smart TV", 5),
            ("Wireless Mouse", electronics, 450000, "Ergonomic design", 50),
            ("Men's Jacket", clothing, 1200000, "Winter warm jacket", 30),
            ("Women's Dress", clothing, 890000, "Summer collection", 25),
            ("Running Shoes", clothing, 2100000, "Lightweight sports shoes", 20),
            ("Coffee Maker", home, 5600000, "Automatic espresso machine", 12),
            ("Blender", home, 3200000, "High-speed kitchen blender", 18),
            ("Cookware Set", home, 4500000, "10-piece non-stick set", 10),
            ("Python Book", books, 350000, "Learn Python programming", 40),
            ("Django for Beginners", books, 280000, "Build web apps with Django", 35),
        ]

        for name, cat, price, desc, stock in products:
            Product.objects.create(
                name=name, category=cat, price=price, description=desc, stock=stock
            )

        self.stdout.write(self.style.SUCCESS("✅ 12 demo products created!"))
