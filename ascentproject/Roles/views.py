# views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Role
from .serializers import RoleSerializer

@api_view(['GET'])
def get_roles(request):
    """
    Retrieve all roles.
    """
    roles = Role.objects.all()
    serializer = RoleSerializer(roles, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def create_role(request):
    """
    Create a new role.
    """
    serializer = RoleSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_role(request, pk):
    """
    Retrieve a single role by ID.
    """
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RoleSerializer(role)
    return Response(serializer.data)

@api_view(['PUT'])
def update_role(request, pk):
    """
    Update an existing role by ID.
    """
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = RoleSerializer(role, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def delete_role(request, pk):
    """
    Delete a role by ID.
    """
    try:
        role = Role.objects.get(pk=pk)
    except Role.DoesNotExist:
        return Response({'detail': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    role.delete()
    return Response({'detail': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
