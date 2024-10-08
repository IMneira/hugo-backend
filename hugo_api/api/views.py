from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.models import Curso, Profesor, Seccion, Bloque, Requisito
from api.serializers import CursoSerializer, ProfesorSerializer, SeccionSerializer, BloqueSerializer, RequisitoSerializer
from api.utils import get_data_from_excel
from django.http import JsonResponse

#--------------------------------ViewSets--------------------------------------
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
#--------------------------------ViewSets--------------------------------------


#
@api_view(['POST'])
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

