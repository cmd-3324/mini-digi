import shutil
import random
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from shop.models import Category, Product, ProductVariant

from django.db import connection
import itertools
class Command(BaseCommand):
    help = "Seed demo categories and products with multiple variants"
    STATIC_PRODUCT_IMAGES = [f"product-{i}.jpg" for i in range(1, 10)]
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
        static_img = settings.BASE_DIR / "static" / "img"
        media_root = settings.MEDIA_ROOT
        media_cat = media_root / "categories"
        media_prod = media_root / "products"
        media_cat.mkdir(parents=True, exist_ok=True)
        media_prod.mkdir(parents=True, exist_ok=True)

        for i in range(1, 5):
            src = static_img / f"cat-{i}.jpg"
            dst = media_cat / f"cat-{i}.jpg"
            if src.exists() and not dst.exists():
                shutil.copy(src, dst)

        

        self.stdout.write("✅ Images copied")

        with connection.cursor() as cursor:
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            cursor.execute("TRUNCATE TABLE reviews_comment")
            cursor.execute("TRUNCATE TABLE shop_product_favorited_by")
            cursor.execute("TRUNCATE TABLE shop_productvariant")
            cursor.execute("TRUNCATE TABLE shop_product")
            cursor.execute("TRUNCATE TABLE shop_category")
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        for old_folder in media_prod.glob("*"):
            if old_folder.is_dir():
                shutil.rmtree(old_folder)
        electronics = Category.objects.create(name="Electronics", slug="electronics", image="categories/cat-1.jpg")
        clothing = Category.objects.create(name="Clothing", slug="clothing", image="categories/cat-2.jpg")
        home = Category.objects.create(name="Home & Kitchen", slug="home", image="categories/cat-3.jpg")
        books = Category.objects.create(name="Books", slug="books", image="categories/cat-4.jpg")

        products_data = [
            {
                "name": "Laptop ASUS",
                "cat": electronics,
                "price": 25000000,
                "desc": "Powerful laptop for work/gaming",
                "stock": 15,
                "rate" : 4,
                "variants": [
                    {"color": "silver", "size": "", "image": "products/product-1.jpg"},
                    {"color": "gray", "size": "", "image": ""},
                    {"color": "gold", "size": "", "image": ""},
                ]
            },
            {
                "name": "iPhone 15",
                "cat": electronics,
                "price": 45000000,
                "desc": "Latest Apple smartphone",
                "stock": 8,
                "rate" : 3,
                "variants": [
                    {"color": "black", "size": "", "image": "products/product-2.jpg"},
                    {"color": "white", "size": "", "image": ""},
                    {"color": "gold", "size": "", "image": ""},
                ]
            },
            {
                "name": "Samsung TV 55\"",
                "cat": electronics,
                "price": 32000000,
                "desc": "4K Smart TV",
                "stock": 5,
                "rate" : 1.5,
                "variants": [
                    {"color": "gray", "size": "", "image": "products/product-3.jpg"},
                    {"color": "black", "size": "", "image": ""},
                ]
            },
            {
                "name": "Wireless Mouse",
                "cat": electronics,
                "price": 450000,
                "desc": "Ergonomic wireless mouse",
                "stock": 50,
                "rate" : 4,
                "variants": [
                    {"color": "black", "size": "", "image": "products/product-4.jpg"},
                    {"color": "white", "size": "", "image": ""},
                    {"color": "red", "size": "", "image": ""},
                ]
            },
            {
                "name": "Men's Jacket",
                "cat": clothing,
                "price": 1200000,
                "desc": "Winter warm jacket",
                "stock": 30,
                "rate" : 4,
                "variants": [
                    {"color": "black", "size": "S", "image": "products/product-5.jpg"},
                    {"color": "black", "size": "M", "image": ""},
                    {"color": "black", "size": "L", "image": ""},
                    {"color": "blue", "size": "M", "image": ""},
                ]
            },
            {
                "name": "Women's Dress",
                "cat": clothing,
                "price": 890000,
                "desc": "Summer collection dress",
                "stock": 25,
                "rate" : 3.5,
                "variants": [
                    {"color": "red", "size": "M", "image": "products/product-6.jpg"},
                    {"color": "blue", "size": "S", "image": ""},
                    {"color": "green", "size": "L", "image": ""},
                ]
            },
            {
                "name": "Running Shoes",
                "cat": clothing,
                "price": 2100000,
                "desc": "Lightweight sports shoes",
                "stock": 20,
                "rate" : 3.5,
                "variants": [
                    {"color": "white", "size": "42", "image": "products/product-7.jpg"},
                    {"color": "black", "size": "42", "image": ""},
                    {"color": "white", "size": "44", "image": ""},
                ]
            },
            {
                "name": "Coffee Maker",
                "cat": home,
                "price": 5600000,
                "desc": "Automatic espresso machine",
                "stock": 12,
                "rate" : 3.5,
                "variants": [
                    {"color": "silver", "size": "", "image": "products/product-8.jpg"},
                    {"color": "black", "size": "", "image": ""},
                ]
            },
            {
                "name": "Blender",
                "cat": home,
                "price": 3200000,
                "desc": "High-speed kitchen blender",
                "stock": 18,
                "rate" : 3.5,
                "variants": [
                    {"color": "white", "size": "", "image": "products/product-1.jpg"},
                    {"color": "black", "size": "", "image": ""},
                ]
            },
            {
                "name": "Cookware Set",
                "cat": home,
                "price": 4500000,
                "desc": "10-piece non-stick set",
                "stock": 10,
                "rate" : 3.5,
                "variants": [
                    {"color": "stainless", "size": "", "image": "products/product-2.jpg"},
                ]
            },
            {
                "name": "Python Programming",
                "cat": books,
                "price": 350000,
                "desc": "Learn Python programming",
                "stock": 40,
                "rate" : 3.5,
                "variants": [
                    {"color": "", "size": "", "image": "products/product-3.jpg"},
                ]
            },
            {
                "name": "Django for Beginners",
                "cat": books,
                "price": 280000,
                "desc": "Build web apps with Django",
                "stock": 35,
                "rate" : 3.5,
                "variants": [
                    {"color": "", "size": "", "image": "products/product-4.jpg"},
                ]
            },
        ]

        image_cycle = itertools.cycle(self.STATIC_PRODUCT_IMAGES)

        for p_data in products_data:
            product = Product.objects.create(
                name=p_data["name"],
                category=p_data["cat"],
                price=p_data["price"],
                description=p_data["desc"],
                stock=p_data["stock"],
                available=True,
            )

            product_folder = media_prod / product.slug
            product_folder.mkdir(parents=True, exist_ok=True)

            for i, v_data in enumerate(p_data["variants"]):
                img_name = v_data["image"].rsplit("/", 1)[-1] if v_data["image"] else next(image_cycle)
                src_file = static_img / img_name
                new_name = "default.jpg" if i == 0 else f"variant_{i+1}.jpg"
                db_image_path = ""
                if src_file.exists():
                    shutil.copy(src_file, product_folder / new_name)
                    db_image_path = f"products/{product.slug}/{new_name}"

                ProductVariant.objects.create(
                    product=product,
                    is_default=(i == 0),
                    is_active=True,
                    stock=p_data["stock"],
                    color=v_data["color"],
                    size=v_data["size"],
                    image=db_image_path,
                    price_override=None,
                )

        for product in Product.objects.all():
            product.tasting_notes = random.choice(self.TASTING_SAMPLES)
            product.food_pairing = random.choice(self.FOOD_SAMPLES)
            product.save()

        self.stdout.write(self.style.SUCCESS("✅ 4 categories + products with multiple variants seeded!"))