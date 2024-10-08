from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Curso, Profesor, Seccion, Bloque, Requisito
from api.serializers import CursoSerializer, ProfesorSerializer, SeccionSerializer, BloqueSerializer, RequisitoSerializer
from api.utils import get_data_from_excel

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
class ExcelUploadView(APIView):

    def post(self, request, *args, **kwargs):
        excel_file = request.FILES['file']

        if excel_file:
            inserted = get_data_from_excel(excel_file)
            if inserted:
                return Response(status=status.HTTP_201_CREATED, data={'message': 'Data inserted'})
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'Error inserting data'})

        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'error': 'No file provided'})


