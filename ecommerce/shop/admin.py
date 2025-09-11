from django.contrib import admin
from . models import (Customer,Product,ProductImage,Color,Size,Cart,OrderPlaced)

# Register your models here.
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display =['id', 'user', 'name', 'division','district','thana','street_address','zipcode']

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'selling_price',
        'discounted_price',
        'description',
        'brand',
        'category',
        'product_image',
        'display_additional_images',
        'display_sizes',
        'display_colors',
    ]

    def display_additional_images(self, obj):
        return ", ".join([img.color for img in obj.additional_images.all()])
    display_additional_images.short_description = "Additional Images"

    def display_sizes(self, obj):
        return obj.sizes if obj.sizes else "-"
    display_sizes.short_description = "Sizes"

    def display_colors(self, obj):
        return obj.colors if obj.colors else "-"
    display_colors.short_description = "Colors"

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'color', 'image']
    

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user','product','quantity']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customer','product','quantity','ordered_date','status']


