from unicodedata import category
from django.shortcuts import render
from django.template.loader import render_to_string
from django.apps import apps
from django.http import  JsonResponse

from .forms import *


Product = apps.get_model('product', 'Product')
ProductAttribute = apps.get_model('product', 'ProductAttribute')
Brand = apps.get_model('product', 'Brand')
Category = apps.get_model('product', 'Category')
Color = apps.get_model('product', 'Color')
Material = apps.get_model('product', 'Material')
Order = apps.get_model('product', 'Order')

# shopuser_product
def shopuser_products(request):

    """
		shopuser_product view
	"""
    
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
def shopuser_order_list(request):

    """
		shop user orders
	"""
    shopuser = request.user

    orders = Order.objects.filter(products__shopuser = shopuser).distinct()

    return render(request, 'shopuser_orders.html', {'orders':orders,})
    
			
            
	
		

		


