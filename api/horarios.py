from api.models import Curso, Bloque, Seccion
from api.serializers import BloqueSerializer, SeccionSerializer
import itertools
from datetime import datetime


def get_combinaciones_de_secciones(cursos_ids, cursos_obligatorios_ids, minimo_n_cursos, max_n_creditos):
    # Obtener las secciones de los cursos obligatorios
    secciones_obligatorias = []
    for curso_id in cursos_obligatorios_ids:
        curso = Curso.objects.get(id=curso_id)
        secciones = Seccion.objects.filter(curso=curso)
        secciones_obligatorias.append(secciones)
    
    # Obtener las secciones de los cursos no obligatorios
    cursos_no_obligatorios = [curso_id for curso_id in cursos_ids if curso_id not in cursos_obligatorios_ids]
    secciones_no_obligatorias = []
    for curso_id in cursos_no_obligatorios:
        curso = Curso.objects.get(id=curso_id)
        secciones = Seccion.objects.filter(curso=curso)
        secciones_no_obligatorias.append(secciones)
    
    # Generar combinaciones para las secciones obligatorias (fijas)
    combinaciones_obligatorias = list(itertools.product(*secciones_obligatorias))
    
    # Generar combinaciones de los cursos no obligatorios (tomando de minimo_n_cursos a len(cursos_ids) cursos)
    combinaciones_finales = []
    for r in range(max(0, minimo_n_cursos - len(cursos_obligatorios_ids)), len(cursos_no_obligatorios) + 1):
        combinaciones_no_obligatorias = itertools.combinations(secciones_no_obligatorias, r)
        for combinacion_no_obligatoria in combinaciones_no_obligatorias:
            # Convertir las listas de secciones en combinaciones específicas
            secciones_por_curso = list(itertools.product(*combinacion_no_obligatoria))
            for obligatoria in combinaciones_obligatorias:
                for opcional in secciones_por_curso:
                    combinaciones_finales.append(obligatoria + opcional)
    
    return combinaciones_finales

def hay_solapamiento(combinacion):
    dict_bloques = {dia: [] for dia in range(1, 7)}
    for seccion in combinacion:
        for bloque in seccion.bloques.all(): dict_bloques[bloque.dia_semana].append(bloque)
    for bloques in dict_bloques.values():
        n = len(bloques)
        if n > 1:
            bloques.sort(key=lambda b: b.hora_inicio)
            for i in range(n - 1):
                bloque_i = bloques[i]
                for j in range(i + 1, n):
                    bloque_j = bloques[j]
                    if bloque_i.seccion != bloque_j.seccion:
                        solapan_horas = (bloque_i.hora_inicio < bloque_j.hora_fin and bloque_j.hora_inicio < bloque_i.hora_fin)
                        solapan_fechas = (bloque_i.fecha_inicio < bloque_j.fecha_fin and bloque_j.fecha_inicio < bloque_i.fecha_fin)
                        if solapan_horas and solapan_fechas: return True
    return False




def usa_horario_protegido(combinacion, horarios_protegidos):
    for seccion in combinacion:
        for bloque in seccion.bloques.all():
            for horario_protegido in horarios_protegidos:
                print(horario_protegido["dia_de_semana"])
                if bloque.dia_semana == horario_protegido['dia_de_semana']:
                
                    bloque_hora_inicio = bloque.hora_inicio
                    bloque_hora_fin = bloque.hora_fin
                    protegido_hora_inicio = datetime.strptime(horario_protegido['hora_inicio'], '%H:%M').time()
                    protegido_hora_fin = datetime.strptime(horario_protegido['hora_fin'], '%H:%M').time()
                    print(protegido_hora_fin)
                    
                    solapan_horas = (bloque_hora_inicio < protegido_hora_fin and protegido_hora_inicio < bloque_hora_fin)

                    if solapan_horas:
                        return True

    return False


def generate_horarios(cursos_ids, permite_solapamiento, minimo_n_cursos, cursos_obligatorios_ids, max_n_creditos, horarios_protegidos = None):
    combinaciones = get_combinaciones_de_secciones(cursos_ids, cursos_obligatorios_ids, minimo_n_cursos, max_n_creditos)

    horarios = []

    for combinacion in combinaciones:
        if not permite_solapamiento:
            if hay_solapamiento(combinacion):
                continue
        
        if len(horarios_protegidos) != 0:
            if usa_horario_protegido(combinacion, horarios_protegidos):
                continue


        horario = []
        for seccion in combinacion:
            bloques = seccion.bloques.all()
            #horario.append(bloque for bloque in bloques) #falta que el bloque se agregue con la información que queremos usar y en el formato que queremos
            for bloque in bloques:
                serializer = BloqueSerializer(bloque)
                horario.append(serializer.data)
        horarios.append(horario)

        
        

    return horarios





