from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_my_orders, name="my_orders"),
    path("add", views.add_order, name="add_order"),
    path("cancel/<int:pk>", views.cancel_order, name="cancel_order"),
]
