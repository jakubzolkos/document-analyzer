from django.urls import path
from .views import LoginView, LogoutView,HomeView


urlpatterns = [
    # Login / sign up screen
    path('login/', LoginView.as_view(), name='account_login'),
    # Logout of the account
    path('logout/', LogoutView.as_view(), name='account_logout'),
    # Home view for users who logged in successfuly
    path('', HomeView.as_view(), name='home'),
]