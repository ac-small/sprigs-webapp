from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.http import HttpResponse

from .models import Product, Category, Product_Classification

class IndexView(generic.ListView):
    template_name = 'sprigs/index.html'

    def get_queryset(self):
        """
        Return the category options
        """
        return Category.objects.exclude(category__isnull=True).exclude(category__exact='None').distinct('category')

# Results view
def run(request):
    selected_option = request.GET['category']
    classification_lookup = Product_Classification.objects.filter(classification__exact=selected_option).values_list()
    products = []
    for i in classification_lookup:
        print ("Product Id:" + str(i[1]))
        products.append(list(Product.objects.filter(flyer_id__exact=i[1]).values_list('product_name', 'sale_price', flat=False)))

    if products == []:
        return HttpResponse("Currently, there is no data for the category selected")
    else:
        return HttpResponse(products,  content_type="application/json", charset="utf-8")
