from django.shortcuts import get_object_or_404, render
from django_datatables_view.base_datatable_view import BaseDatatableView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse
import numpy as np

from .models import Product, Category, Product_Classification

class IndexView(generic.ListView):
    template_name = 'sprigs/index.html'

    def get_queryset(self):
        """
        Return the category options
        """
        return Category.objects.exclude(category__isnull=True).exclude(category__exact='None').distinct('category')

class OrderListJson(BaseDatatableView):

    # The model we're going to show
    model = Product
    # define the columns that will be returned
    columns = ['product_name', 'sale_price', 'start_date']
    order_columns = ['product_name', 'sale_price', 'start_date']
    max_display_length = 50

    def get_initial_queryset(self):
        selected_option = self.request.GET.get('category')
        classification_lookup = Product_Classification.objects.filter(classification__exact=selected_option).values("product_id")
        return (Product.objects.filter(flyer_id__in=classification_lookup).values("product_name", "sale_price", "start_date").distinct())

    def render_column(self, row, column):
        return super(OrderListJson, self).render_column(row, column)

        #TODO: generate visuals / graph. Use Matplotlib? Bokeh? Plotly?

class ResultsView(generic.View):
    def get(self, request):
        return render(request, 'sprigs/results.html')
