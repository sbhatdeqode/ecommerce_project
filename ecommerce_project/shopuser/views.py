"""
    shopuser view
"""

from django.shortcuts import render
from django.template.loader import render_to_string
from django.apps import apps
from django.http import  JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .forms import *


Product = apps.get_model('product', 'Product')
ProductAttribute = apps.get_model('product', 'ProductAttribute')
Brand = apps.get_model('product', 'Brand')
Category = apps.get_model('product', 'Category')
Color = apps.get_model('product', 'Color')
Material = apps.get_model('product', 'Material')
Order = apps.get_model('product', 'Order')
ProductSalesBrand = apps.get_model('product', 'ProductSalesBrand')
ProductSalesCat = apps.get_model('product', 'ProductSalesCat')



# shopuser_product
@login_required
def shopuser_products(request):

    """
		shopuser_product view
	"""
    if request.user.user_type == '1':

        shopuser = request.GET.get('s_id')

    else:

        shopuser = request.user

    Product = apps.get_model('product', 'Product')

    total_data = Product.objects.filter(shopuser = shopuser ).count()
    shopuser_products = Product.objects.filter(shopuser = shopuser ).order_by('-id')
    
   
    return render(request, 'shopuser_products.html',
		{
			'shopuser_products':shopuser_products,
			'total_data':total_data,
		}
		)


# pblish/unpblish products
@login_required
def pblish_unpblish_products(request):

    """
		pblish/unpblish products
	"""

    product_id = request.GET.get('product_id')

    shopuser = request.user
    Product = apps.get_model('product', 'Product')
    product = Product.objects.get(shopuser = shopuser, id = product_id)

    if product.published:

        product.published = False
        product.save()
        message = "Product Unpublished successfully"
        shopuser_products = Product.objects.filter(shopuser = shopuser ).order_by('-id')
        t = render_to_string('ajax/shopuser_products.html', {'shopuser_products' : shopuser_products})
        return JsonResponse({'data' : t, 'message':message})

    product.published = True
    product.save()
    message = "Product published successfully"
    shopuser_products = Product.objects.filter(shopuser = shopuser ).order_by('-id')
    t = render_to_string('ajax/shopuser_products.html', {'shopuser_products' : shopuser_products})
    return JsonResponse({'data' : t, 'message':message})
    

# update product
@login_required
def product_update(request):

    """
		pblish/unpblish products
	"""

    shopuser = request.user
    p_id = request.GET.get('p_id')
    product = Product.objects.get(shopuser = shopuser, id = p_id)
    pa = ProductAttribute.objects.filter(product = product).first()

    if request.method=='POST':

       
        form_pro = ProductUpdateForm(request.POST)
        form_at =  ProductAttributeForm(request.POST)


        brand = Brand.objects.get(id = form_pro.data.get('brand'))
        cat = Category.objects.get(id = form_pro.data.get('category'))

        product.title = form_pro.data.get('title')
        product.detail = form_pro.data.get('detail')
        product.category = cat
        product.brand = brand
        

        if form_pro.data.get('published') == 'on':
            product.published = True
        else:
            product.published = False

        product.save()

        material = Material.objects.get(id = form_at.data.get('material'))
        color = Color.objects.get(id = form_at.data.get('color'))

        pa.color = color
        pa.material = material
        pa.image = 'product_imgs/'+form_at.data.get('image')

        pa.save()
        
        return render(request, 'product_update_success.html')

    
    form_at = ProductAttributeForm(instance = pa)
    form_pro = ProductUpdateForm(instance = product)

    return render(request, 'product_update.html', {'form_at':form_at, 'form_pro':form_pro})

    
# delete products
@login_required
def product_delete(request):

    """
		delete products
	"""

    product_id = request.GET.get('product_id')

    shopuser = request.user
    Product = apps.get_model('product', 'Product')
    product = Product.objects.get(shopuser = shopuser, id = product_id)

    product.delete()
    message = "product deleted successfully"
    shopuser_products = Product.objects.filter(shopuser = shopuser ).order_by('-id')
    t = render_to_string('ajax/shopuser_products.html', {'shopuser_products' : shopuser_products})
    return JsonResponse({'data' : t, 'message':message})


