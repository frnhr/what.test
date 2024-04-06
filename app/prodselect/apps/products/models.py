import uuid
import re

from django.db import models
import faker


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, null=False, blank=False, default="")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    description = models.TextField(max_length=1000, blank=True, null=False, default="")
    stock = models.PositiveIntegerField(default=0, null=False, blank=False)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def generate_fake(cls, n: int) -> list[int]:
        fake = faker.Faker()

        def _fake_price() -> float:
            """
            Generate a random price.
            Using the price_formats to avoid having 90% of prices having the same number of digits.
            """
            return float(
                fake.numerify(
                    fake.random_element(faker.providers.currency.en_US.Provider.price_formats)
                )
                .replace(",", "")
            )

        def _fake_name() -> str:
            """
            Product name, between 1 and 4 random words.

            I can personally confirm that reading generated values is a very fun way to waste time.
            """
            words = re.sub(r"[^\w\s]", "", fake.text(300).lower()).split(" ")
            # ^ only lowercase words, no punctuation
            long_words = list(filter(lambda word: len(word) > 3, words))  # remove "a", "the", etc.
            few_words = long_words[:fake.random_int(min=2, max=6)]
            # capitalize the start of the first word and maybe a few more:
            few_words[0] = few_words[0].title()
            for i in range(1, len(few_words)):
                if fake.boolean(chance_of_getting_true=10):
                    few_words[i] = few_words[i].title()
            # join the words and return
            return " ".join(few_words)

        def _random_stock() -> int:
            """
            Generate a random stock number, with more chances of having a low stock.
            """
            return fake.random_int(min=0, max=10 ** fake.random_int(min=1, max=4))

        ids = []
        for _ in range(n):
            product = cls.objects.create(
                name=_fake_name(),
                price=_fake_price(),
                description=fake.text(fake.random_int(100, 900)),
                stock=_random_stock(),
            )
            ids.append(product.id)
        return ids
