from api.models import Curso, Profesor, Seccion, Bloque, Requisito
from rest_framework import serializers
from django.contrib.auth.models import User


class CursoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Curso
        fields = ['url', 'nombre', 'id']

class ProfesorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profesor
        fields = ['url', 'nombre']

class SeccionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seccion
        fields = ['url', 'nrc', 'profesor', 'curso']
    
class BloqueSerializer(serializers.HyperlinkedModelSerializer):
    nombre_curso = serializers.CharField(source='seccion.curso.nombre', read_only=True)
    nombre_profesor = serializers.CharField(source='seccion.profesor.nombre', read_only=True)
    nrc = serializers.IntegerField(source='seccion.nrc', read_only=True)
    class Meta:
        model = Bloque
        fields = ['nrc','nombre_curso','nombre_profesor','dia_semana', 'hora_inicio', 'hora_fin', 'tipo', 'fecha_inicio', 'fecha_fin', 'sala']

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

    horarios_protegidos = serializers.ListField(
        child = serializers.DictField(),
        required = False )