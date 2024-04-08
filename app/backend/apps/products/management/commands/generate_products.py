from django.core.management import CommandParser
from django.core.management.base import BaseCommand

from backend.apps.products.models import Product


class Command(BaseCommand):
    help = "Generates N products with fake (random) data."

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("number_of_products", metavar="N", type=int)

    def handle(self, *_args, **options) -> None:
        number_of_products = options["number_of_products"]
        generated_ids = Product.generate_fake(number_of_products)
        self.stderr.write(
            self.style.SUCCESS(f"Generated {len(generated_ids)} products."),
        )
