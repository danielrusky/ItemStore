import json

from catalog.models import *

from django.core.management import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        Category.objects.all().delete()
        Product.objects.all().delete()
        Contacts.objects.all().delete()

        with open('./data.json', 'r') as f:
            the_list = json.loads(f.read())

        contacts_for_create = []
        categories_to_fill = []
        products_to_fill = []
        index_for_products = {}
        for item in the_list:
            if item['model'] == 'catalog.category':
                temp = Category(**item['fields'])
                categories_to_fill.append(temp)
                index_for_products |= ({item['pk']: temp})
            elif item['model'] == 'catalog.product':
                products_to_fill.append(Product(name=item['fields']['name'],
                                                description=item['fields']['description'],
                                                image=item['fields']['image'],
                                                price=item['fields']['price'],
                                                date_created=item['fields']['date_created'],
                                                date_modified=item['fields']['date_modified'],
                                                category=index_for_products[item['fields']['category']]))
            elif item['model'] == 'catalog.contacts':
                contacts_for_create.append(Contacts(name=item['fields']['name'],
                                                    phone=item['fields']['phone'],
                                                    message=item['fields']['message'],
                                                    avatar=item['fields']['avatar']))
        Category.objects.bulk_create(categories_to_fill)
        Product.objects.bulk_create(products_to_fill)
        Contacts.objects.bulk_create(contacts_for_create)