
from multiprocessing import context
from allauth.account import views
from allauth.account import app_settings
from django.shortcuts import render
from django.views import View

from django.views.generic.list import ListView
from django.contrib.auth import get_user_model
from django.db.models import Q


class ShopUserSignupView(views.SignupView):
    template_name = "account/shop_user_signup." + app_settings.TEMPLATE_EXTENSION

signup = ShopUserSignupView.as_view()

class ShopUserListView(ListView):
    model = get_user_model()
    template_name = "account/shopuser_list." + app_settings.TEMPLATE_EXTENSION

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(~Q(shop_name = "NA"))
        qs = qs.filter(Q(is_active = False))
        return qs

shopuser_list = ShopUserListView.as_view()


class shopuser_details(View):

    template_name_details = "account/shopuser_detail." + app_settings.TEMPLATE_EXTENSION
    template_name_approval = "account/shopuser_approval." + app_settings.TEMPLATE_EXTENSION

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

           