from .views import create_user
from . import views
from django.urls import path
# router = DefaultRouter()
# router.register(r'users', UserViewSet)
# router.register(r'entities', EntitiesViewSet)
# router.register(r'organizations', OrganizationViewSet)
# router.register(r'products', ProductViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('user/authenticate/',views.authenticate_user , name='authenticate_user'),
    path('user/create/', views.create_user, name='create_user'),
    path('user/fetchall/', views.fetch_all_users, name='fetch_all_users'),
    path('user/<str:user_id>/', views.get_user, name='get_user'),
    path('user/reset_password/', views.reset_password, name='reset_password'),
    path('user/assign_entities/<str:user_id>/', views.assign_entities_to_user, name='assign_entities_to_user'), 
    path('user/update/<str:user_id>/', views.update_user, name='update_user'),
    path('user/delete/<str:user_id>/', views.delete_user, name='delete_user'),
    
]