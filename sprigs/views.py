from django.views import generic
from .models import Product, Category, Product_Classification

class IndexView(generic.ListView):
    template_name = 'sprigs/index.html'

    def get_queryset(self):
        """
        Return the category options
        """
        return Category.objects.exclude(category__isnull=True).exclude(category__exact='None').distinct('category')

class ResultsView(generic.ListView):

    template_name = 'sprigs/results.html'
    context_object_name = 'results'

    def get_queryset(self):
        selected_option = self.request.GET.get('category')
        classification_lookup = Product_Classification.objects.filter(classification__exact=selected_option).values("product_id")
        results = Product.objects.filter(flyer_id__in=classification_lookup).values("product_name", "sale_price", "start_date").distinct()
        return results

        #TODO: generate visuals / graph. Use Matplotlib? Bokeh? Plotly?
