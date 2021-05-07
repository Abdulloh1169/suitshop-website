import re
from random import randint
from django.core.exceptions import ValidationError


def phone_validator(phone, obj=None):
    if not bool(re.match("^\+(998)[0-9]{9}$", phone)):
        raise ValidationError("Phone number format is wrong (+998999999999)")


def image_validator(img, obj=None):
    pass
    
    # uncomment below to activate image validator
    #if not (0.9 < img.height/img.width < 1.1):
    #    raise ValidationError(
    #        f"image size should be in 3/4 proportion, this images proportion is{ img.width}/ {img.height}")


def recommendations(queryset, cont, obj):
    if queryset.objects.count() <= cont:
        return list(queryset.objects.all())
    qs = queryset.objects.filter(category=obj.category)
    if qs.count() < cont:
        qs = queryset.objects.all()

    a = list()
    while len(a) < cont:
        i = qs[randint(0, qs.count()-1)]
        if i not in a:
            a.append(i)

    return a





