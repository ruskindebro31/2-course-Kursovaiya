from django.urls import path
from django.views.generic import RedirectView

from apps.catalog.views import ProductDetailView

app_name = "catalog"

urlpatterns = [
    path("", RedirectView.as_view(pattern_name="core:home", permanent=False), name="product_list"),
    path(
        "category/<slug:category_slug>/",
        RedirectView.as_view(pattern_name="core:home", permanent=False),
        name="products_by_category",
    ),
    path("<slug:slug>/", ProductDetailView.as_view(), name="product_detail"),
]
