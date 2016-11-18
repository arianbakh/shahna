from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'index.html', {})

def login(request):
    pass  # TODO


@login_required
def logout(request):
    pass  # TODO


@login_required
def profile(request):
    pass  # TODO
