from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from django.db.models import Max,Min,Count,Avg
from django.contrib import messages

from .models import *

# product_list

def product_list(request):
	total_data = Product.objects.count()
	data = Product.objects.all().order_by('-id')[:1]
    
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

# Load More
def load_more_data(request):

	offset = int(request.GET['offset'])
	limit = int(request.GET['limit'])
	data = Product.objects.all().order_by('-id')[offset: offset + limit]
	t = render_to_string('ajax/productx_list.html', {'data':data})

	return JsonResponse({'data':t})


# cart add
def cart_add(request):

	product_id = int(request.GET['product_id'])

	customer = request.user
	product = Product.objects.get(id = product_id)

	cart = Cart(customer = customer, product = product )
	cart.save()

	carts = Cart.objects.filter(customer = customer)

	messages.success(request, 'Product added to cart successfully')
	return JsonResponse({'totalitems':len(carts)})


# cart list
def cart_list(request):
   
	cart = Cart.objects.filter(customer = request.user)
	total_amount = 0

	if cart:
		for c in cart:
			pass
			#total_amount += c.product.productattribute_set.first.price

	return render(request, 'cartx.html', {'total_amount': total_amount})