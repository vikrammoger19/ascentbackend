# adminapp/views.py
import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Organization, Product, User, Entities
from .serializers import AdminSerializer, EntitySerializer
from django.db.models import CharField
from django.db.models.functions import Cast
import logging
class AdminViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminSerializer

    @action(detail=False, methods=['post'])
    def login(self, request):
        email = request.data.get('email_id')
        password = request.data.get('password')
        admin = User.objects.filter(email_id=email, password=password).first()
        if admin:
            serializer = self.get_serializer(admin)
            return Response(serializer.data)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['put'])
    def assign_entities(self, request, pk=None):
        admin = self.get_object()
        entity_ids = request.data.get('entity_ids', [])
        entities = Entity.objects.filter(id__in=entity_ids)
        admin.assigned_entities = ','.join(map(str, entities.values_list('id', flat=True)))
        admin.save()
        return Response({'message': 'Entities assigned successfully!'})

class EntityViewSet(viewsets.ModelViewSet):
    queryset = Entities.objects.all()
    serializer_class = EntitySerializer



import json
import re

logger = logging.getLogger(__name__)

def get_organization_products(request, user_id):
    try:
        # Fetch the user from the User model
        user = get_object_or_404(User, user_id=user_id)
        print(f"Fetched user: {user}")  # Debugging print
        logger.info(f"Fetched user: {user}")  # Log the user info

        # Get the raw assigned_entities (stored as a JSON/text field)
        assigned_entities_str = user.assigned_entities or "[]"
        print(f"Assigned entities (raw): {assigned_entities_str}")  # Debugging print
        logger.info(f"Assigned entities (raw): {assigned_entities_str}")  # Log raw assigned_entities

        # Preprocess the assigned_entities string to make it valid JSON (add quotes around entity IDs)
        assigned_entities_str = re.sub(r'([A-Za-z0-9_]+)', r'"\1"', assigned_entities_str)
        print(f"Preprocessed assigned entities: {assigned_entities_str}")  # Debugging print
        logger.info(f"Preprocessed assigned entities: {assigned_entities_str}")  # Log preprocessed entities

        try:
            # Parse the assigned_entities field (now should be valid JSON)
            assigned_entities = json.loads(assigned_entities_str)
            print(f"Assigned entities (parsed): {assigned_entities}")  # Debugging print
            logger.info(f"Assigned entities (parsed): {assigned_entities}")  # Log parsed entities
        except json.JSONDecodeError:
            print(f"Error decoding JSON: {assigned_entities_str}")  # Debugging print
            logger.error(f"Error decoding JSON: {assigned_entities_str}")  # Log error
            return JsonResponse({'status': 'error', 'message': 'Invalid assigned_entities format'}, status=400)

        # Convert assigned_entities to strings for filtering in queries
        assigned_entities = [str(entity_id) for entity_id in assigned_entities]
        print(f"Converted assigned entities to strings: {assigned_entities}")  # Debugging print
        logger.info(f"Converted assigned entities to strings: {assigned_entities}")  # Log string conversion

        # Fetch all entities assigned to the user (ensure the entity_id is a string)
        entities = Entities.objects.annotate(
            entity_id_str=Cast('entity_id', CharField())
        ).filter(entity_id_str__in=assigned_entities)
        print(f"Fetched entities: {entities}")  # Debugging print
        logger.info(f"Fetched entities: {entities}")  # Log entities
        
        # Get the unique organization IDs associated with the fetched entities
        organization_ids = entities.values_list('organization_id', flat=True).distinct()
        print(f"Fetched unique organization IDs: {organization_ids}")  # Debugging print
        logger.info(f"Fetched unique organization IDs: {organization_ids}")  # Log org IDs

        # Fetch organizations based on these unique organization IDs
        organizations = Organization.objects.filter(organization_id__in=organization_ids)
        print(f"Fetched organizations: {organizations}")  # Debugging print
        logger.info(f"Fetched organizations: {organizations}")  # Log organizations

        # List to hold the product details
        products = []

        # Loop through organizations to fetch the products
        for org in organizations:
            # Fetch related products using ManyToManyField
            product_ids = org.products.all()  # This will fetch related Product objects
            print(f"Organization: {org.name}, Product IDs: {[product.product_id for product in product_ids]}")  # Debugging print
            logger.info(f"Organization: {org.name}, Product IDs: {[product.product_id for product in product_ids]}")  # Log product IDs

            # Fetch the corresponding products from the Product table using the product IDs
            if product_ids:
                products_queryset = Product.objects.filter(product_id__in=[product.product_id for product in product_ids])
                print(f"Fetched products: {products_queryset}")  # Debugging print
                logger.info(f"Fetched products: {products_queryset}")  # Log products

                for product in products_queryset:
                    products.append({
                        'product_id': product.product_id,
                        'product_name': product.name,
                        'organization': org.name,
                    })
            else:
                print(f"No products associated with organization: {org.name}")  # Debugging print
                logger.info(f"No products associated with organization: {org.name}")  # Log no products

        print(f"Fetched products: {products}")  # Debugging print
        logger.info(f"Fetched products: {products}")  # Log fetched products

        # Return the products as a JSON response
        return JsonResponse({'status': 'success', 'products': products}, status=200)

    except Exception as e:
        print(f"Error occurred: {str(e)}")  # Debugging print
        logger.error(f"Error occurred: {str(e)}")  # Log error
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
