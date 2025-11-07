from django.db import models
from django.contrib.auth.models import User

class Docente(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class Material(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre

class Prestamo(models.Model):
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    fecha_prestamo = models.DateTimeField(auto_now_add=True)
    usuario_pañol = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="prestamos_realizados")

    def __str__(self):
        return f"{self.cantidad} de {self.material.nombre} a {self.docente.nombre}"