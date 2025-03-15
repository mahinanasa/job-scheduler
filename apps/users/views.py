from django.http import JsonResponse
from django.views import View
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class UserView(View):
    def get(self, request):
        return JsonResponse({"message": "User API working!"})

class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('jobs:dashboard')