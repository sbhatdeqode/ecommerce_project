"""
    forms moudule
"""

from django import forms
from django.apps import apps

Product = apps.get_model('product', 'Product')
ProductAttribute = apps.get_model('product', 'ProductAttribute')

class ProductUpdateForm(forms.ModelForm):

    """
        Product Update form
    """

    class Meta:

        """
           meta class
        """

        model = Product
        exclude = ('shopuser',)


class ProductAttributeForm(forms.ModelForm):

    """
        ProductAttribute form
    """

    class Meta:

        """
           meta class
        """

        model = ProductAttribute
        exclude = ('product',)
