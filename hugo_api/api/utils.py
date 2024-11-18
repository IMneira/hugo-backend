import pandas as pd
from api.models import Curso, Profesor, Seccion, Bloque

def get_data_from_excel(excel_file, header=13):
    df = pd.read_excel(excel_file, header=header)

    # mapeo días de la semana
    dias_semana = {
        'LUNES': 1,
        'MARTES': 2,
        'MIERCOLES': 3,
        'JUEVES': 4,
        'VIERNES': 5,
    }

    for index, row in df.iterrows():
        # agregar curso
        curso, created = Curso.objects.get_or_create(
            nombre=row['TITULO'],
            defaults={
                'creditos': 6,  # implementar en el futuro
                'especialidad': row['AREA'] 
            }
        )

        # agregar profesor 
        profesor, created = Profesor.objects.get_or_create(
            nombre=row['PROFESOR']
        )

        # agregar seccion 
        seccion, created = Seccion.objects.get_or_create(
            nrc=row['NRC'],
            defaults={'profesor': profesor, 'curso': curso}
        )

        # agregar bloque
        for dia, dia_numero in dias_semana.items():
            if pd.notna(row[dia]):  # solo si el día tiene horario
                try:
                    hora_inicio, hora_fin = row[dia].split('-')
                except ValueError:
                    print(f"Error en el horario para {row['TITULO']} el {dia}")
                    continue
                
                bloque, created = Bloque.objects.get_or_create(
                    dia_semana=dia_numero,
                    hora_inicio=hora_inicio.strip(),
                    hora_fin=hora_fin.strip(),
                    seccion=seccion,
                    tipo=row['TIPO DE REUNIÓN'],
                    fecha_inicio=row['INICIO'],
                    fecha_fin=row['FIN'],
                    sala = row['SALA'],
                    
                )
                

    return "Datos procesados correctamente."
