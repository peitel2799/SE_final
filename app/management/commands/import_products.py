import json
import requests
from io import BytesIO
from django.core.files import File
from django.core.management.base import BaseCommand
from app.models import Type, LandHouse, Apartment
import os

class Command(BaseCommand):
    help = 'Import products from JSON file'

    def handle(self, *args, **kwargs):
        # Đường dẫn file JSON
        json_file = 'app/products.json'

        # Đọc file JSON
        with open(json_file, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            # Tạo hoặc lấy Type
            real_estate_type, _ = Type.objects.get_or_create(name=item['Loại hình'])

            # Tải ảnh từ URL và lưu vào MEDIA_ROOT
            response = requests.get(item['images'])
            img_name = os.path.basename(item['images'])
            if response.status_code == 200:
                img_data = BytesIO(response.content)
            else:
                self.stderr.write(f"Could not download image: {item['images']}")
                continue

            # Phân loại theo `Loại hình` và tạo sản phẩm tương ứng
            if real_estate_type.name == 'Nhà đất':
                product, created = LandHouse.objects.get_or_create(
                    title=item['title'],
                    defaults={
                        'address': item['address'],
                        'price': item.get('Giá thỏa thuận'),
                        'price_per_sqm': item.get('Giá theo m2'),
                        'description': item.get('Mô tả'),
                        'real_estate_type': real_estate_type,
                        'floors': item.get('Số tầng'),
                        'total_floor_area': item.get('Tổng diện tích sàn'),
                        'land_area': item.get('Diện tích đất'),
                        'frontage': item.get('Mặt tiền'),
                        'frontage_direction': item.get('Hướng mặt tiền'),
                        'road_width': item.get('Độ rộng đường/ngõ tiếp giáp mặt tiền'),
                        'distance_to_main_road': item.get('Khoảng cách BĐS ra trục chính'),
                    }
                )
            elif real_estate_type.name == 'Chung cư':
                product, created = Apartment.objects.get_or_create(
                    title=item['title'],
                    defaults={
                        'address': item['address'],
                        'price': item.get('Giá thỏa thuận'),
                        'price_per_sqm': item.get('Giá theo m2'),
                        'description': item.get('Mô tả'),
                        'real_estate_type': real_estate_type,
                        'bedrooms': item.get('Số phòng ngủ'),
                        'usable_area': item.get('Diện tích thông thủy'),
                        'balcony_direction': item.get('Hướng ban công'),
                        'delivery_status': item.get('Tình trạng bàn giao'),
                        'location_in_building': item.get('Vị trí căn'),
                        'bathrooms': item.get('Số phòng vệ sinh'),
                        'view': item.get('Tầm nhìn'),
                        'floor_range': item.get('Khoảng tầng'),
                        'project': item.get('Dự án'),
                        'furniture_status': item.get('Tình trạng nội thất'),
                        'furniture_included': item.get('Nội thất đi kèm'),
                        'sub_area': item.get('Phân khu'),
                        'building': item.get('Toà/Dãy nhà'),
                    }
                )
            else:
                self.stderr.write(f"Unknown type: {real_estate_type.name}")
                continue

            # Gắn ảnh vào sản phẩm
            product.image.save(img_name, File(img_data), save=True)
            product.save()

        self.stdout.write(self.style.SUCCESS('Products imported successfully!'))
