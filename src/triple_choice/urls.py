"""triple_choice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from triple_choice import settings
from django.contrib.auth import views as auth_views

admin.site.site_header = settings.APP_SITE_HEADER
admin.site.site_title = settings.APP_SITE_TITLE
admin.site.index_title = settings.APP_INDEX_TITLE

urlpatterns = [
    path('tinymce/', include('tinymce.urls')),
    path('super-admin/', admin.site.urls),
    path('', include("product.urls")),
    path('', include("order.urls")),
    path('', include("authentication.urls")),
    path('', include("page.urls")),
    path('user/', include("customer.urls")),
    path('supplier/', include("supplier.urls")),
    # path("stripe/", include("djstripe.urls", namespace="djstripe")),
    # path("v1/payment_intents", include("djstripe.urls", namespace="djstripe")),

    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="frontend/authentication/password_reset_done.html"),
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="frontend/authentication/password_reset_confirm.html", ),
         name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="frontend/authentication/password_reset_complete.html"),
         name="password_reset_complete")

]
urlpatterns + static(settings.STATIC_URL)
# urlpatterns += + static(settings.STATIC_URL)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
