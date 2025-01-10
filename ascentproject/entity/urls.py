# from django.urls import path
# from . import views

# urlpatterns = [
#     path('organizations/', views.organization_list, name='organization_list'),
#     path('entities/', views.entity_list, name='entity_list'),
#     path('entities/<int:pk>/', views.entity_detail, name='entity_detail'),
#     path('organizations/', views.create_organization, name='create_organization'),
#     path('entities/', views.create_entity, name='create_entity'),
# ]
from django.urls import path
from . import views

urlpatterns = [
    path('organizations/', views.OrganizationViewSet.as_view({'get': 'list'}), name='organization-list'),
    path('entities/', views.EntityViewSet.as_view({'get': 'list'}), name='entity-list'),
    path('organizations/<int:organization_id>/entities/', views.EntityViewSet.as_view({'get': 'list'}), name='organization-entities'),
    
]
