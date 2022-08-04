"""
	views
"""

from django.shortcuts import render
from django.http import  JsonResponse
from django.template.loader import render_to_string
from django.db.models import Max, Min
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views import View
from django.utils.decorators import method_decorator

from .models import *


# home
@login_required
def home(request):
	
	"""
		home
	"""
    
	if request.user.user_type == '1':

		response = redirect('adminops/adminops_home')
		return response

	elif request.user.user_type == '2':

		response = redirect('shopuser/shopuser_products')
		return response

	else:
		response = redirect('products/product_list')
		return response


# product_list
class ProductList(View):

	"""
		product_list view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)


	def get(self, request):

		total_data = Product.objects.count()
		data = Product.objects.filter(published = True).order_by('-id')

		p = Paginator(data, 6)
		page = request.GET.get('page')
		datas = p.get_page(page)
   
		return render(request, 'productx_list.html',
								{
									'datas':datas,
			
									'total_data':total_data,
			
								}
					)


# Search
class Search(View):

	"""
		search view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)

	def get(self, request):

		q = request.GET['q']
		data = Product.objects.filter(title__icontains = q, published = True).order_by('-id')
		return render(request, 'search.html', {'data':data})


# filter_data view
class FilterData(View):

	"""
		filter_data view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)

	def get(self, request):

		colors = request.GET.getlist('color[]')
		categories = request.GET.getlist('category[]')
		brands = request.GET.getlist('brand[]')
		sizes = request.GET.getlist('size[]')
		price = request.GET.get('price')

		allProducts = Product.objects.filter(published = True).order_by('-id').distinct()

		if price :

			if price == 'low':

				allProducts = Product.objects.filter(published = True).order_by('productattribute__price').distinct()

			elif price == 'high':

				allProducts = Product.objects.filter(published = True).order_by('-productattribute__price').distinct()

		if len(colors)>0:
			allProducts = allProducts.filter(productattribute__color__id__in = colors).distinct()

		if len(categories)>0:
			allProducts = allProducts.filter(category__id__in = categories).distinct()

		if len(brands)>0:
			allProducts = allProducts.filter(brand__id__in = brands).distinct()

		if len(sizes)>0:
			allProducts = allProducts.filter(productattribute__size__id__in = sizes).distinct()

		p = Paginator(allProducts, 6)
		page = request.GET.get('page')
		datas = p.get_page(page)

		t = render_to_string('ajax/productx_list.html', {'data' : datas})
		return JsonResponse({'data' : t})
	

# Cart Add
class CartAdd(View):

	"""
		Cart Add view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)

	def get(self, request):

		product_id = request.GET.get('product_id')
	
		customer = request.user
		product = Product.objects.get(id = product_id)

		if Cart.objects.filter(product__id = product_id, customer = request.user).exists():

			message = "Item already exists in the cart"

			carts = Cart.objects.filter(customer = customer)

			return JsonResponse({'totalitems':len(carts), 'message':message})

		cart = Cart(customer = customer, product = product )
		cart.save()

		carts = Cart.objects.filter(customer = customer)
		message = "Item added to cart"

		return JsonResponse({'totalitems':len(carts), 'message':message})


# Cart List
class CartList(View):

	"""
		Cart List view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)

	def get(self, request):

		if request.user.is_authenticated:
			cart = Cart.objects.filter(customer = request.user)
			total_amount = 0

			if cart:
				for c in cart:

					pa = ProductAttribute.objects.get(product = c.product)
					total_amount += pa.price

			return render(request, 'cart.html', {'total_amount': total_amount})

		return redirect('/account/login/')


# Cart Delete
class CartDelete(View):

	"""
		Cart Delete view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)

	def get(self, request):

		product_id = request.GET['id']
		
		cart_d = Cart.objects.filter(product__id = product_id, customer = request.user).first()
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


