from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.utils.translation import gettext as _
from . import functions as func
from . import forms, models

# getting an absolute path without language code
def get_path(request):
    return request.get_full_path()[3:]


# home page 
def index(request):
    info = models.Info.objects.first()
    images = models.ShopImage.objects.all()
    products = models.Product.objects.all()[:8]
    categories = models.Category.objects.all()
    collections = models.Collection.objects.all()

    context = {
        "info": info,
        "images": images,
        "products": products,
        "collections": collections,
        "categories": categories,
    }
    context["collections"] = models.Collection.objects.all()
    context["path"] = get_path(request)
    return render(request, "base/index.html", context)



# all products page
def all_products(request):
    categories = models.Category.objects.all()
    products = models.Product.objects.order_by("-date_changed")
    paginator = Paginator(products, 100)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    context={
        "products": paged_products,
    }

    context["categories"] = categories
    context["collections"] = models.Collection.objects.all()
    context["path"] = get_path(request)
    context["info"] = models.Info.objects.first()

    return render(request, "base/products.html", context)


# products in special category
def some_products(request, cat):
    category = get_object_or_404(models.Category, id=cat)
    products = models.Product.objects.filter(category=category).order_by("-date_changed")

    pagination = Paginator(products, 100)
    page = request.GET.get('page')
    paged_products = pagination.get_page(page)

    context = {"products": paged_products, "category": category}
    context["categories"] = models.Category.objects.all()
    context["collections"] = models.Collection.objects.all()
    context["path"] = get_path(request)
    context["info"] = models.Info.objects.first()

    return render(request, "base/products.html", context)

# single product
def single_product(request, pk):
    categories = models.Category.objects.all()
    product = get_object_or_404(models.Product, id=pk)
    recommendations = func.recommendations(models.Product, 4, product)
    
    context = {"product": product, "recommendations": recommendations, "categories": categories}
    context["collections"] = models.Collection.objects.all()
    context["path"] = get_path(request)
    context["info"] = models.Info.objects.first()

    return render(request, "base/product.html", context)


# products in spesific collection
def collection_products(request, id):
    products = models.Product.objects.filter(collection__id=id).order_by("-date_changed")
    collection = models.Collection.objects.get(id=id)

    pagination = Paginator(products, 50)
    page = request.GET.get('page')
    paged_products = pagination.get_page(page)

    
    context = {
        "products": paged_products,
        "collection": collection,

    }

    context["categories"] = models.Category.objects.all()
    context["collections"] = models.Collection.objects.all()
    context["path"] = get_path(request)
    context["info"] = models.Info.objects.first()

    return render(request, "base/collection_products.html", context)


# collection products in special category
def some_collection_products(request, id, cat):
    products = models.Product.objects.filter(collection__id=id)
    category = get_object_or_404(models.Category, id=cat)
    products = models.Product.objects.filter(category=category).order_by("-date_changed")
    collection = models.Collection.objects.get(id=id)

    pagination = Paginator(products, 50)
    page = request.GET.get('page')
    paged_products = pagination.get_page(page)

    
    context = {
        "category": category,
        "products": paged_products,
        "collection": collection,

    }

    context["categories"] = models.Category.objects.all()
    context["collections"] = models.Collection.objects.all()
    context["path"] = get_path(request)
    context["info"] = models.Info.objects.first()

    return render(request, "base/collection_products.html", context)



# contact
def contact(request):
    context = {}
    var = False
    categories = models.Category.objects.all()
    form = forms.ContactForm()

    if request.method == "POST":
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            form.save()
            var = True
            form = forms.ContactForm()

    context["form"] = form
    context["var"] = var
    context["categories"] = categories
    context["collections"] = models.Collection.objects.all()
    context["path"] = get_path(request)
    context["info"] = models.Info.objects.first()

    return render(request, "base/contact.html", context)


# collections page
def collections(request):
    session = models.Collection.objects.all()
    categories = models.Category.objects.all()
    context = {
        "categories": categories,
        "session": session,
    }
    context["collections"] = models.Collection.objects.all()
    context["path"] = get_path(request)
    context["info"] = models.Info.objects.first()
    
    return render(request, "base/newsletter.html", context)

