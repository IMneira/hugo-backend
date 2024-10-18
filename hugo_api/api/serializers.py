from api.models import Curso, Profesor, Seccion, Bloque, Requisito
from rest_framework import serializers
from django.contrib.auth.models import User


class CursoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Curso
        fields = ['url', 'nombre', 'creditos']

class ProfesorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profesor
        fields = ['url', 'nombre']

class SeccionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seccion
        fields = ['url', 'nrc', 'profesor', 'curso', 'especialidad', 'fecha_inicio', 'fecha_fin']
    
class BloqueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bloque
        fields = ['url', 'dia_semana', 'hora_inicio', 'hora_fin', 'seccion', 'tipo', 'fecha']

class RequisitoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Requisito
        fields = ['url', 'curso', 'requisito']

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']


class HorarioSerializer(serializers.Serializer):
    cursos = serializers.ListField(
        child = serializers.IntegerField(),
        required = True )
    
    permite_solapamiento = serializers.BooleanField(required = True)

    horarios_protegidos = serializers.DictField(
        child = serializers.ListField( child = serializers.CharField() ),
        required = False )