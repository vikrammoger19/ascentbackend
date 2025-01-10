from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminViewSet, EntityViewSet
from . import views
router = DefaultRouter()
router.register(r'admins', AdminViewSet)
router.register(r'entities', EntityViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('products/<str:user_id>/', views.get_organization_products, name='get_organization_products'),
]
