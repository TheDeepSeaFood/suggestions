from .models import Brand


def brand_name(request):
    try:
        brand = Brand.objects.first()
        return {"brand_name": brand.name if brand else "OpiniNest"}
    except Brand.DoesNotExist:
        return {"brand_name": "OpiniNest"}
