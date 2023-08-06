from django.shortcuts import render


def home(request):
    """
    Controller for the app home page.
    """
    context = {}

    return render(request, 'two/home.html', context)