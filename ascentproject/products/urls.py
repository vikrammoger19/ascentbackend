from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, RoleViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'roles', RoleViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
