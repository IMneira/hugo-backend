from rest_framework import viewsets
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from api.models import Curso, Profesor, Seccion, Bloque, Requisito
from django.contrib.auth.models import User
from api.serializers import CursoSerializer, ProfesorSerializer, SeccionSerializer, BloqueSerializer, RequisitoSerializer, UserSerializer, HorarioSerializer
from api.utils import get_data_from_excel
from rest_framework.authtoken.models import Token
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from api.horarios import get_horarios

#--------------------------------ViewSets--------------------------------------
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class CursoViewSet(viewsets.ModelViewSet):
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    #permission_classes = [permissions.IsAuthenticated]
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class ProfesorViewSet(viewsets.ModelViewSet):
    queryset = Profesor.objects.all()
    serializer_class = ProfesorSerializer
    #permission_classes = [permissions.IsAuthenticated]
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class SeccionViewSet(viewsets.ModelViewSet):
    queryset = Seccion.objects.all()
    serializer_class = SeccionSerializer
    #permission_classes = [permissions.IsAuthenticated]
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class BloqueViewSet(viewsets.ModelViewSet):
    queryset = Bloque.objects.all()
    serializer_class = BloqueSerializer
    #permission_classes = [permissions.IsAuthenticated]
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
class RequisitoViewSet(viewsets.ModelViewSet):
    queryset = Requisito.objects.all()
    serializer_class = RequisitoSerializer
    #permission_classes = [permissions.IsAuthenticated]
#--------------------------------ViewSets--------------------------------------



#--------------------------------Upload Excel--------------------------------------
#falta restringir para que solo acceda admin logueado
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def upload_excel(request):
    excel_file = request.FILES.get('file', None)
    
    if excel_file is None:
        return JsonResponse({'error': 'No file provided'}, status=400)
    
    try:
        respuesta = get_data_from_excel(excel_file)
        print(respuesta)

    except Exception as e:
        return JsonResponse({'error inserting data': str(e)}, status=500)

    return JsonResponse({
        'message': 'Data processed successfully',
    })
#--------------------------------Upload Excel--------------------------------------



#-------------------------Sesion de administrador----------------------------------
@api_view(['POST'])
def login(request):
    user = get_object_or_404(User, username=request.data['username'])

    if not user.check_password(request.data['password']):
        return Response({'error': 'Invalid password'}, status=400)

    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)

    return Response({'token': token.key, 'user': serializer.data}, status=200)


@api_view(['POST'])
def register(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])
        user.save()

        token = Token.objects.create(user=user)
    

        return Response({'user': serializer.data, 'token': token.key}, status=201)
    return Response(serializer.errors, status=400)
#-------------------------Sesion de administrador----------------------------------



#-------------------------Obtención de horarios------------------------------------
@api_view(['POST'])
def get_horarios(request):
    serializer = HorarioSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    # obtener los datos
    cursos = serializer.validated_data['cursos']
    permite_solapamiento = serializer.validated_data['permite_solapamiento']
    #horarios_protegidos = serializer.data['horarios_protegidos']

    #horarios = get_horarios([1,2,3], True) #horarios_protegidos)

    horarios = "test"
    # generar horarios

    return Response({'message': 'Horarios generados correctamente', 'data':horarios}, status=200)
#-------------------------Obtención de horarios------------------------------------