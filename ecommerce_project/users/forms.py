"""
    user forms module
"""

from allauth.account.forms import SignupForm
from django import forms
from django.contrib.auth import get_user_model

USER_TYPE_CHOICES =(
    ("1", "Admin"),
    ("2", "Shopuser"),
    ("3", "Customer"),

)


class CustomSignupForm(SignupForm):

    """
        custom signup form
    """

    dob = forms.DateField(label='Date Of Birth',
     input_formats = ['%m/%d/%Y', ],
     )

    gender=forms.CharField(
        label=("Gender"),
        widget=forms.TextInput(
            attrs={ "placeholder":("Gender")})
    )

    adress=forms.CharField(
        label=("Adress"),
        widget=forms.TextInput(
            attrs={ "placeholder":("Adress")})
    )

    shop_type =  forms.CharField(
        label=("Shop Type"),
        widget=forms.TextInput(
            attrs={ "placeholder":("Shop Type")})
    )

    user_type =  forms.CharField(
        label=("User Type"),
        widget=forms.TextInput(
            attrs={ "placeholder":("User Type")})
    )

    shop_name =  forms.CharField(
        label=("Shop Name"),
        widget=forms.TextInput(
            attrs={ "placeholder":("Shop Name")})
    )


    def save(self, request):

        user = super(CustomSignupForm, self).save(request)
        user.dob = self.cleaned_data['dob']
        user.gender=self.cleaned_data['gender']
        user.adress = self.cleaned_data['adress']
        user.user_type = self.cleaned_data['user_type']
        user.shop_type = self.cleaned_data['shop_type']
        user.shop_name = self.cleaned_data['shop_name']

        if self.cleaned_data['shop_name'] != 'NA':
            user.is_active = False

        #send_mail('A Shop User Registered',
        # 'Please Go to the website and approve/reject the request',
        # settings.EMAIL_HOST_USER, [settings.RECIPIENT_ADDRESS])

        user.save()
        return user


class ModalForm(forms.Form):

    """
        shopuser update modal form
    """

    shop_type = forms.CharField(label="shop_type", max_length=30)
    shop_name = forms.CharField(label="shop_name", max_length=30)


class ShopuserAddForm(forms.ModelForm):

    """
        shopuser add form
    """

    class Meta:

        """
            meta
        """
        model = get_user_model()
        fields = ['email', 'username', 'dob', 'user_type',
         'adress', 'gender', 'shop_name', 'shop_type',]
