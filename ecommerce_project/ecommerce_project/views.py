"""
	Home view module
"""

from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

class Home(View):

	"""
		Home view
	"""

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):

		return super().dispatch(*args, **kwargs)

	def get(self, request):

		"""
			get method
		"""

		if request.user.user_type == '1':

			response = redirect('adminops/adminops_home')
			return response

		elif request.user.user_type == '2':

			response = redirect('shopuser/shopuser_products')
			return response

		else:
			response = redirect('products/product_list')
			return response