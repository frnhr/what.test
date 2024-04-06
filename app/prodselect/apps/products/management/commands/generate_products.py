from django.core.management.base import BaseCommand, CommandError
from prodselect.apps.products.models import Product


class Command(BaseCommand):
    help = "Generates N products with fake (random) data."

    def add_arguments(self, parser):
        parser.add_argument("number_of_products", metavar="N", type=int)

    def handle(self, *args, **options):
        number_of_products = options["number_of_products"]
        generated_ids = Product.generate_fake(number_of_products)
        self.stderr.write(self.style.SUCCESS(f"Generated {len(generated_ids)} products."))
