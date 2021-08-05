from django.contrib import admin
from rango.models import Category, Page, Product
from rango.models import UserProfile

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Product, ProductAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url','views')

admin.site.register(Page, PageAdmin)


admin.site.register(UserProfile)