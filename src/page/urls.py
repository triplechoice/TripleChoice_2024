from django.urls import path

from page.views import page

urlpatterns = [
    path('<str:slug>/', page)
]
