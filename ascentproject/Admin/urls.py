from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminViewSet, EntityViewSet

router = DefaultRouter()
router.register(r'admins', AdminViewSet)
router.register(r'entities', EntityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
