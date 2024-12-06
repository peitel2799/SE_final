# from django.shortcuts import render
# from app.models import Category , Product
# # Create your views here.


# def Mater(request):
#     return render(request ,'master.html')

# def Index(request):
#     category = Category.objects.all()
#     product = Product.objects.all()
#     categoryID = request.GET.get('category')
#     if categoryID:
#         product = Product.objects.filter(sub_category = categoryID).order_by('-id')
#     else:
#         product = Product.objects.all()
#     context = {
#         'category' : category,
#         'product' : product,
#     }
#     return render(request , 'index.html' , context)

from django.shortcuts import render
from app.models import Type, Product, LandHouse, Apartment, Product
import random
def Mater(request):
    return render(request ,'master.html')
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
        'products': products,
    }
    return render(request, 'index.html', context)