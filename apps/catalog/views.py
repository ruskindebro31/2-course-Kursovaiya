from django.views.generic import DetailView

from apps.catalog.models import Product


class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.filter(is_active=True).select_related("category")
