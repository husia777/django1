from django.core.management import BaseCommand
from ads.models import Category, Ads, Locations, Users
import csv


class Command(BaseCommand):

    def handle(self, *args, **options):
        #try:
            with open('ads/location.csv', 'r', encoding='utf-8') as file:
                fieldnames = ['id', 'name', 'lat', 'lng']
                file_reader = csv.DictReader(file, delimiter=",", fieldnames=fieldnames)
                next(file_reader)

                for i in file_reader:
                    location = Locations(
                        name=i['name'],
                        lat=i['lat'],
                        lng=i['lng'],
                    )
                    location.save()



            with open('ads/user.csv', 'r', encoding='utf-8') as file:
                fieldnames = ['id','first_name','last_name','username','password','role','age','location_id']
                file_reader = csv.DictReader(file, delimiter=",", fieldnames=fieldnames)
                next(file_reader)

                for i in file_reader:
                    user = Users(
                        first_name=i['first_name'],
                        last_name=i['last_name'],
                        username=i['username'],
                        password=i['password'],
                        role=i['role'],
                        age=i['age'],
                        )
                    user.save()

            with open('ads/categories.csv', 'r', encoding='utf-8') as file:
                fieldnames = ['id', 'name']
                file_reader = csv.DictReader(file, delimiter=",", fieldnames=fieldnames)
                next(file_reader)

                for i in file_reader:
                    category = Category(
                        name=i['name'],
                    )
                    category.save()

            with open('ads/ads.csv', 'r', encoding='utf-8') as file:
                fieldnames = ['Id', 'name', 'author_id', 'price', 'description', 'is_published', 'image',   'category_id']
                file_reader = csv.DictReader(file, delimiter=",", fieldnames=fieldnames)
                next(file_reader)

                for i in file_reader:
                    ads = Ads(
                        name=i['name'],
                        author_id=int(i['author_id']),
                        price=i['price'],
                        description=i['description'],
                        is_published=True if i['is_published'] == 'TRUE' else False,
                        logo = i['image'],
                        category_id=int(i['category_id'])
                    )
                    ads.save()







    print('insert done')
        #except:
            #print('insert_error')
