from cgitb import lookup
from django.urls import path, include
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)

products_routers = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_routers.register('reviews', views.ReviewViewSet,basename='products-reviews')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='carts-items')
urlpatterns = router.urls + products_routers.urls + carts_router.urls