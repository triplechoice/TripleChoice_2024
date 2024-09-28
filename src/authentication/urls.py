from django.urls import path, reverse_lazy

from authentication.views import CustomerLoginView, AuthCheckView, CustomerLogoutView, RegistrationView, activateView, \
    UserExists, ApiLoginView, PassWordResetView, AdminPassWordResetView, Profile

app_name = 'authentication'
urlpatterns = [
    path('sign-in/', CustomerLoginView.as_view(), name='login'),
    path('api/check-auth/', AuthCheckView.as_view(), name='auth_check'),
    path('logout/', CustomerLogoutView.as_view(), name='logout'),
    path('create-account/', RegistrationView.as_view(), name='register'),
    path('activate/(<uidb64>[0-9A-Za-z_\-]+)/(<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', activateView,
         name='activate'),
    path('user/profile/', Profile.as_view(), name="user_profile"),
    path('user_exists/', UserExists.as_view(), name='user_exists'),

    path("api/api_login/", ApiLoginView.as_view(), name="api_login"),

    path("password_reset/", PassWordResetView.as_view(), name="password_reset"),
    path("admin_password_reset/", AdminPassWordResetView.as_view(), name="admin_password_reset"),

]
