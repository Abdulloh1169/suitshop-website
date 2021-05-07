from django.db import models
from django.core.exceptions import ValidationError
from parler.models import TranslatableModel, TranslatedFields
from django.utils.translation import gettext as  _
from . import functions as func

"""
All Models

Info, Category, Product, Image, Contact, ShopImage, Collection

"""


# do'kon informatsialari
class Info(TranslatableModel):
    translations = TranslatedFields(
        address = models.CharField(_('address'), max_length=300, null=True)
    )
    
    phone = models.CharField(_('phone number'), max_length=13, validators=[func.phone_validator], null=True,
        help_text = "+998xxxxxxx")
    email = models.EmailField(null=True)
    telegram = models.URLField(blank=True, null=True, help_text=_("this field have to incleude 'http://' or 'https://'"))
    instagram = models.URLField(blank=True, null=True, help_text=_("this field have to incleude 'http://' or 'https://'"))
    facebook = models.URLField(blank=True, null=True, help_text=_("this field have to incleude 'http://' or 'https://'"))

    class Meta:
        verbose_name_plural = _("Info")

    def __str__(self):
        return _("Shop Information")

    def __unicode__(self):
        return _("Shop Information")

    def save(self):
        if Info.objects.count() > 3:
            raise ValidationError(_("you can not have more than one info object"))
        return super().save()


# kategoriya
class Category(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_("category name"), max_length=30, null=True)
    )

    image = models.ImageField(_("category image"), upload_to="category", null=True)

    class Meta:
        verbose_name_plural = _("categories")

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# kollektsialar
class Collection(TranslatableModel):
    translations = TranslatedFields(
        name = models.CharField(_("collection"), max_length=30, null=True),
        blog_text = models.TextField(_("blog text"), null=True, blank=True)
    )
    image = models.ImageField(_("collection image"), upload_to="collections", null=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


# productlar 
class Product(TranslatableModel):
    CHOICES = ((True, "✓"), (False, "✕"))
    translations = TranslatedFields(
        name = models.CharField(_("name"), max_length=30, null=True),
        description = models.CharField(_("description"), max_length=500, null=True, blank=True),
        extra_prices = models.TextField(_("prices"), null=True, blank=True)
    )

    price = models.CharField(_("price"), max_length=30, null=True)
    category = models.ForeignKey(Category, verbose_name=_("category"), on_delete=models.SET_NULL, null=True)
    is_new = models.BooleanField(_("new"), default=False, choices=CHOICES)
    is_top = models.BooleanField(_("top"), default=False, choices=CHOICES)
    collection = models.ForeignKey(Collection, verbose_name=_("collection"), on_delete=models.SET_NULL, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_changed = models.DateTimeField(auto_now=True)

    @property
    def get_prices(self):
        a = list()
        if self.extra_prices is None or self.extra_prices.isspace():
            return ()
        for i in self.extra_prices.split("\n"):
            try:
                i, j = i.split(":")
            except:
                return ()
            a.append((i,j))
        return a

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name



# product rasmlari
class Image(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products', validators=[func.image_validator])
    alt = models.CharField(_("alternative message"), max_length=50, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product)


# do'kon rasmlari | 8ta rasmga mo'ljallangan
class ShopImage(models.Model):
    image = models.ImageField(upload_to="shop", null=True)
    alt = models.CharField(_("alternative message"), max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.alt}-{self.id}"


# admin bilan aloqa
class Contact(models.Model):
    name = models.CharField(max_length=50, null=True)
    phone = models.CharField(max_length=13, validators=[func.phone_validator], null=True)
    subject = models.CharField(max_length=100, null=True)
    message = models.CharField(max_length=500, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):
        if Contact.objects.count() >= 100:
            Contact.objects.last().delete()

        return super().save(*args, **kwargs)
