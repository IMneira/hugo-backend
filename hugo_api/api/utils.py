import pandas as pd
from api.models import Curso, Profesor, Seccion, Bloque

def get_data_from_excel(excel_file, header=14):
    df = pd.read_excel(excel_file, header=header)

    cursos = []
    profesores = []
    secciones = []
    bloques = []

    # días de la semana presentes en las columnas
    dias_semana = {
        'LUNES': 1,
        'MARTES': 2,
        'MIERCOLES': 3,
        'JUEVES': 4,
        'VIERNES': 5
    }

    for index, row in df.iterrows():
        # agregar Curso
        curso, created = Curso.objects.get_or_create(
            nombre=row['TITULO'],
            defaults={'creditos': 3}  # -> falta implementar
        )
        cursos.append(curso)

        # agregar profesor
        profesor, created = Profesor.objects.get_or_create(
            nombre=row['PROFESOR']
        )
        profesores.append(profesor)

        # agregar seccion
        seccion = Seccion(
            nrc=row['NRC'],
            profesor=profesor,
            curso=curso,
            especialidad=row['AREA'],
            fecha_inicio=row['INICIO'],
            fecha_fin=row['FIN']
        )
        secciones.append(seccion)

        # procesar los bloques de los días de la semana
        for dia, dia_numero in dias_semana.items():
            if pd.notna(row[dia]):  # solo si el dia tiene horario
                try:
                    hora_inicio, hora_fin = row[dia].split('-')
                except ValueError:
                    print("hubo un error en la obtención del horario")
                    continue
                
                bloque = Bloque(
                    dia_semana=dia_numero,  # número del día
                    hora_inicio=hora_inicio.strip(),
                    hora_fin=hora_fin.strip(),
                    tipo=row['TIPO DE REUNIÓN'],
                    seccion=seccion,
                    fecha=row['INICIO']  # útil en caso de ser prueba
                )
                bloques.append(bloque)

    # insertar en la base de datos

    try:
        Curso.objects.bulk_create(cursos, ignore_conflicts=True)
        Profesor.objects.bulk_create(profesores, ignore_conflicts=True)
        Seccion.objects.bulk_create(secciones)
        Bloque.objects.bulk_create(bloques)

        return True
    
    except Exception as e:

        print(e)
        return False

