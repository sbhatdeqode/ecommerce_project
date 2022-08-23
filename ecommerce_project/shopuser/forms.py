"""
    forms moudule
"""

from django import forms
from django.apps import apps

Product = apps.get_model('product', 'Product')
ProductAttribute = apps.get_model('product', 'ProductAttribute')
Brand = apps.get_model('product', 'Brand')
Category = apps.get_model('product', 'Category')
Color = apps.get_model('product', 'Color')
Material = apps.get_model('product', 'Material')

class ProductAddForm(forms.ModelForm):

    """
        Product Update form
    """

    class Meta:

        """
           meta class
        """

        model = Product
        exclude = ('shopuser',)

    def save(self, request):

        shopuser = request.user
        brand = Brand.objects.get(id = self.data.get('brand'))
        cat = Category.objects.get(id = self.data.get('category'))

        title = self.data.get('title')
        detail = self.data.get('detail')

        product = Product(
                        brand = brand, category = cat,
                        title = title, detail = detail,
                        shopuser = shopuser,
                        )

        if self.data.get('published') == 'on':
            product.published = True
        else:
            product.published = False

        product.save()

        return product


class ProductAttributeAddForm(forms.ModelForm):

    """
        ProductAttribute form
    """

    class Meta:

        """
           meta class
        """

        model = ProductAttribute
        exclude = ('product',)

    def save(self, request, product):

        p_pa = ProductAttribute(product = product)

        material = Material.objects.get(id = self.data.get('material'))
        color = Color.objects.get(id = self.data.get('color'))

        p_pa.price = self.data.get('price')
        p_pa.color = color
        p_pa.rating = self.data.get('rating')
        p_pa.material = material
        p_pa.image = request.FILES.get('image')

        p_pa.save()


class ProductUpdateForm(forms.ModelForm):

    """
        Product Update form
    """

    def __init__(self, *args, **kwargs):

        super(ProductUpdateForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)

        if instance and instance.id:

            self.fields['shopuser'].required = False

            self.fields['shopuser'].widget.attrs['readonly'] = True
            

    def clean_shopuser(self):
        
        instance = getattr(self, 'instance', None)
        print(instance)
        if instance:
            return instance.shopuser
        else:
            return self.cleaned_data.get('shopuser', None)

    class Meta:

        """
           meta class
        """

        model = Product
        exclude = ()

    


class ProductAttributeUpdateForm(forms.ModelForm):

    """
        ProductAttribute form
    """

    def __init__(self, *args, **kwargs):

        super(ProductAttributeUpdateForm, self).__init__(*args, **kwargs)

        instance = getattr(self, 'instance', None)

        if instance and instance.id:

            self.fields['product'].required = False

            self.fields['product'].widget.attrs['readonly'] = True

    class Meta:

        """
           meta class
        """

        model = ProductAttribute
        exclude = ()

    def clean_product(self):
        
        instance = getattr(self, 'instance', None)
        if instance:
            return instance.product
        else:
            return self.cleaned_data.get('product', None)