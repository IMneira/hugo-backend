from django.db import models

# Create your models here.
class Curso(models.Model):
    nombre = models.CharField(max_length=100)
    creditos = models.IntegerField()
    especialidad = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.nombre
    
class Profesor(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Seccion(models.Model):
    nrc = models.IntegerField(primary_key=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)

    def __str__(self):
        return self.nrc

class Bloque(models.Model):
    dia_semana = models.IntegerField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    seccion = models.ForeignKey(Seccion, on_delete=models.CASCADE, related_name='bloques')
    tipo = models.CharField(max_length=50)
    sala = models.CharField(max_length=20, null=True)
    fecha_inicio = models.DateField(null=True)
    fecha_fin = models.DateField(null=True)

    def __str__(self):
        return self.dia_semana+ ' ' + self.hora_inicio + ' ' + self.hora_fin + ' ' + self.tipo

class Requisito(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='curso_dependiente')
    requisito = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='requisito')

    def __str__(self):
        return self.curso.nombre + ' -> ' + self.requisito.nombre

