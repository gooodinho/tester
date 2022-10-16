from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from typing import Union

from .service import *
from .forms import UserLoginForm, UploadFileForm


@login_required(login_url='login')
def main_page_view(request) -> HttpResponse:
    form = UploadFileForm()
    context = {'form': form}
    if request.method == 'POST':
        csv_file = request.FILES['csv_file']
        xml_file = request.FILES['xml_file']
        files_handler(csv_file, xml_file)
    if request.user.is_superuser:
        all_users = User.objects.filter(is_superuser=False)
        context['all_users'] = all_users
    return render(request, 'users/main_page.html', context)


def user_login_view(request) -> Union[HttpResponse, HttpResponseRedirect]:
    if request.method == "POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            if login_user_handler(request):
                return redirect('main_page')
    else:
        form = UserLoginForm()       
    return render(request, 'users/login.html', {'form': form})


@login_required(login_url='login')
def user_logout_view(request) -> HttpResponseRedirect:
    logout_handler(request)
    return redirect('login')
