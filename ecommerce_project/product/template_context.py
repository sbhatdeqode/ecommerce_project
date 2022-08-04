"""
	custom context
"""

from django.db.models import Min,Max
from .models import Product, ProductAttribute, Cart, Wishlist

def get_filters(request):

    """
        context method
	"""

    if request.user.is_authenticated:

        cats = Product.objects.distinct().values('category__title', 'category__id')
        brands = Product.objects.distinct().values('brand__title', 'brand__id')
        colors = ProductAttribute.objects.distinct().values('color__title', 'color__id','color__color_code')
        mats = ProductAttribute.objects.distinct().values('material__title', 'material__id')
        minMaxPrice = ProductAttribute.objects.aggregate(Min('price'), Max('price'))
        cart_products = Cart.objects.filter(customer = request.user)
        wishlist_products = Wishlist.objects.filter(customer = request.user)

        data = {

				'cats':cats,
				'brands':brands,
				'colors':colors,
				'mats':mats,
				'minMaxPrice':minMaxPrice,
				'cart_products':cart_products,
				'wishlist_products': wishlist_products,

		}
        return data

    return {}
