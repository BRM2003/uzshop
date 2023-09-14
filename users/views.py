from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import *

# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file
from .forms import *
from .models import Admins
from goods.models import *
from claims.models import *


def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
        print(form)
        return redirect(form)
    else:
        form = SignupForm()
    response = {'form': form}
    return render(request, 'authenticate/sign_up.html', response)

def login_user(request):
    response = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            page_return = request.POST['page_return']
            if page_return == '':
                if Admins.objects.filter(user=user).exists():
                    page_return = 'control'
                else:
                    page_return = '/shop'
            return redirect(page_return)
        else:
            messages.success(request, "Error")
            return render(request, 'authenticate/login.html', {'error': 'Username or Password is incorrect'})
    else:
        response['page_return'] = request.GET.get('page_return', '')
        print(response['page_return'])
    return render(request, 'authenticate/login.html', response)


#: ['M07am6RspHW8jDY1eowGFF9PnQ58UR7aruebkwSnreioBDq1B1JvTgu7Ru2bQsvQ']


@permission_classes([IsAuthenticated])
def control_page(request):
    response = {}
    try:

        if Admins.objects.filter(user=request.user).exists():

            if request.method == 'POST':
                pr_category = GoodsCategory.objects.get(id=request.POST['category'])
                form = GoodsForm(request.POST, request.FILES)
                if form.is_valid():
                    product = Goods.objects.create(title=request.POST['title'],
                                                   category=pr_category,
                                                   description=request.POST['description'],
                                                   amount=request.POST['amount'],
                                                   price_for_admin=request.POST['price_for_admin'],
                                                   currency='UZS',
                                                   photo=request.FILES['photo'],
                                                   cr_by=request.user)
                    product.save()
            response['form'] = GoodsForm()
            admin = Admins.objects.get(user=request.user)
            response['admin'] = admin
            response['count_of_orders'] = len(Orders.objects.all())
            # response['categories'] = GoodsCategory.objects.all()
        else:
            response['error'] = 100
            response['message'] = "you don't have access"
    except Exception as e:
        print(str(e))
    return render(request, 'admin/main.html', response)


@csrf_exempt
@permission_classes([IsAuthenticated])
def orders_page(request):
    response = {}
    try:
        if request.method == 'GET':
            orders_filter = request.GET.get('filter', '')
            search_by_id = request.GET.get('searchById', '')
            search_by_phone = request.GET.get('searchByPhone', '')
            if search_by_phone != '':
                response['orders'] = Orders.objects.filter(user__phone_number__search=search_by_phone)
            elif search_by_id != '':
                response['orders'] = Orders.objects.filter(order_id=search_by_id)
            elif orders_filter != '':
                response['orders'] = Orders.objects.filter(status=orders_filter)
            else:
                response['orders'] = Orders.objects.all()
            response['count_of_orders'] = len(response['orders'])
            print(response['orders'])
            print(response['count_of_orders'])
        else:
            print(request.POST)
    except Exception as e:
        response['success'] = False
        response['error_message'] = str(e)
    return render(request, 'admin/orders.html', response)