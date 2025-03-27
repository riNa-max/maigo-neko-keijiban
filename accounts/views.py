from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView,UpdateView
from django.urls import reverse_lazy
from .forms import AccountUpdateForm,CustomUserCreationForm
from django.contrib.auth import get_user_model, login
from django.shortcuts import render, redirect
from django.views import View
from lost_cat.models import Lostcat
from .forms import CustomLoginForm

Account = get_user_model()

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomLoginForm

class LogoutConfirmView(TemplateView):
    template_name = "accounts/logout_confirm.html"

class LogoutView(LogoutView):
    template_name='accounts/logout.html'

class SignUpView(View):
    template_name = 'accounts/signup.html'

    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('registration_complete')
        return render(request, self.template_name, {'form': form})

class RegistrationCompleteView(View):
    template_name = 'accounts/registration_complete.html'

    def get(self, request):
        return render(request, self.template_name)

class AccountDeleteView(LoginRequiredMixin, View):
    template_name = 'accounts/account_confirm_delete.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        user = request.user
        user.delete()
        return redirect('login')

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/myaccount.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user

        try:
            context['lost_cat'] = user.lost_cat
        except Lostcat.DoesNotExist:
            context['lost_cat'] = None

        return context

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountUpdateForm
    template_name = 'accounts/account_edit.html'
    success_url = reverse_lazy('myaccount') 

    def get_object(self, queryset=None):
        return self.request.user

class HomeView(TemplateView):
    template_name = 'accounts/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_authenticated:
            context['lost_cat'] = Lostcat.objects.filter(owner=user).first()
        else:
            context['lost_cat'] = None

        return context