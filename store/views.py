from webbrowser import get
from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import DefaultPagination
from .models import Review, Product, Collection, OrderItem, Cart, CartItem
from .serializers import AddCartItemSerializer, CartItemSerializer, ReviewSerializer, ProductSerializer, CartSerializer, CollectionSerializer, UpdateCartItemSerializer
from .filters import ProductFilter
# Create your views here.

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends =[DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    pagination_class = DefaultPagination
    def get_serializer_context(self):
        return {'request': self.request}

    
    def destroy(self, request, pk, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0 :
            return Response({'error': 'Product cannot be deleted bcz '})
        return super().destroy(request, *args, **kwargs )
    
   

    
class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class =  CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection, pk=pk)
        if collection.products.count() > 0 :
            return Response({'error': 'Product cannot be deleted bcz '})
        collection.delete()
        return Response('Ok')

class ReviewViewSet(ModelViewSet):
   
    serializer_class  = ReviewSerializer
    
    def get_queryset(self):
        return  Review.objects.filter(product_id=self.kwargs['product_pk'])
    

    def get_serializer_context(self):
         return {'product_id': self.kwargs['product_pk']}
    

class CartViewSet(CreateModelMixin, DestroyModelMixin , RetrieveModelMixin,GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer

class CartItemsViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_serializer_context(self, **kwargs):
        return {'cart_id': self.kwargs['cart_pk']}
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
            return CartItem.objects.filter(cart=self.kwargs['cart_pk']).select_related('product')
        