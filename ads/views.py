from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView

from ads.models import Ads, Category
from django.views.decorators.csrf import csrf_exempt
import json


class Index(View):
    def get(self, request):
        return JsonResponse({'status': 'ok'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Ad(View):

    def get(self, request):
        data = Ads.objects.all()
        list_data = []
        for dt in data:
            list_data.append({
                'Id' : dt.id,
                'name' : dt.name,
                'author' : dt.author,
                'price' : dt.price,
                'description' : dt.description,
                'address' : dt.address,
                'is_published' : dt.is_published
                    })
        return JsonResponse(list_data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        ad = Ads(
            name=data['name'],
            author=data['author'],
            price=data['price'],
            description=data['description'],
            address=data['address'],
            is_published=data['is_published']
        )
        ad.save()
        return JsonResponse({'res':'ok'}, status=200)


class AdDetailView(DetailView):
    model = Ads

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
            return JsonResponse({
                    'Id' : ad.id,
                    'name' : ad.name,
                    'author' : ad.author,
                    'price' : ad.price,
                    'description' : ad.description,
                    'address' : ad.address,
                    'is_published' : ad.is_published})
        except:
            return JsonResponse({'error': 'not found'}, status=404)

@method_decorator(csrf_exempt, name='dispatch')
class Cat(View):

    def get(self, request):
        data = Category.objects.all()
        list_data = []
        for dt in data:
            list_data.append({
                'id' : dt.id,
                'name' : dt.name
            })
        return JsonResponse(list_data, safe=False)

    def post(self, request):
        data = json.loads(request.body)
        category = Category(
            name=data['name'],
        )
        category.save()
        return JsonResponse({'res': 'ok'}, status=200)


class CatDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            caregory = self.get_object()
            return JsonResponse({
                    'Id' : caregory.id,
                    'name' : caregory.name,
                   })
        except:
            return JsonResponse({'error': 'not found'}, status=404)
