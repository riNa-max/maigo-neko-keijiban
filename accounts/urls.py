from django.urls import path
from .views import CustomLoginView,DashboardView,AccountUpdateView,LogoutView,SignUpView,AccountDeleteView,RegistrationCompleteView,LogoutConfirmView,HomeView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('logout/confirm/', LogoutConfirmView.as_view(), name='logout_confirm'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('registration-complete/', RegistrationCompleteView.as_view(), name='registration_complete'),
    path('delete_account/', AccountDeleteView.as_view(), name='delete_account'),
    path('myaccount/', DashboardView.as_view(), name='myaccount'),
    path('myaccount/edit/', AccountUpdateView.as_view(), name='account_edit'),
    path('', HomeView.as_view(), name='home'),
]
