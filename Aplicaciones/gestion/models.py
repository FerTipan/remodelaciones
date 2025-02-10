from django.db import models

class Propietario(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()

    def __str__(self):
        return self.nombre

class Inmueble(models.Model):
    propietario = models.ForeignKey(Propietario, on_delete=models.CASCADE)
    direccion = models.CharField(max_length=200)
    foto = models.FileField(upload_to='evidencias_inmuebles', null=True, blank=True)

    def __str__(self):
        return f"{self.direccion}, {self.propietario}"

class Reforma(models.Model):
    inmueble = models.ForeignKey(Inmueble, on_delete=models.CASCADE)
    descripcion = models.TextField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=50, choices=[('Pendiente', 'Pendiente'), ('En Progreso', 'En Progreso'), ('Finalizado', 'Finalizado')])
    costo_estimado = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Reforma en {self.inmueble.descripcion}"

class Cotizacion(models.Model):
    reforma = models.ForeignKey(Reforma, on_delete=models.CASCADE)
    proveedor = models.CharField(max_length=100)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    aceptada = models.BooleanField(default=False)
    fecha = models.DateField()

    def __str__(self):
        return f"{self.proveedor} - {self.monto}"

