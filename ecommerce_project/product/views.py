"""
	views
"""

from django.shortcuts import render
from django.http import  JsonResponse
from django.template.loader import render_to_string
from django.db.models import Max, Min
from django.contrib import messages
from django.shortcuts import redirect

from .models import *


# product_list
def product_list(request):

	"""
		product_list view
	"""

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

	"""
		search view
	"""

	q = request.GET['q']
	data = Product.objects.filter(title__icontains = q).order_by('-id')
	return render(request, 'search.html', {'data':data})


# Filter Data
def filter_data(request): 

	"""
		filter_data view
	"""

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

	"""
		load_more_data view
	"""

	offset = int(request.GET['offset'])
	limit = int(request.GET['limit'])
	data = Product.objects.all().order_by('-id')[offset: offset + limit]
	t = render_to_string('ajax/productx_list.html', {'data':data})

	return JsonResponse({'data':t})


# cart add
def cart_add(request):

	"""
		cart_add view
	"""

	product_id = int(request.GET['product_id'])

	customer = request.user
	product = Product.objects.get(id = product_id)

	cart = Cart(customer = customer, product = product )
	cart.save()

	carts = Cart.objects.filter(customer = customer)

	return JsonResponse({'totalitems':len(carts)})


# cart list
def cart_list(request):

	"""
		cart_list view
	"""
   
	if request.user.is_authenticated:
		cart = Cart.objects.filter(customer = request.user)
		total_amount = 0

		if cart:
			for c in cart:

				pa = ProductAttribute.objects.get(product = c.product)
				total_amount += pa.price

		return render(request, 'cart.html', {'total_amount': total_amount})

	return redirect('/admin/login/')


# cart delete
def cart_delete(request):

	"""
		cart_delete view
	"""
  
	product_id = request.GET['id']
	
	cart_d = Cart.objects.filter(product__id = product_id).first()
	cart_d.delete()

	cart_products = Cart.objects.filter(customer = request.user)
	cart = Cart.objects.filter(customer = request.user)
	total_amount = 0

	if cart:
		for c in cart:

			pa = ProductAttribute.objects.get(product = c.product)
			total_amount += pa.price

	t = render_to_string('ajax/cart.html',{'total_amount':total_amount, 'cart_products':cart_products})
	return JsonResponse({'data':t,'totalitems':len(cart_products)})


# wishlist add
def wishlist_add(request):

	"""
		wishlist_add view
	"""

	product_id = int(request.GET['product_id'])
    
	customer = request.user
	product = Product.objects.get(id = product_id)

	if Wishlist.objects.filter(product__id = product_id).exists():

		wishlists = Wishlist.objects.filter(customer = customer)
		message = "Item already exists in the cart"

		return JsonResponse({'totalitems':len(wishlists), 'message':message})

	wishlist = Wishlist(customer = customer, product = product )
	wishlist.save()

	wishlists = Wishlist.objects.filter(customer = customer)
	message = "Item is added to wishlist"

	return JsonResponse({'totalitems':len(wishlists), 'message':message})


# wishlist list
def wishlist_list(request):

	"""
		wishlist_list view
	"""
   
	if request.user.is_authenticated:

		return render(request, 'wishlist.html',)

	return redirect('/admin/login/')


# wishlist delete
def wishlist_delete(request):

	"""
		wishlist_delete view
	"""
  
	product_id = request.GET['id']
	
	wish_d = Wishlist.objects.filter(product__id = product_id).first()
	wish_d.delete()

	wishlist_products = Wishlist.objects.filter(customer = request.user)
	

	t = render_to_string('ajax/wishlist.html',{'wishlist_products':wishlist_products})
	return JsonResponse({'data':t, 'totalitems':len(wishlist_products), 'message': "Item successfully deleted" })
