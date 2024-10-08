from rest_framework import viewsets, permissions
from api.models import Curso, Profesor, Seccion, Bloque, Requisito
from api.serializers import CursoSerializer, ProfesorSerializer, SeccionSerializer, BloqueSerializer, RequisitoSerializer

class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    #permission_classes = [permissions.IsAuthenticated]


class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    #permission_classes = [permissions.IsAuthenticated]

class SeccionViewSet(viewsets.ModelViewSet):
    queryset = Seccion.objects.all()
    serializer_class = SeccionSerializer
    #permission_classes = [permissions.IsAuthenticated]

class BloqueViewSet(viewsets.ModelViewSet):
    queryset = Bloque.objects.all()
    serializer_class = BloqueSerializer
    #permission_classes = [permissions.IsAuthenticated]

class RequisitoViewSet(viewsets.ModelViewSet):
    queryset = Requisito.objects.all()
    serializer_class = RequisitoSerializer
    #permission_classes = [permissions.IsAuthenticated]




