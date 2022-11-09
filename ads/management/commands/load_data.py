from django.core.management import BaseCommand
from ads.models import Category, Ads
import csv

class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            with open('ads/ads.csv', 'r', encoding='utf-8') as file:
                fieldnames = ['Id', 'name', 'author', 'price', 'description', 'address', 'is_published']
                file_reader = csv.DictReader(file, delimiter=",", fieldnames=fieldnames)
                next(file_reader)


                for i in file_reader:
                    ads = Ads(
                    name = i['name'],
                    author = i['author'],
                    price = i['price'],
                    description= i['description'],
                    address = i['address'],
                    is_published = True if i['is_published'] == 'TRUE' else False
                    )
                    ads.save()

            with open('ads/categories.csv', 'r', encoding='utf-8') as file:
                fieldnames = ['id', 'name']
                file_reader = csv.DictReader(file, delimiter=",", fieldnames=fieldnames)
                next(file_reader)


                for i in file_reader:
                    category = Category(
                    name = i['name'],
                    )
                    category.save()

            print('insert done')
        except:
            print('insert_error')