from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.decorators.cache import never_cache
from .views import SignUpView

urlpatterns = [
    path('login/', never_cache(auth_views.LoginView.as_view(template_name='registration/login.html')), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]