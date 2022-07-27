from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Max,Min,Count,Avg

from .models import *

# product_list

def product_list(request):
	total_data = Product.objects.count()
	data = Product.objects.all().order_by('-id')[:3]
    
	min_price = ProductAttribute.objects.aggregate(Min('price'))
	max_price = ProductAttribute.objects.aggregate(Max('price'))
   
	return render(request, 'productx_list.html',
		{
			'data':data,
			'total_data':total_data,
			'min_price':min_price,
			'max_price':max_price,
		}
		)

# Search
def search(request):

	q = request.GET['q']
	data = Product.objects.filter(title__icontains = q).order_by('-id')
	return render(request, 'search.html', {'data':data})

# Filter Data
def filter_data(request): 

	colors = request.GET.getlist('color[]')
	categories = request.GET.getlist('category[]')
	brands = request.GET.getlist('brand[]')
	sizes = request.GET.getlist('size[]')
	minPrice = request.GET['minPrice']
	maxPrice = request.GET['maxPrice']

	allProducts = Product.objects.all().order_by('-id').distinct()
	allProducts = allProducts.filter(productattribute__price__gte = minPrice)
	allProducts = allProducts.filter(productattribute__price__lte = maxPrice)

	if len(colors)>0:
		allProducts = allProducts.filter(productattribute__color__id__in = colors).distinct()

	if len(categories)>0:
		allProducts = allProducts.filter(category__id__in = categories).distinct()

	if len(brands)>0:
		allProducts = allProducts.filter(brand__id__in = brands).distinct()

	if len(sizes)>0:
		allProducts = allProducts.filter(productattribute__size__id__in = sizes).distinct()

	t = render_to_string('ajax/productx_list.html', {'data' : allProducts})
	return JsonResponse({'data' : t})
