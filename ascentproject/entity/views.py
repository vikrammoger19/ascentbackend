# # entity/views.py

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Entities
# from .serializers import EntitySerializer, EntityCreateUpdateSerializer


# class EntityListCreateView(APIView):
#     def get(self, request):
#         entities = Entities.objects.all()
#         serializer = EntitySerializer(entities, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = EntityCreateUpdateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class EntityDetailView(APIView):
#     def get(self, request, pk):
#         try:
#             entity = Entities.objects.get(pk=pk)
#             serializer = EntitySerializer(entity)
#             return Response(serializer.data)
#         except Entities.DoesNotExist:
#             return Response({"error": "Entity not found"}, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, pk):
#         try:
#             entity = Entities.objects.get(pk=pk)
#             serializer = EntityCreateUpdateSerializer(entity, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         except Entities.DoesNotExist:
#             return Response({"error": "Entity not found"}, status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request, pk):
#         try:
#             entity = Entities.objects.get(pk=pk)
#             entity.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         except Entities.DoesNotExist:
#             return Response({"error": "Entity not found"}, status=status.HTTP_404_NOT_FOUND)


# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from .models import Organization, Entities
# from .serializers import OrganizationSerializer, EntitySerializer

# @api_view(['GET'])
# def organization_list(request):
#     organizations = Organization.objects.all()  # Query all organizations
#     serializer = OrganizationSerializer(organizations, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def entity_list(request):
#     entities = Entities.objects.all()  # Query all entities
#     serializer = EntitySerializer(entities, many=True)
#     return Response(serializer.data)

# @api_view(['GET'])
# def entity_detail(request, pk):
#     try:
#         entity = Entities.objects.get(pk=pk)  # Query a specific entity by primary key
#     except Entities.DoesNotExist:
#         return Response({'error': 'Entity not found'}, status=404)
    
#     serializer = EntitySerializer(entity)
#     return Response(serializer.data)

# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from rest_framework import status
# from .models import Organization, Entities
# from .serializers import OrganizationSerializer, EntitySerializer, EntityCreateUpdateSerializer

# @api_view(['POST'])
# def create_organization(request):
#     if request.method == 'POST':
#         serializer = OrganizationSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()  # Save the new organization
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def create_entity(request):
#     if request.method == 'POST':
#         serializer = EntityCreateUpdateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()  # Save the new entity
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework import viewsets
# from .models import Organization, Entities
# from .serializers import OrganizationSerializer, EntitySerializer

# class OrganizationViewSet(viewsets.ModelViewSet):
#     queryset = Organization.objects.all()
#     serializer_class = OrganizationSerializer

# class EntityViewSet(viewsets.ModelViewSet):
#     queryset = Entities.objects.all()
#     serializer_class = EntitySerializer
from rest_framework import viewsets
from .models import Organization, Entities
from .serializers import OrganizationSerializer, EntitySerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

# class EntityViewSet(viewsets.ModelViewSet):
#     queryset = Entities.objects.all()
#     serializer_class = EntitySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Organization, Entities
from .serializers import EntitySerializer
from rest_framework import viewsets
from rest_framework.exceptions import NotFound

class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entities.objects.all()
    serializer_class = EntitySerializer

    def get_queryset(self):
        queryset = Entities.objects.all()
        organization_id = self.request.query_params.get('organization_id', None)
        if organization_id is not None:
            queryset = queryset.filter(organization_id=organization_id)
        return queryset

    @action(detail=True, methods=['get'], url_path='entities-by-org')
    def entities_by_org(self, request, pk=None):
        # Get the organization ID from the URL (pk)
        organization_id = pk
        # Check if the organization exists
        try:
            organization = Organization.objects.get(organization_id=organization_id)
        except Organization.DoesNotExist:
            raise NotFound("Organization not found.")
        
        # Get the entities related to this organization
        entities = Entities.objects.filter(organization=organization)
        serializer = EntitySerializer(entities, many=True)
        return Response(serializer.data)
