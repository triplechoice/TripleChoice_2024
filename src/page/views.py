from django.shortcuts import render, get_object_or_404

# Create your views here.
from page.models import Page


def page(request, slug):

    page_obj =  get_object_or_404(Page, slug=slug)
    return render(request, template_name='pages/index.html', context={'page': page_obj})
