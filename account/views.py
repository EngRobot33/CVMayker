from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone

from .forms import *
from .models import *

import xlwt


def index(request):
    return render(request, 'cvmaker/index.html')


@login_required
def panel(request):
    jobseekers = JobSeeker.objects.all().order_by('first_name', 'last_name')
    return render(request, 'cvmaker/panel.html', {'jobseekers': jobseekers})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(request,
                                username=form.cleaned_data['username'],
                                password=form.cleaned_data['password']
                                )

            if user is not None:
                if user.is_active:
                    auth_login(request, user)

                    return redirect('account:panel')
                else:
                    return redirect('account:index')
        else:
            return render(request, 'cvmaker/login.html', {'form': form})
    else:
        form = LoginForm()

    return render(request, 'cvmaker/login.html', {'form': form})


@login_required
def logout(request):
    auth_logout(request)
    return redirect('account:index')


@login_required
def export_excel(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Job-seekers' + \
        str(timezone.now()) + '.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Job-seekers')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['First Name', 'Last Name', 'E-mail', 'Phone Number', 'Skills', 'Projects']

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    font_style = xlwt.XFStyle()

    rows = JobSeeker.objects.values_list(
        'first_name', 'last_name', 'email', 'phone_number', 'skills__title', 'project__title'
    )

    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]), font_style)

    wb.save(response)

    return response


@login_required()
def search_result(request):
    if request.method == "POST":
        searched = request.POST['searched']
        jobseekers = JobSeeker.objects.filter(Q(first_name__icontains=searched)|
                                              Q(last_name__icontains=searched)|
                                              Q(email__icontains=searched)|
                                              Q(phone_number__icontains=searched)|
                                              Q(skills__title__icontains=searched)|
                                              Q(project__title__icontains=searched)
                                              ).distinct()
        return render(request, 'cvmaker/search_result.html', {'searched': searched, 'jobseekers': jobseekers})
    else:
        return render(request, 'cvmaker/search_result.html', {})


@login_required()
def sort(request, field):
    jobseekers = JobSeeker.objects.all().order_by(field)
    return render(request, 'cvmaker/panel.html', {'jobseekers': jobseekers})
