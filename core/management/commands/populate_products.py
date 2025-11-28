from django.core.management.base import BaseCommand
from core.models import Product
from decimal import Decimal


class Command(BaseCommand):
    help = "Заполняет базу данных тестовыми продуктами"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Начинаем создание тестовых продуктов..."))

        products_data = [
            {
                "name": "Поддон европаллет сосна 120x80",
                "condition": "new",
                "price": Decimal("450.00"),
                "length": Decimal("120.00"),
                "width": Decimal("80.00"),
                "wood_type": "Сосна",
                "load_capacity": 1000,
                "in_stock": True,
                "quantity": 150,
            },
            {
                "name": "Поддон усиленный дуб 120x100",
                "condition": "new",
                "price": Decimal("500.00"),
                "length": Decimal("120.00"),
                "width": Decimal("100.00"),
                "wood_type": "Дуб",
                "load_capacity": 1500,
                "in_stock": True,
                "quantity": 80,
            },
            {
                "name": "Поддон б/у сосна 120x80",
                "condition": "used",
                "price": Decimal("250.00"),
                "length": Decimal("120.00"),
                "width": Decimal("80.00"),
                "wood_type": "Сосна",
                "load_capacity": 800,
                "in_stock": True,
                "quantity": 200,
            },
            {
                "name": "Поддон промышленный береза 144x120",
                "condition": "new",
                "price": Decimal("600.00"),
                "length": Decimal("144.00"),
                "width": Decimal("120.00"),
                "wood_type": "Береза",
                "load_capacity": 2000,
                "in_stock": True,
                "quantity": 50,
            },
            {
                "name": "Поддон б/у дуб 120x100",
                "condition": "used",
                "price": Decimal("300.00"),
                "length": Decimal("120.00"),
                "width": Decimal("100.00"),
                "wood_type": "Дуб",
                "load_capacity": 1200,
                "in_stock": True,
                "quantity": 120,
            },
            {
                "name": "Поддон стандарт ель 100x120",
                "condition": "new",
                "price": Decimal("550.00"),
                "length": Decimal("100.00"),
                "width": Decimal("120.00"),
                "wood_type": "Ель",
                "load_capacity": 1100,
                "in_stock": True,
                "quantity": 90,
            },
            {
                "name": "Поддон б/у эконом сосна 100x80",
                "condition": "used",
                "price": Decimal("200.00"),
                "length": Decimal("100.00"),
                "width": Decimal("80.00"),
                "wood_type": "Сосна",
                "load_capacity": 700,
                "in_stock": True,
                "quantity": 180,
            },
            {
                "name": "Поддон премиум лиственница 150x120",
                "condition": "new",
                "price": Decimal("700.00"),
                "length": Decimal("150.00"),
                "width": Decimal("120.00"),
                "wood_type": "Лиственница",
                "load_capacity": 2500,
                "in_stock": True,
                "quantity": 40,
            },
        ]

        created_count = 0
        existing_count = 0

        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                length=product_data["length"],
                width=product_data["width"],
                condition=product_data["condition"],
                wood_type=product_data["wood_type"],
                defaults=product_data,
            )

            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"✓ Создан: {product}"))
            else:
                existing_count += 1
                self.stdout.write(self.style.WARNING(f"→ Уже существует: {product}"))

        self.stdout.write("\n" + "=" * 60)
        self.stdout.write(
            self.style.SUCCESS(f"Создано новых продуктов: {created_count}")
        )
        self.stdout.write(
            self.style.WARNING(f"Пропущено существующих: {existing_count}")
        )
        self.stdout.write(
            self.style.NOTICE(f"Всего продуктов в базе: {Product.objects.count()}")
        )
        self.stdout.write("=" * 60)
        self.stdout.write(self.style.SUCCESS("\n✓ Готово!"))
