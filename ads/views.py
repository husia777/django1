from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView, ListView, CreateView, UpdateView, DeleteView
from ads.models import Ads, Category, Users, Locations
from django.views.decorators.csrf import csrf_exempt
import json
from app import settings
from django.db.models.functions import Concat



class Index(View):
    def get(self, request):
        return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsView(ListView):
    model = Ads

    def get(self, request, *args, **kwargs):
        ad_list = Ads.objects.all()
        ad_list = ad_list.select_related('category', 'author').order_by('-price')

        paginator = Paginator(ad_list, settings.TOTAL_ON_PAGE)
        page_number = request.GET.get('page')
        page_object = paginator.get_page(page_number)

        list_data = []
        for dt in page_object:
            list_data.append({
                'Id': dt.id,
                'name': dt.name,
                'author_id': dt.author_id,
                'author': dt.author.first_name,
                'price': dt.price,
                'description': dt.description,
                'is_published': dt.is_published,
                'logo': dt.logo.url if dt.logo else None,
                'category': dt.category.name
            })
            response = {
                'items': list_data,
                'total': paginator.count,
                'num_page': paginator.num_pages
            }

        return JsonResponse(response, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdsDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
            return JsonResponse({
                'Id': ad.id,
                'name': ad.name,
                'author_id': ad.author.id,
                'author': ad.author.first_name,
                'price': ad.price,
                'description': ad.description,
                'is_published': ad.is_published,
                'logo': ad.logo.url,
                'category': ad.category.name
                })
        except:
            return JsonResponse({'error': 'not found'}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class AdsCreateView(CreateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'address', 'is_published']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        ad = Ads.objects.create(
            name=data['name'],
            author=data['author'],
            price=data['price'],
            description=data['description'],
            address=data['address'],
            is_published=data['is_published'],
            logo=data['logo'],
            category=['category']
        )

        return JsonResponse({'res': 'ok'}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class AdsUpdateView(UpdateView):
    model = Ads
    fields = ['name', 'price', 'description', 'address', 'is_published']
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data['name']
        self.object.author = data['author']
        self.object.price = data['price']
        self.object.description = data['description']
        self.object.address = data['address']
        self.object.is_published = data['is_published']
        self.object.logo = data['logo'],
        self.object.category = data['category']

        self.object.save()

        return JsonResponse({
            'name': self.object.name,
            'author': self.object.author,
            'price': self.object.price,
            'description': self.object.description,
            'address': self.object.address,
            'is_published': self.object.is_published,
            'logo': self.object.logo,
            'category': self.object.category
            }, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class AdsDeleteView(DeleteView):
    model = Ads
    success_url = 'ad'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status':'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsAddImage(UpdateView):
    model = Ads
    fields = ['name', 'author', 'price', 'description', 'address', 'is_published', 'logo', 'category']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.logo = request.FILES["logo"]
        self.object.save()
        return JsonResponse({
            'name': self.object.name,
            'author': self.object.author,
            'price': self.object.price,
            'description': self.object.description,
            'address': self.object.address,
            'is_published': self.object.is_published,
            'logo': self.object.logo.url if self.object.logo else None,
            'category': self.object.category
            })


@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(ListView):
    model = Category

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.order_by('name')
        list_data = []
        for dt in self.object_list:
            list_data.append({
                'id': dt.id,
                'name': dt.name
            })
        return JsonResponse(list_data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            caregory = self.get_object()
            return JsonResponse({
                'Id': caregory.id,
                'name': caregory.name})
        except:
            return JsonResponse({'error': 'not found'}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = ['name']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        category = Category.objects.create(
            name=data['name'],
        )
        category.save()
        return JsonResponse({'res': 'ok'}, status=200)



@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']
    def post(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data['name']
        self.object.save()

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = 'cat'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status': 'ok'}, status=200)





@method_decorator(csrf_exempt, name='dispatch')
class UsersView(ListView):
    model = Users

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        self.object_list = self.object_list.prefetch_related('location').order_by('username').all()


        list_data = []
        for dt in self.object_list:
            list_data.append({
                'Id': dt.id,
                'first_name': dt.first_name,
                'last_name': dt.last_name,
                'username': dt.username,
                'password': dt.password,
                'role': dt.role,
                'age': dt.age,
                'location': list(map(str, dt.location.all())),
            })

        return JsonResponse(list_data, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UsersDetailView(DetailView):
    model = Users

    def get(self, request, *args, **kwargs):
        #try:
            ad = self.get_object()
            paginator = Paginator(ad, settings.TOTAL_ON_PAGE)
            page_number = request.GET.get('page')
            page_object = paginator.get_page(page_number)
            list_data = []
            list_data.append({
                'Id': ad.id,
                'first_name': ad.first_name,
                'last_name': ad.last_name,
                'username': ad.username,
                'password': ad.password,
                'role': ad.role,
                'age': ad.age,
                'location': ad.location.name,
                'total_ads': ad.total_ads
            })

            response = {
                'items': list_data,
                'total': paginator.count,
                'num_page': paginator.num_pages
            }

            return JsonResponse(response, safe=False)

        #except:
            return JsonResponse({'error': 'not found'}, status=404)


@method_decorator(csrf_exempt, name='dispatch')
class UsersCreateView(CreateView):
    model = Users
    fields = ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'location']

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        ad = Users.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            password=data['password'],
            role=data['role'],
            age=data['age'],
        )
        for location in data['location']:
            user_loc, created = Locations.objects.get_or_create(
                name=location)
            ad.location.add(user_loc)
        ad.save()
        return JsonResponse({'res': 'ok'}, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class UsersUpdateView(UpdateView):
    model = Users
    fields = ['first_name', 'last_name', 'username', 'password', 'role', 'age', 'location']
    def post(self, request, *args, **kwargs):
        user_data = json.loads(request.body)

        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.first_name = data['first_name']
        self.object.last_name = data['last_name']
        self.object.username = data['username']
        self.object.password = data['password']
        self.object.role = data['role']
        self.object.age = data['age']
        self.object.location = self.object.name.get_or_create(data['location']),
        self.object.save()

        return JsonResponse({
            'first_name': self.object.name,
            'last_name': self.object.author,
            'username': self.object.price,
            'password': self.object.description,
            'role': self.object.address,
            'age': self.object.is_published,
            'location': self.object.location,

        }, status=200)

@method_decorator(csrf_exempt, name='dispatch')
class UsersDeleteView(DeleteView):
    model = Users
    success_url = 'user'

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return JsonResponse({'status':'ok'}, status=200)



