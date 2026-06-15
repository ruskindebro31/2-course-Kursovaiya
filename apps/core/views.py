from django.views.generic import TemplateView

from apps.catalog.models import Product


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["products"] = (
            Product.objects.filter(is_active=True).select_related("category").order_by("-created_at")
        )
        return context
