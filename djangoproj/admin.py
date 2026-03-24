from django.contrib import admin
from carsapp.models import CarMake, CarModel

# 1. Cấu hình hiển thị CarModel lồng trong CarMake (Inline)
# Giúp bạn thêm nhiều dòng xe ngay khi đang tạo hãng xe
class CarModelInline(admin.TabularInline):
    model = CarModel
    extra = 1

# 2. Cấu hình quản trị cho CarMake (Hãng xe)
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name']
    inlines = [CarModelInline]

# 3. Cấu hình quản trị cho CarModel (Dòng xe)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'year', 'car_make')
    list_filter = ['type', 'year', 'car_make']
    search_fields = ['name']

# 4. Đăng ký các Model với hệ thống Admin
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)