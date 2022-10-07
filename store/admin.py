from django.contrib import admin
from django.db.models.aggregates import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse
from .models import Product, Collection, Customer, Order
# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_per_page = 10
    list_select_related = ['collection']
    
    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 50 :
            return 'Low'
        return 'Ok'


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = ( reverse('admin:store_product_changelist')
         + '?' 
         + urlencode({
            'collection__id': str(collection.id)
         }) )
        return  format_html("<a href={}>{}</a>", url , collection.products_count )
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id','placed_at','customer_name']
    list_select_related = ['customer']

    def customer_name(self, order):
        return order.customer
    class Meta:
        ordering = ['first_name', 'last_name']