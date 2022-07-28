from .models import Product, ProductAttribute, Cart
from django.db.models import Min,Max

def get_filters(request):

		cats = Product.objects.distinct().values('category__title', 'category__id')
		brands = Product.objects.distinct().values('brand__title', 'brand__id')
		colors = ProductAttribute.objects.distinct().values('color__title', 'color__id','color__color_code')
		mat = ProductAttribute.objects.distinct().values('material__title', 'material__id')
		minMaxPrice = ProductAttribute.objects.aggregate(Min('price'), Max('price'))
		cart_products = Cart.objects.filter(customer = request.user)

		data={
			'cats':cats,
			'brands':brands,
			'colors':colors,
			'mat':mat,
			'minMaxPrice':minMaxPrice,
			'cart_products':cart_products,
		}
		return data