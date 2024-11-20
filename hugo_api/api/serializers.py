from api.models import Curso, Profesor, Seccion, Bloque, Requisito
from rest_framework import serializers
from django.contrib.auth.models import User


class CursoSerializer(serializers.HyperlinkedModelSerializer):
    nombre = serializers.CharField(max_length=100)
    creditos = serializers.IntegerField()
    especialidad = serializers.CharField(max_length=100, required=False)
    class Meta:
        model = Curso
        fields = ['id', 'nombre', 'creditos', 'especialidad']

class ProfesorSerializer(serializers.HyperlinkedModelSerializer):
    nombre = serializers.CharField(max_length=100)
    class Meta:
        model = Profesor
        fields = ['id','nombre']

class SeccionSerializer(serializers.HyperlinkedModelSerializer):
    nrc = serializers.IntegerField()
    profesor = serializers.PrimaryKeyRelatedField(queryset=Profesor.objects.all())
    curso = serializers.PrimaryKeyRelatedField(queryset=Curso.objects.all())
    class Meta:
        model = Seccion
        fields = ['nrc', 'profesor', 'curso']
    
class BloqueSerializer(serializers.HyperlinkedModelSerializer):
    seccion = serializers.PrimaryKeyRelatedField(queryset=Seccion.objects.all())
    dia_semana = serializers.IntegerField()
    hora_inicio = serializers.TimeField()
    hora_fin = serializers.TimeField()
    tipo = serializers.CharField(max_length=50)
    sala = serializers.CharField(max_length=20, allow_null=True)
    fecha_inicio = serializers.DateField(allow_null=False)
    fecha_fin = serializers.DateField(allow_null=False)

    #solo lectura, no para la creación de instancias
    nrc = serializers.IntegerField(source='seccion.nrc', read_only=True)
    nombre_curso = serializers.CharField(source='seccion.curso.nombre', read_only=True)
    nombre_profesor = serializers.CharField(source='seccion.profesor.nombre', read_only=True)
    
    class Meta:
        model = Bloque
        fields = ['id','nrc','nombre_curso','nombre_profesor','dia_semana', 'hora_inicio', 'hora_fin', 'tipo', 'fecha_inicio', 'fecha_fin', 'sala', 'seccion']

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
    
    cursos_obligatorios = serializers.ListField(
        child = serializers.IntegerField(),
        required = True )
    
    minimo_n_cursos = serializers.IntegerField(required = True)

    permite_solapamiento = serializers.BooleanField(required = True)

    max_n_creditos = serializers.IntegerField(required = True)

    horarios_protegidos = serializers.ListField(
        child = serializers.DictField(),
        required = False )