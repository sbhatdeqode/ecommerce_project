import json
from allauth.account import views
from allauth.account import app_settings
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views import View, generic
from django.views.generic.list import ListView
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse

from .forms import ModalForm, ShopuserAddForm


class ShopUserSignupView(views.SignupView):

    """
		Shopuser Signup View
	"""

    template_name = "account/shop_user_signup." + app_settings.TEMPLATE_EXTENSION

signup = ShopUserSignupView.as_view()

class ShopUserListView(ListView):

    """
		Shopuser List View
	"""

    model = get_user_model()
    template_name = "account/shopuser_list." + app_settings.TEMPLATE_EXTENSION

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(user_type = '2')
        qs = qs.filter(Q(is_active = False))
        return qs

shopuser_list = ShopUserListView.as_view()


class shopuser_details(View):

    """
		Shopuser detail View
	"""

    template_name_details = "account/shopuser_detail." + app_settings.TEMPLATE_EXTENSION
    template_name_approval = "account/shopuser_approval." + app_settings.TEMPLATE_EXTENSION

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        user_model = get_user_model()
        context = {}
        user_id = kwargs["user_id"]
        context["shopuser"] = user_model.objects.get(id = user_id)
        return render(request, self.template_name_details, context)

    def post(self, request):

        context = {}

        user_model = get_user_model()
       
        user_id = request.POST.get('user_id')
        
        user =  user_model.objects.get(id = user_id)

        context["shopuser"] = user
     
        if request.POST.get('result') == 'approve':
            user.is_active = True
            user.save()
            context["result"] = "APPROVED"
            #send_mail('You shop got approved', 'Your shop regestration request is approved by the Admin', settings.EMAIL_HOST_USER, user.email)

        else :
            
            context["result"] = "REJECTED"
            #send_mail('You shop got rejected', 'Your shop regestration request is requested by the Admin', settings.EMAIL_HOST_USER, user.email)
        
        print(request.POST.get('reason'))
        return render(request, self.template_name_approval, context)


class ShopuserCrud(View):

    """
		Shopuser crud View
	"""

    template_name =  "account/shopuser_crud." + app_settings.TEMPLATE_EXTENSION

    model = get_user_model()

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        user_model = get_user_model()
        context = {}
       
        context["object_list"] = user_model.objects.filter(user_type = '2', is_active = True)
        context['form'] = ModalForm()
        return render(request, self.template_name, context)

shopuser_crud = ShopuserCrud.as_view()

        
class UpdateShopuser(View):

    """
		Shopuser Update View
	"""

    template_name =  "account/shopuser_update." + app_settings.TEMPLATE_EXTENSION

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        pk = kwargs["pk"]
        shop_user = get_user_model().objects.get(id = pk)
        form = ModalForm
        return render(request, self.template_name, {
        'form': form,
        'shop_user': shop_user,
        })

    def post(self, request, *args, **kwargs):

        pk = kwargs["pk"]
        shop_user = get_user_model().objects.get(id = pk)
        shop_type = request.POST.get("shop_type")
        shop_name = request.POST.get("shop_name")
        shop_user.shop_type = shop_type
        shop_user.shop_name = shop_name
        shop_user.save()

        return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                       
                        "showMessage": f"{shop_user.email} updated."
                    })
                }
            )
        

class DeleteShopuser(View):

    """
		Shopuser delete View
	"""

    template_name =  "account/shopuser_delete." + app_settings.TEMPLATE_EXTENSION

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        pk = kwargs["pk"]
        shop_user = get_user_model().objects.get(id = pk)

        form = ModalForm
        return render(request, self.template_name, {
            'form': form,
            'shop_user': shop_user,
        })

    def post(self, request, *args, **kwargs):

        pk = kwargs["pk"]
        shop_user = get_user_model().objects.get(id = pk)
        shop_user.delete()

        return HttpResponse(
            status=204,
            headers={
                'HX-Trigger': json.dumps({
                   
                    "showMessage":  "shop user deleted."
                })
            })


class AddShopuser(View):

    """
		Shopuser Add View
	"""

    template_name =  "account/shopuser_add." + app_settings.TEMPLATE_EXTENSION
    template_name_success =  "account/shopuser_add_success." + app_settings.TEMPLATE_EXTENSION

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        form = ShopuserAddForm()

        return render(request, self.template_name, {
        'form': form,'errors':'',
        })

    def post(self, request, *args, **kwargs):

        form = ShopuserAddForm(request.POST)

        if form.is_valid():
            shopuser = form.save()
            return render(request, self.template_name_success)

        errors = form.errors

        form = ShopuserAddForm()
    
        return render(request, self.template_name, {
        'form': form, 'errors':errors
        })


class EditProfileCustomer(generic.UpdateView):

    template_name = 'account/profile_edit.html'
    model = get_user_model()
    fields = ['email','username','dob','adress', 'gender']
    success_url = '/account/profile'


class EditProfileShopuser(generic.UpdateView):

    template_name = 'account/profile_edit.html'
    model = get_user_model()
    fields = ['email','username','dob','adress', 'gender', 'shop_type', 'shop_name']
    success_url = '/account/profile'


class Profile(View):

    """
		Profile View
	"""

    template_name =  'account/profile.html'
    

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):

        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):

        #print(request.META.get('HTTP_REFERER')[-2:-14:-1][::-1])

        id = request.GET.get('id')

        if id:
            user = get_user_model().objects.get(id = id)
        else:
            user = request.user

        return render(request, self.template_name, {'user':user,})

    


    