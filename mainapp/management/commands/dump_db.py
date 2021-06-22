import pickle

from django.core.management.base import BaseCommand

from authapp.models import ShopUser
from mainapp.models import Product, ProductCategory


def write_to_pickle(data, file_name):
    with open(file_name, 'wb') as infile:
        return pickle.dump(data, infile)


class Command(BaseCommand):
    help = 'Dump data from db'

    def handle(self, *args, **options):
        product_schema = {'name', 'description', 'short_desc'}
        items = []
        for item in ProductCategory.objects.all():
            # print(item.__dict__)
            # print(vars(item))
            items.append({key: val
                          for key, val in vars(item).items()
                          if key in product_schema})
        print(items)

        # items = load_from_json('mainapp/json/products.json')
        # for item in items:
        #     category = ProductCategory.objects.get(name=item['category'])
        #     item['category'] = category
        #     Product.objects.create(**item)
        #
        # # len(Product.objects.filter(category=1))
        # # Product.objects.filter(category=1).count()
        # if not ShopUser.objects.filter(username='django').exists():
        #     ShopUser.objects.create_superuser('django', 'django@gb.local', 'geekbrains')
