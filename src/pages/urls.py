from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('films/', views.films, name='films'),
    path('customers/', views.customers, name='customers'),
    path('rentals/', views.rentals, name='rentals'),
    path('stores/', views.stores, name='stores'),
    path('payments/', views.payments, name='payments')
]
