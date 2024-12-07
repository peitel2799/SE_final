from django.shortcuts import render, redirect, HttpResponse
from app.models import Type, Product, Contact_us, LandHouse, Apartment
from django.contrib.auth import authenticate, login, logout
from app.models import UseCreateForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
import random

def Master(request):
    return render(request, 'master.html')

def Index(request):
    types = Type.objects.all()
    type_id = request.GET.get('real_estate_type')
    
    # Lọc sản phẩm theo loại hình
    if type_id:
        land_houses = LandHouse.objects.filter(real_estate_type_id=type_id).order_by('-id')
        apartments = Apartment.objects.filter(real_estate_type_id=type_id).order_by('-id')
    else:
        land_houses = LandHouse.objects.all().order_by('-id')
        apartments = Apartment.objects.all().order_by('-id')
    
    # Kết hợp cả hai loại sản phẩm
    products = list(land_houses) + list(apartments)
    random.shuffle(products)
    context = {
        'types': types,
        'products': products[:9],
    }
    return render(request, 'index.html', context)

def signup(request):
    if request.method == 'POST':
        form = UseCreateForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['password1'],
            )
            login(request , new_user)
            return redirect('index')
    else:
        form = UseCreateForm()
    
    context = {
        'form': form,
    }
    return render(request , 'registration/signup.html' , context)


def custom_logout(request):
    logout(request)
    return redirect('index')

@login_required(login_url="/accounts/login/")
def cart_add(request , id):
    cart = Cart(request)
        
    # Lọc sản phẩm theo loại hình
    product = LandHouse.objects.filter(id = id).first()
    if product is None:
        product = Apartment.objects.filter(id = id).first()
    
    #product = Product.objects.get(id = id)
    cart.add(product= product)
    return redirect('index')


@login_required(login_url="/accounts/login/")
def item_clear(request , id):
    cart = Cart(request)
    product = LandHouse.objects.filter(id = id).first()
    if product is None:
        product = Apartment.objects.filter(id = id).first()
    cart.remove(product)
    return redirect('cart_detail')

""" @login_required(login_url="/accounts/login/")
def item_increment(request , id):
    cart = Cart(request)
    product = LandHouse.objects.filter(id = id).first()
    if product is None:
        product = Apartment.objects.filter(id = id).first()
    cart.add(product= product)
    return redirect('cart_detail') """

""" @login_required(login_url="/accounts/login/")
def item_decrement(request , id):
    cart = Cart(request)
    product = LandHouse.objects.filter(id = id).first()
    if product is None:
        product = Apartment.objects.filter(id = id).first()
    cart.decrement(product= product)
    return redirect('cart_detail') """

@login_required(login_url="/accounts/login/")
def cart_clear(request ):
    cart = Cart(request)
    cart.clear()
    return redirect('cart_detail')

@login_required(login_url="/accounts/login/")
def car_detail(request):
    return render(request , 'cart/cart_detail.html')

def Contact_Page(request):
    if request.method == "POST":
        contact = Contact_us(
            name = request.POST.get('name'),
            email = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )
        contact.save()
    return render(request, 'contact.html')

# def CheckOut(request):
#     if request.method == "POST":
#         address = request.POST.get('address')
#         phone = request.POST.get('phone')
#         pincode = request.POST.get('pincode')
#         cart = request.session.get('cart')
#         uid = request.session.get('_auth_user_id')
#         user = User.objects.get(pk=uid)
#         for i in cart:
#             a = int(cart[i]['price'])
#             b = cart[i]['quantity']
#             total = a*b
#             order = Order(
#                 user = user,
#                 product = cart[i]['name'],
#                 price = cart[i]['price'],
#                 quantity = cart[i]['quantity'],
#                 image = cart[i]['image'],
#                 address = address,
#                 phone = phone,
#                 pincode = pincode,
#                 total = total
#             )
#             order.save()
#         request .session['cart'] = {}
#         return redirect("index")
#     return HttpResponse('This is checkout page')

# def Your_Order(requset):
#     uid = requset.session.get('_auth_user_id')
#     user = User.objects.get(pk=uid)
#     order = Order.objects.filter(user = user)
#     context = {
#         "order": order,
#     }
#     return render(requset, 'order.html', context)

# def Product_page(request):
#     # Lấy danh sách các loại hình bất động sản
#     types = Type.objects.all()

#     # Lấy giá trị loại hình từ URL query parameter
#     typeID = request.GET.get('real_estate_type')

#     # Lọc sản phẩm theo loại hình, nếu được chọn
#     if typeID:
#         # Kiểm tra loại hình nào được chọn
#         selected_type = Type.objects.get(id=typeID)
#         if selected_type.name == 'Nhà đất':
#             products = LandHouse.objects.all().order_by('-id')
#         elif selected_type.name == 'Chung cư':
#             products = Apartment.objects.all().order_by('-id')
#         else:
#             products = []  # Không có sản phẩm nào nếu loại hình không hợp lệ
#     else:
#         # Nếu không lọc, lấy toàn bộ sản phẩm
#         products = list(LandHouse.objects.all()) + list(Apartment.objects.all())

#     context = {
#         'types': types,  # Truyền danh sách loại hình vào context
#         'products': products,  # Truyền danh sách sản phẩm vào context
#     }
#     return render(request, 'product.html', context)
from django.core.paginator import Paginator

def Product_page(request):
    # Lấy danh sách các loại hình bất động sản
    types = Type.objects.all()

    # Lấy giá trị loại hình từ URL query parameter
    typeID = request.GET.get('real_estate_type')

    # Lọc sản phẩm theo loại hình, nếu được chọn
    if typeID:
        selected_type = Type.objects.get(id=typeID)
        if selected_type.name == 'Nhà đất':
            products = LandHouse.objects.all().order_by('-id')
        elif selected_type.name == 'Chung cư':
            products = Apartment.objects.all().order_by('-id')
        else:
            products = []  # Không có sản phẩm nào nếu loại hình không hợp lệ
    else:
        # Nếu không lọc, lấy toàn bộ sản phẩm
        products = list(LandHouse.objects.all()) + list(Apartment.objects.all())
        # products = sorted(products, key=lambda x: x.id, reverse=True)  # Sort all products by id
        random.shuffle(products)

    # Add pagination
    paginator = Paginator(products, 9)  # Show 9 products per page
    page_number = request.GET.get('page')  # Get the current page number from the query string
    page_obj = paginator.get_page(page_number)  # Get the corresponding page

    context = {
        'types': types,        # Truyền danh sách loại hình vào context
        'products': page_obj,  # Pass the paginated products (page_obj) into context
    }
    return render(request, 'product.html', context)


def Product_Detail(request):
    product = Product.objects.filter(id = id).first()
    context = {
        'product': product
    }
    return render(request, 'product_detail.html', context)

def Search(request):
    query = request.GET['query']
    
    product = Product.objects.filter(name_icontains = query)
    context = {
        'product': product
    }
    
    return render(request, 'search.html', context)