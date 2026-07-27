import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Category, Product
import random

class Command(BaseCommand):
    help = "Seed demo categories and products"
    TASTING_SAMPLES = [
        "Deep ruby with purple reflections. Silky texture...",
        "Bright garnet with ripe cherries and plums...",
        "Pale straw yellow with citrus and white flowers...",
        "Intense ruby red with blackberry and vanilla...",
        "Golden amber with dried fruit and honey...",
    ]
    FOOD_SAMPLES = [
        "Grilled ribeye, lamb rack, aged cheeses...",
        "Roasted duck, mushroom risotto, Parmesan...",
        "Seafood, grilled fish, fresh goat cheese...",
        "Hard cheeses, dried meats, dark chocolate...",
        "Spicy dishes, BBQ ribs, blue cheese...",
    ]
    def handle(self, *args, **kwargs):
        # Copy static/img files → media/
        static_img = settings.BASE_DIR / "static" / "img"
        media_cat = settings.MEDIA_ROOT / "categories"
        media_prod = settings.MEDIA_ROOT / "products"
        media_cat.mkdir(parents=True, exist_ok=True)
        media_prod.mkdir(parents=True, exist_ok=True)

        for i in range(1, 5):
            src, dst = static_img / f"cat-{i}.jpg", media_cat / f"cat-{i}.jpg"
            if src.exists() and not dst.exists():
                shutil.copy(src, dst)

        for i in range(1, 9):
            src, dst = static_img / f"product-{i}.jpg", media_prod / f"product-{i}.jpg"
            if src.exists() and not dst.exists():
                shutil.copy(src, dst)

        self.stdout.write("✅ Images copied")

        Product.objects.all().delete()
        Category.objects.all().delete()

        electronics = Category.objects.create(
            name="Electronics", slug="electronics", image="categories/cat-1.jpg"
        )
        clothing = Category.objects.create(
            name="Clothing", slug="clothing", image="categories/cat-2.jpg"
        )
        home = Category.objects.create(
            name="Home & Kitchen", slug="home", image="categories/cat-3.jpg"
        )
        books = Category.objects.create(
            name="Books", slug="books", image="categories/cat-4.jpg"
        )

        # Each product gets the image that visually matches it
        products_data = [
            (
                "Laptop ASUS",
                electronics,
                25000000,
                "Powerful laptop for work/gaming",
                15,
                "products/product-1.jpg",
                "silver",
                "",
            ),
            (
                "iPhone 15",
                electronics,
                45000000,
                "Latest Apple smartphone",
                8,
                "products/product-2.jpg",
                "black",
                "",
            ),
            (
                'Samsung TV 55"',
                electronics,
                32000000,
                "4K Smart TV",
                5,
                "products/product-3.jpg",
                "",
                "",
            ),
            (
                "Wireless Mouse",
                electronics,
                450000,
                "Ergonomic wireless mouse",
                50,
                "products/product-4.jpg",
                "black",
                "",
            ),
            (
                "Men's Jacket",
                clothing,
                1200000,
                "Winter warm jacket",
                30,
                "products/product-5.jpg",
                "black",
                "L",
            ),
            (
                "Women's Dress",
                clothing,
                890000,
                "Summer collection dress",
                25,
                "products/product-6.jpg",
                "red",
                "M",
            ),
            (
                "Running Shoes",
                clothing,
                2100000,
                "Lightweight sports shoes",
                20,
                "products/product-7.jpg",
                "white",
                "42",
            ),
            (
                "Coffee Maker",
                home,
                5600000,
                "Automatic espresso machine",
                12,
                "products/product-8.jpg",
                "",
                "",
            ),
            (
                "Blender",
                home,
                3200000,
                "High-speed kitchen blender",
                18,
                "products/product-1.jpg",
                "",
                "",
            ),
            (
                "Cookware Set",
                home,
                4500000,
                "10-piece non-stick set",
                10,
                "products/product-2.jpg",
                "",
                "",
            ),
            (
                "Python Programming",
                books,
                350000,
                "Learn Python programming",
                40,
                "products/product-3.jpg",
                "",
                "",
            ),
            (
                "Django for Beginners",
                books,
                280000,
                "Build web apps with Django",
                35,
                "products/product-4.jpg",
                "",
                "",
            ),
        ]
        for name, cat, price, desc, stock, img, color, size in products_data:
            Product.objects.create(
                name=name,
                category=cat,
                price=price,
                description=desc,
                stock=stock,
                image=img,
                available=True,
                color=color,
                size=size,
            )
        for product in Product.objects.all():
            product.tasting_notes = random.choice(self.TASTING_SAMPLES)
            product.food_pairing = random.choice(self.FOOD_SAMPLES)
            product.save()
        self.stdout.write(self.style.SUCCESS("✅ 4 categories + 12 products seeded!"))
 
