from django.urls import path
from .views import LoginView, LogoutView, HomeView
from api.views import DocumentsView


urlpatterns = [
    # Login / sign up screen
    path('login/', LoginView.as_view(), name='account_login'),
    path('', LoginView.as_view(), name='account_login'),
    # Logout of the account
    path('logout/', LogoutView.as_view(), name='account_logout'),
    # Home view for users who logged in successfuly
    path('dashboard/', DocumentsView.as_view(), name='home'),
]