# wishlist_add
class WishlistAdd(View):

	"""
		wishlist_add view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)


	def get(self, request):

		product_id = int(request.GET['product_id'])
		
		customer = request.user
		product = Product.objects.get(id = product_id)

		if Wishlist.objects.filter(product__id = product_id, customer = customer).exists():

			wishlists = Wishlist.objects.filter(customer = customer)
			message = "Item already exists in the wishlist"

			return JsonResponse({'totalitems':len(wishlists), 'message':message})

		wishlist = Wishlist(customer = customer, product = product )
		wishlist.save()

		wishlists = Wishlist.objects.filter(customer = customer)
		message = "Item is added to wishlist"

		return JsonResponse({'totalitems':len(wishlists), 'message':message})


# wishlist list
class WishlistList(View):

	"""
		wishlist_list view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)

	def get(self, request):

		if request.user.is_authenticated:

			wishlist_products = Wishlist.objects.filter(customer = request.user)

			return render(request, 'wishlist.html',{'wishlist_products':wishlist_products})

		return redirect('/admin/login/')

	
# wishlist Delete
class WishlistDelete(View):

	"""
		Wishlist Delete view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)

	def get(self, request):

		product_id = request.GET['id']
	
		wish_d = Wishlist.objects.filter(product__id = product_id, customer = request.user).first()
		wish_d.delete()

		wishlist_products = Wishlist.objects.filter(customer = request.user)
		
		t = render_to_string('ajax/wishlist.html',{'wishlist_products':wishlist_products})
		return JsonResponse({'data':t, 'totalitems':len(wishlist_products), 'message': "Item successfully deleted" })


# place order
class PlaceOrder(View):

	"""
		 place order view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)

	def get(self, request):

		customer = request.user

		cart = Cart.objects.filter(customer = customer)
		

		order = Order(customer = customer)
		order.save()

		total_amount = 0

		for c in cart:
			
			pa = ProductAttribute.objects.get(product = c.product)
			total_amount += pa.price
			c.product.sold = True
			c.product.save()
			order.products.add(c.product)
			c.delete()
			wishlist = Wishlist.objects.filter(customer = customer, product =c.product)
			wishlist.delete()

		order.total_amount = total_amount
		order.save()

		return render(request, 'order.html', {'order':order, 'total_amount':total_amount})


# Buy Now
class BuyNow(View):

	"""
		 Buy Now view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)

	def get(self, request):


		customer = request.user

		p_id = request.GET['pid']

		product = Product.objects.get(id = p_id)

		total_amount = 0

		if Cart.objects.filter(product__id = p_id, customer = request.user).exists():

			cart = Cart.objects.filter(product__id = p_id, customer = request.user)
			cart.delete()

		if Wishlist.objects.filter(product__id = p_id, customer = request.user).exists():

			wishlist = Wishlist.objects.filter(product__id = p_id, customer = request.user)
			wishlist.delete()

		order = Order(customer = customer)
		order.save()

		pa = ProductAttribute.objects.get(product = product)
		total_amount += pa.price
		product.sold = True
		product.save()
		order.products.add(product)
		order.total_amount = total_amount
		order.save()

		return render(request, 'order.html',{'order':order, 'total_amount':total_amount})


# Order List
class OrderList(View):

	"""
		Order List view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)

	def get(self, request):

		if request.user.get_user_type_display() == 'Admin':

			c_id = request.GET.get('c_id')
			customer = get_user_model().objects.get(id = c_id)

		else :
			customer = request.user

		orders = Order.objects.filter(customer = customer)

		return render(request, 'order_list.html', {'orders':orders,})





# Order Cancel
class OrderCancel(View):

	"""
		Order Cancel view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)

	def get(self, request):

		order_id = request.GET['order_id']

		order = Order.objects.get(id = str(order_id) )

		order.cancelled = True
		order.save()

		customer = request.user

		orders = Order.objects.filter(customer = customer)

		return render(request, 'order_list.html', {'orders':orders,})


# Product Detail
class ProductDetail(View):

	"""
		Product Detail view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)

	def get(self, request):

		p_id = request.GET.get('p_id')

		product = Product.objects.get(id = p_id)

		return render(request, 'product_detail.html', {'product':product,})


