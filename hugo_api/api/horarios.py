from api.models import Curso, Bloque, Seccion
import itertools



def get_combinaciones_de_secciones(cursos_ids):
    secciones_por_curso = []

    for curso_id in cursos_ids:
        curso = Curso.objects.get(id=curso_id)
        secciones = Seccion.objects.filter(curso=curso)
        secciones_por_curso.append(secciones)

    # obtener todas las combinaciones de secciones, tomando una sección por curso
    combinaciones = list(itertools.product(*secciones_por_curso))

    return combinaciones

def hay_solapamiento(combinacion):
    #combinacion es una lista de secciones (objetos de la clase Seccion)
    pass

def usa_horario_protegido(combinacion, horarios_protegidos):
    #combinacion es una lista de secciones (objetos de la clase Seccion)
    pass


def get_horarios(cursos_ids, permite_solapamiento, horarios_protegidos = None):
    combinaciones = get_combinaciones_de_secciones(cursos_ids)

    horarios = []

    for combinacion in combinaciones:
        if not permite_solapamiento:
            if hay_solapamiento(combinacion):
                continue
        
        if horarios_protegidos != None:
            if usa_horario_protegido(combinacion, horarios_protegidos):
                continue


        horario = []
        for seccion in combinacion:
            bloques = seccion.bloques.all()
            horario.append(bloque for bloque in bloques) #falta que el bloque se agregue con la información que queremos usar y en el formato que queremos
        
        horarios.append(horario)

        
        

    return horarios


