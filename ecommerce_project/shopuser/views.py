"""
    shopuser view
"""

from django.shortcuts import render
from django.template.loader import render_to_string
from django.apps import apps
from django.http import  JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.views import View
from django.utils.decorators import method_decorator

from .forms import ProductAttributeAddForm, ProductAddForm, ProductUpdateForm, ProductAttributeUpdateForm


Product = apps.get_model('product', 'Product')
ProductAttribute = apps.get_model('product', 'ProductAttribute')
Brand = apps.get_model('product', 'Brand')
Category = apps.get_model('product', 'Category')
Color = apps.get_model('product', 'Color')
Material = apps.get_model('product', 'Material')
Order = apps.get_model('product', 'Order')
ProductSalesBrand = apps.get_model('product', 'ProductSalesBrand')
ProductSalesCat = apps.get_model('product', 'ProductSalesCat')


# Shopuser Products
class ShopuserProducts(View):

    """
		shopuser_product view
	"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get(self, request):

        """
		    get request
        """

        if request.user.user_type == '1':

            shopuser = request.GET.get('s_id')

        else:

            shopuser = request.user

        total_data = Product.objects.filter(shopuser = shopuser ).count()
        shopuser_products = Product.objects.filter(shopuser = shopuser ).order_by('-id')


        return render(request, 'shopuser_products.html',
            {
                'shopuser_products':shopuser_products,
                'total_data':total_data,
            }
            )


# pblish/unpblish products
class PblishUnpblish(View):

    """
		pblish/unpblish products view
	"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get(self, request):

        """
		    get request
        """

        product_id = request.GET.get('product_id')

        shopuser = request.user

        product = Product.objects.get(shopuser = shopuser, id = product_id)

        if product.published:

            product.published = False
            product.save()
            message = "Product Unpublished successfully"
            shopuser_products = Product.objects.filter(shopuser = shopuser ).order_by('-id')
            data = render_to_string('ajax/shopuser_products.html', {
                'shopuser_products' : shopuser_products
                })
            return JsonResponse({'data' : data, 'message':message})

        product.published = True
        product.save()
        message = "Product published successfully"
        shopuser_products = Product.objects.filter(shopuser = shopuser ).order_by('-id')
        data = render_to_string('ajax/shopuser_products.html', {
            'shopuser_products' : shopuser_products
            })
        return JsonResponse({'data' : data, 'message':message})


# Product Uupdate
class ProductUupdate(View):

    """
		Product Uupdate  view
	"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get(self, request):

        """
		    get request
        """

        shopuser = request.user
        p_id = request.GET.get('p_id')

        product = Product.objects.get(shopuser = shopuser, id = p_id)
        p_pa = ProductAttribute.objects.filter(product = product).first()

        form_at = ProductAttributeUpdateForm(instance = p_pa)
        form_pro = ProductUpdateForm(instance = product)

        return render(request, 'product_update.html', {'form_at':form_at, 'form_pro':form_pro})

    
    def post(self, request):

        """
		    post request
        """

        shopuser = request.user
        p_id = request.GET.get('p_id')

        if not p_id:

            p_id = request.POST.get('p_id')

        product = Product.objects.get(shopuser = shopuser, id = p_id)
        p_pa = ProductAttribute.objects.filter(product = product).first()

        form_pro = ProductUpdateForm(request.POST, instance = product)
        form_at =  ProductAttributeUpdateForm(request.POST, request.FILES, instance = p_pa)

        if form_pro.is_valid() and form_at.is_valid():

            form_pro.save()
    
            form_at.save()

            return render(request, 'product_update_success.html')

        form_at_errors = form_at.errors
        form_pro_errors = form_pro.errors

        return render(request, 'product_update.html', {
            'form_at':form_at, 'form_pro':form_pro,
             'form_at_errors': form_at_errors, 'form_pro_errors':form_pro_errors
             })


# Produc Delete
class ProductDelete(View):

    """
		 Produc tDelete  view
	"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get(self, request):

        """
		    get request
        """

        product_id = request.GET.get('product_id')

        shopuser = request.user

        product = Product.objects.get(shopuser = shopuser, id = product_id)

        product.delete()
        message = "product deleted successfully"
        shopuser_products = Product.objects.filter(shopuser = shopuser ).order_by('-id')
        data = render_to_string('ajax/shopuser_products.html',
                            {'shopuser_products' : shopuser_products})
        return JsonResponse({'data' : data, 'message':message})


