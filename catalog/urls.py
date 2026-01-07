from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_products, name="get_products"),
    path("<str:slug>/", views.get_product, name="get_product"),
    path("search", views.search_products, name="search_product"),
    path("", views.list_category, name="list_category"),
    path("<slug:slug>", views.detail_category, name="detail_category"),
]

