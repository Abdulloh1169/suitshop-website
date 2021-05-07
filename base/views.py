from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
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
    key_for_category = "all"
    categories = models.Category.objects.all()

    products = models.Product.objects.all()
    category = request.GET.get("category")

    if category:
        products = set(products.filter(category__translations__name=category))
        key_for_category = category

    context={
        "current_type": key_for_category,
        "products": products,
        "categories": categories,
    }
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
    products = models.Product.objects.filter(collection__id=id)
    category = request.GET.get("category")
    categories = models.Category.objects.all()
    collection = models.Collection.objects.get(id=id)

    if category:
        products = set(products.filter(category__translations__name=category))
        key_for_category = category
    
    context = {
        "categories": categories,
        "key": category,
        "products": products,
        "collection": collection,

    }

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