# Produc Add
class ProductAdd(View):

    """
		 Produc Add  view
	"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def post(self, request):

        """
	        post request
        """

        shopuser = request.user

        form_pro = ProductAddForm(request.POST)
        form_at =  ProductAttributeAddForm(request.POST, request.FILES)

        if form_pro.is_valid and form_at.is_valid:

            product = form_pro.save(request = request)

            form_at.save(request = request, product = product)

            return render(request, 'product_update_success.html')

        errors = form_pro.errors

        form_at = ProductAttributeAddForm()
        form_pro = ProductAddForm()

        return render(request, 'product_add.html', {'form_at':form_at, 'form_pro':form_pro, 'errors':errors})

    def get(self, request):

        """
		    get request
        """

        form_at = ProductAttributeAddForm()
        form_pro = ProductAddForm()

        errors = ''

        return render(request, 'product_add.html', {'form_at':form_at, 'form_pro':form_pro, 'errors':errors})


# shopuser_order_list
class ShopuserOrderList(View):

    """
		shopuser_order_list
	"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get(self, request):

        """
		    get request
        """

        if request.user.user_type == '1':

            shopuser_id = request.GET.get('s_id')
            shopuser = get_user_model().objects.get(id = shopuser_id)

        else:

            shopuser = request.user

        orders = Order.objects.filter(products__shopuser = shopuser, cancelled = False).distinct()

        return render(request, 'shopuser_orders.html', {'orders':orders, 'shopuser':shopuser})


# Shopuser Order Percentage
class ShopuserOrderPercentage(View):

    """
		Shopuser Order Percentage View
	"""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get(self, request):

        """
		    get request
        """

        if request.user.user_type == '1':

            shopuser_id = request.GET.get('s_id')
            shopuser = get_user_model().objects.get(id = shopuser_id)

        else:

            shopuser = request.user

        brands = Brand.objects.all().distinct().order_by('id')
        cats = Category.objects.all().distinct()

        for brand in brands:

            if ProductSalesBrand.objects.filter(shopuser = shopuser, brand = brand).exists():

                brand_sale = ProductSalesBrand.objects.get(shopuser = shopuser, brand = brand)
                total = Product.objects.filter(
                                                brand = brand,
                                                shopuser = shopuser
                                            ).distinct().count()

                sold =  Product.objects.filter(
                                                brand = brand, shopuser = shopuser, sold = True
                                            ).distinct().count()
                brand_sale.total = total
                brand_sale.sold = sold
                brand_sale.brand = brand
                brand_sale.save()

            else :

                total = Product.objects.filter(
                                                brand = brand, shopuser = shopuser
                                            ).distinct().count()
                sold =  Product.objects.filter(
                                                brand = brand, shopuser = shopuser, sold = True
                                            ).distinct().count()
                brand_sale = ProductSalesBrand(
                                                shopuser = shopuser, total = total,
                                                sold = sold, brand = brand
                                            )
                brand_sale.save()

        prod_sale_brand = ProductSalesBrand.objects.filter(
                                         shopuser = shopuser
                                         ).order_by('brand__id')

        for cat in cats:

            if ProductSalesCat.objects.filter(shopuser = shopuser, category = cat).exists():

                cat_sale = ProductSalesCat.objects.get(shopuser = shopuser, category = cat)

                total = Product.objects.filter(
                    category = cat, shopuser = shopuser
                    ).distinct().count()

                sold =  Product.objects.filter(
                    category = cat, shopuser = shopuser, sold = True
                    ).distinct().count()

                cat_sale.total = total
                cat_sale.sold = sold
                cat_sale.cat = cat
                cat_sale.save()

            else :

                total = Product.objects.filter(
                    category = cat, shopuser = shopuser
                    ).distinct().count()

                sold =  Product.objects.filter(
                    category = cat, shopuser = shopuser, sold = True
                    ).distinct().count()

                cat_sale = ProductSalesCat(
                    shopuser = shopuser, total = total,
                    sold = sold, category = cat
                    )

                cat_sale.save()

        prod_sale_cat = ProductSalesCat.objects.filter(
            shopuser = shopuser
            ).order_by('category__id')

        return render(request, 'shopuser_order_percetage.html', {
            'prod_sale_brand':prod_sale_brand,
            'prod_sale_cat':prod_sale_cat,
            'shopuser':shopuser
            })
