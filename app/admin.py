# from django.contrib import admin
# from .models import Category, Contact_us, Sub_Category, Product, Contact_us, Order, Brand
# # Register your models here.

# admin.site.register(Category)
# admin.site.register(Sub_Category)
# admin.site.register(Product)
# admin.site.register(Order)
# admin.site.register(Contact_us)
# admin.site.register(Brand)
from django.contrib import admin
from .models import LandHouse, Apartment, Type, Product
admin.site.register(Type)
# admin.site.register(Product)
# Register for LandHouse
@admin.register(LandHouse)
class LandHouseAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'price', 'real_estate_type', 'created_at')
    search_fields = ('title', 'address')
    list_filter = ('real_estate_type', 'created_at', 'frontage_direction')
    ordering = ('-created_at',)

# Register for Apartment
@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'address', 'price', 'real_estate_type', 'created_at')
    search_fields = ('title', 'address', 'project')
    list_filter = ('real_estate_type', 'created_at', 'balcony_direction', 'furniture_status')
    ordering = ('-created_at',)