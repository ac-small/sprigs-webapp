from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic


from .models import Product, Category, Product_Classification

class IndexView(generic.ListView):
    template_name = 'sprigs/index.html'

    def get_queryset(self):
        """
        Return the category options
        """
        return Category.objects.exclude(category__isnull=True).exclude(category__exact='None').distinct('category')