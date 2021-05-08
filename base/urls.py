from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="home"),
	path("products/", views.all_products, name="products"),
	path("products/category/<str:cat>/", views.some_products, name="some_products"),
	path("products/<str:id>/", views.collection_products, name="collection_products"),
	path("products/<str:id>/category/<str:cat>/", views.some_collection_products, name="some_collection_products"),
	path("product/<int:pk>/", views.single_product, name="product"),
	path("contact/", views.contact, name="contact"),
	path("collections/", views.collections, name="collections"),
]