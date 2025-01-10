# urls.py
from django.urls import path
from .views import create_role, get_roles, get_role, update_role, delete_role

urlpatterns = [
    path('roles/getroles', get_roles, name='get_roles'),  # GET all roles with products
    path('roles/addroles', create_role, name='create_role'),  # POST to create a new role
    path('roles/<int:pk>/', get_role, name='get_role'),  # GET single role by ID
    path('roles/update/<int:pk>/', update_role, name='update_role'),  # PUT to update role
    path('roles/delete/<int:pk>/', delete_role, name='delete_role'),  # DELETE to remove a role
]
