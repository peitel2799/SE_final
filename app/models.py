import datetime
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

# class Category(models.Model):
#     name = models.CharField(max_length=150)

#     def __str__(self):
#         return self.name

# class Sub_Category(models.Model):
#     name = models.CharField(max_length=150)
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name    
    
# class Brand(models.Model):
#     name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

# class Product(models.Model):
#     Availability = (('In stock', 'In stock'),('Out of stock', 'Out of stock'))
#     category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False,default=" ")
#     sub_category = models.ForeignKey(Sub_Category, on_delete=models.CASCADE, null=False, default=" ")
#     brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
#     image = models.ImageField(upload_to='ecommerce/pimage')
#     name = models.CharField(max_length=100)
#     price = models.IntegerField()
#     Availability = models.CharField(max_length=100, choices=Availability, null=True)
#     date = models.DateField(auto_now_add=True)

#     def __str__(self):
#         return self.name
    

class UseCreateForm (UserCreationForm):
    email = forms.EmailField(required= True , label='Email' , error_messages= {'exists' : 'This Email has already existed'})
    
    class Meta:
        model = User
        fields = ['username' , 'email' ,'password1' , 'password2']
        
    def __init__(self, *args, **kwargs):
        super(UseCreateForm , self).__init__(*args, **kwargs)
        
        self.fields['username'].widget.attrs['placeholder'] = 'User Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm password'
        
    def save(self, commit = True):
        user = super(UseCreateForm , self).save(commit = False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    def clean_email(self):
        if User.objects.filter(email = self.cleaned_data['email']).exists():
            raise forms.ValidationError(self.fields['email'].error_messages['exists'])
        return self.cleaned_data['email']
    
class Contact_us(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    

    def __str__(self):
        return self.name
    
# class Order(models.Model):
#     image = models.ImageField(upload_to='ecommer/order/image')
#     product = models.CharField(max_length=1000, default='')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     price = models.IntegerField()
#     # quantity = models.CharField(max_length=5)
#     # total = models.CharField(max_length=10, default='') 

#     address = models.TextField
#     phone = models.CharField(max_length=10)
#     pincode = models.CharField(max_length=10)
#     date = models.DateField(default=datetime.datetime.today())

#     def __str__(self):
#         return self.product.name

from django.db import models

class Type(models.Model):
    """
    Model for Real Estate Type (Nhà đất, Chung cư)
    """
    name = models.CharField(max_length=50, choices=(('Nhà đất', 'Nhà đất'), ('Chung cư', 'Chung cư')), unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Base model for all real estate products
    """
    title = models.CharField(max_length=255)  # Tên sản phẩm
    address = models.CharField(max_length=255)  # Địa chỉ
    price = models.CharField(max_length=50, null=True, blank=True)  # Giá thỏa thuận
    price_per_sqm = models.CharField(max_length=50, null=True, blank=True)  # Giá theo m2
    description = models.TextField(null=True, blank=True)  # Mô tả
    image = models.ImageField(upload_to='ecommerce/pimage', default='images/default.jpg')  # URL hình ảnh
    created_at = models.DateTimeField(auto_now_add=True)  # Ngày thêm
    
    def address_first_part(self):
        print(self.address.split(",")[0] if self.address else "")
        return self.address.split(",")[0] if self.address else ""

    # Liên kết tới bảng loại hình (Nhà đất, Chung cư)
    real_estate_type = models.ForeignKey(Type, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True  # Model này chỉ dùng làm base model

    def __str__(self):
        return self.title


class LandHouse(Product):
    """
    Model for Nhà đất (land house)
    """
    floors = models.CharField(max_length=50, null=True, blank=True)  # Số tầng
    total_floor_area = models.CharField(max_length=50, null=True, blank=True)  # Tổng diện tích sàn
    land_area = models.CharField(max_length=50, null=True, blank=True)  # Diện tích đất
    frontage = models.CharField(max_length=100, null=True, blank=True)  # Mặt tiền
    frontage_direction = models.CharField(max_length=50, null=True, blank=True)  # Hướng mặt tiền
    road_width = models.CharField(max_length=50, null=True, blank=True)  # Độ rộng đường/ngõ
    distance_to_main_road = models.CharField(max_length=100, null=True, blank=True)  # Khoảng cách tới đường chính


class Apartment(Product):
    """
    Model for Chung cư (apartment)
    """
    bedrooms = models.CharField(max_length=50, null=True, blank=True)  # Số phòng ngủ
    usable_area = models.CharField(max_length=50, null=True, blank=True)  # Diện tích thông thủy
    balcony_direction = models.CharField(max_length=50, null=True, blank=True)  # Hướng ban công
    delivery_status = models.CharField(max_length=50, null=True, blank=True)  # Tình trạng bàn giao
    location_in_building = models.CharField(max_length=50, null=True, blank=True)  # Vị trí căn (căn góc, căn giữa)
    bathrooms = models.CharField(max_length=50, null=True, blank=True)  # Số phòng vệ sinh
    view = models.CharField(max_length=100, null=True, blank=True)  # Tầm nhìn
    floor_range = models.CharField(max_length=50, null=True, blank=True)  # Khoảng tầng
    project = models.CharField(max_length=100, null=True, blank=True)  # Dự án
    furniture_status = models.CharField(max_length=50, null=True, blank=True)  # Tình trạng nội thất
    furniture_included = models.CharField(max_length=50, null=True, blank=True)  # Nội thất đi kèm
    sub_area = models.CharField(max_length=100, null=True, blank=True)  # Phân khu
    building = models.CharField(max_length=100, null=True, blank=True)  # Tòa/Dãy nhà
