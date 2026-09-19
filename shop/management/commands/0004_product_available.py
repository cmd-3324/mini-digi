from django.db import migrations, models


class Migration(migrations.Migration):
    """
    Adds the `available` BooleanField to Product.
    This was missing and caused a FieldError crash on product_detail view.
    Run AFTER your existing 0003_category_image migration.
    """

    dependencies = [
        ("shop", "0003_category_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="available",
            field=models.BooleanField(default=True),
        ),
    ]
