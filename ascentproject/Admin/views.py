# adminapp/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Entities
from .serializers import AdminSerializer, EntitySerializer

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
