from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="home"),
	path("products/", views.all_products, name="products"),
	path("products/<str:id>/", views.collection_products, name="collection_products"),
	path("product/<int:pk>/", views.single_product, name="product"),
	path("contact/", views.contact, name="contact"),
	path("collections/", views.collections, name="collections"),
]