from django.contrib import admin
from parler.admin import TranslatableAdmin, TranslatableInlineModelAdmin, TranslatableTabularInline
from django.utils.translation import gettext as _
from .models import ( 
    Info, Category, Product, Image,
    Contact, ShopImage, Collection,
)


class ProductImageInline(admin.TabularInline):
    model = Image
    extra = 5


@admin.register(Info)
class InfoAdmin(TranslatableAdmin):
    fieldsets = (
    (None, {
        'fields': ('phone', 'instagram', 'telegram', 'facebook')
            }),
    (_('Multilangual informations'), {
        'fields': ('address',),
            }),
    )


@admin.register(Product)
class ProductAdmin(TranslatableAdmin, admin.ModelAdmin):
    list_display = ("id","name", "category", "collection", "is_new", "is_top")

    list_filter = ("date_changed", "collection", "category")

    fieldsets = (
    (None, {
        'fields': ('price', 'category', 'is_new', 'is_top', 'collection')
            }),
    
    (_('Multilangual informations'), {
        'fields': ('name', 'description', 'extra_prices'),
            }),
    )
    inlines = (ProductImageInline,)


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin):
    list_display = ("id", "name")
    fieldsets = (
        (None, {
        'fields': ('image',)
            }),

        (_('Multilangual informations'), {
        'fields': ('name',),
            }),
        )


@admin.register(Collection)
class CollectionAdmin(TranslatableAdmin):
    list_display = ("id", "name")

    fieldsets = (
        
        (None, {
        'fields': ('image',)
            }),

        (_('Multilangual informations'), {
        'fields': ('name', 'blog_text'),
            }),
        )


@admin.register(Image)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "alt", "date")
    list_filter = ("date",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "phone", "message")
    list_filter = ("date",)
    readonly_fields = ('name', "phone", "subject", "message")

@admin.register(ShopImage)
class ShopImageAdmin(admin.ModelAdmin):
    list_display = ("alt", "id")
