from page.models import Website


def website(request):
       info = Website.objects.first()
       return { "site": info }