# add product
@login_required
def product_add(request):

    """
		add product
	"""
    
    shopuser = request.user

    if request.method=='POST':

       
        form_pro = ProductUpdateForm(request.POST)
        form_at =  ProductAttributeForm(request.POST)

        brand = Brand.objects.get(id = form_pro.data.get('brand'))
        cat = Category.objects.get(id = form_pro.data.get('category'))

        title = form_pro.data.get('title')
        detail = form_pro.data.get('detail')

        product = Product(brand = brand, category = cat, title = title, detail = detail, shopuser = shopuser)
        
        if form_pro.data.get('published') == 'on':
            product.published = True
        else:
            product.published = False

        product.save()

        pa = ProductAttribute(product = product)

        material = Material.objects.get(id = form_at.data.get('material'))
        color = Color.objects.get(id = form_at.data.get('color'))

        pa.price = form_at.data.get('price')
        pa.color = color
        pa.material = material
        pa.image = 'product_imgs/'+form_at.data.get('image')

        pa.save()
        
        return render(request, 'product_update_success.html')

    
    form_at = ProductAttributeForm()
    form_pro = ProductUpdateForm()

    return render(request, 'product_add.html', {'form_at':form_at, 'form_pro':form_pro})


# shop user order list
@login_required
def shopuser_order_list(request):

    """
		shop user orders
	"""

    if request.user.user_type == '1':

        shopuser_id = request.GET.get('s_id')
        shopuser = get_user_model().objects.get(id = shopuser_id)

    else:

        shopuser = request.user

    orders = Order.objects.filter(products__shopuser = shopuser).distinct()
   

    return render(request, 'shopuser_orders.html', {'orders':orders, 'shopuser':shopuser})
    

# shop user order percentage list
@login_required
def shopuser_order_percentage(request):

    """
		shop user orders percentage
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
            total = Product.objects.filter(brand = brand, shopuser = shopuser).distinct().count()
            sold =  Product.objects.filter(brand = brand, shopuser = shopuser, sold = True).distinct().count()
            brand_sale.total = total
            brand_sale.sold = sold
            brand_sale.brand = brand
            brand_sale.save()

        else :

            total = Product.objects.filter(brand = brand, shopuser = shopuser).distinct().count()
            sold =  Product.objects.filter(brand = brand, shopuser = shopuser, sold = True).distinct().count()
            brand_sale = ProductSalesBrand(shopuser = shopuser, total = total, sold = sold, brand = brand)
            brand_sale.save()

    prod_sale_brand = ProductSalesBrand.objects.filter(shopuser = shopuser).order_by('brand__id')


    for cat in cats:

        if ProductSalesCat.objects.filter(shopuser = shopuser, category = cat).exists():

            cat_sale = ProductSalesCat.objects.get(shopuser = shopuser, category = cat)
            total = Product.objects.filter(category = cat, shopuser = shopuser).distinct().count()
            sold =  Product.objects.filter(category = cat, shopuser = shopuser, sold = True).distinct().count()
            cat_sale.total = total
            cat_sale.sold = sold
            cat_sale.cat = cat
            cat_sale.save()

        else :

            total = Product.objects.filter(category = cat, shopuser = shopuser).distinct().count()
            sold =  Product.objects.filter(category = cat, shopuser = shopuser, sold = True).distinct().count()
            cat_sale = ProductSalesCat(shopuser = shopuser, total = total, sold = sold, category = cat)
            cat_sale.save()

    prod_sale_cat = ProductSalesCat.objects.filter(shopuser = shopuser).order_by('category__id')



    return render(request, 'shopuser_order_percetage.html', {'prod_sale_brand':prod_sale_brand, 'prod_sale_cat':prod_sale_cat, 'shopuser':shopuser})			
            
	
		

		


