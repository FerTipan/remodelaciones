from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Inmueble, Propietario, Reforma, Cotizacion
from django.contrib import messages
from django.db.models import Count


# Create your views here.
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dash')
    return render(request, 'login.html')

def inicio(request):
    inmuebles = Inmueble.objects.all()
    return render(request, 'inicio.html', {'inmuebles': inmuebles})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

def dash(request):
    total_inmuebles = Inmueble.objects.count()
    total_cotizaciones = Cotizacion.objects.count()

    context = {
        'total_inmuebles': total_inmuebles,
        'total_cotizaciones': total_cotizaciones,
    }

    return render(request, 'dash.html', context)

def dashboard1(request):
    return render(request, 'dashboard1.html')

def datos_inmuebles(request):
    inmuebles = Inmueble.objects.values('direccion').annotate(total=Count('id'))
    labels = [item['direccion'] for item in inmuebles]
    data = [item['total'] for item in inmuebles]
    
    return JsonResponse({'labels': labels, 'data': data})

def datos_reformas_cotizaciones(request):
    reformas = Reforma.objects.count()
    cotizaciones = Cotizacion.objects.count()

    return JsonResponse({
        'labels': ['Reformas', 'Cotizaciones'],
        'data': [reformas, cotizaciones]
    })

def nuevo_propietario(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')

        if not nombre or not telefono or not email:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'propietarios/nuevo_propietario.html')
        
        try:
            Propietario.objects.create(
                nombre=nombre,
                telefono=telefono,
                email=email
            )
            messages.success(request, 'Propietario registrado exitosamente.')
            return redirect('lista_propietario')  
        except Exception as e:
            messages.error(request, f'Error al crear el Propietario: {e}')

    return render(request, 'propietarios/nuevo_propietario.html')

def lista_propietario(request):
    propietarios = Propietario.objects.all()
    context = {'propietarios': propietarios, }
    return render(request, 'propietarios/lista_propietario.html', context)

def editar_propietario(request, propietario_id):
    propietario = get_object_or_404(Propietario, id=propietario_id)

    if request.method == "POST":
        propietario.nombre = request.POST.get('nombre')
        propietario.telefono = request.POST.get('telefono')
        propietario.email = request.POST.get('email')

        if not propietario.nombre or not propietario.telefono or not propietario.email:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'propietarios/editar_propietario.html', {'propietario': propietario})

        try:
            propietario.save()
            messages.success(request, 'Propietario actualizado correctamente.')
            return redirect('lista_propietario')
        except Exception as e:
            messages.error(request, f'Error al actualizar el propietario: {e}')
    return render(request, 'propietarios/editar_propietario.html', {'propietario': propietario})

def eliminar_propietario(request, propietario_id):
    propietario = get_object_or_404(Propietario, id=propietario_id)
    if request.method == 'POST':
        propietario.delete()
        messages.success(request, 'Propietario eliminado correctamente.')
    return redirect('lista_propietario')

#------ Inmuebles -----
def nuevo_inmueble(request):
    propietarios = Propietario.objects.all()

    if request.method == "POST":
        propietario_id = request.POST.get('propietario')
        direccion = request.POST.get('direccion')
        foto = request.FILES.get('foto')

        if not propietario_id or not direccion or not foto:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'inmuebles/nuevo_inmueble.html', {'propietarios': propietarios})
        
        propietario = get_object_or_404(Propietario, id=propietario_id)
        
        try:
            Inmueble.objects.create(
                propietario=propietario, 
                direccion=direccion, 
                foto=foto)
            messages.success(request, 'Inmueble registrado exitosamente.')
            return redirect('lista_inmueble')
        except Exception as e:
            messages.error(request, f'Error al crear el Inmueble: {e}')
    return render(request, 'inmuebles/nuevo_inmueble.html', {'propietarios': propietarios})

def lista_inmueble(request):
    inmuebles = Inmueble.objects.all()
    return render(request, 'inmuebles/lista_inmueble.html', {'inmuebles': inmuebles})

def editar_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    propietarios = Propietario.objects.all()
    imagen_anterior = inmueble.foto  

    if request.method == "POST":
        inmueble.propietario_id = request.POST.get('propietario')
        inmueble.direccion = request.POST.get('direccion')

        # Solo actualizar la foto si se ha subido una nueva
        if 'foto' in request.FILES and request.FILES['foto']:
            inmueble.foto = request.FILES['foto']
        else:
            inmueble.foto = imagen_anterior 

        # Validar que los campos obligatorios no estén vacíos
        if not inmueble.propietario_id or not inmueble.direccion:
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'inmuebles/editar_inmueble.html', {'inmueble': inmueble, 'propietarios': propietarios})
        
        try:
            inmueble.save()
            messages.success(request, 'Inmueble actualizado correctamente.')
            return redirect('lista_inmueble')
        except Exception as e:
            messages.error(request, f'Error al actualizar el inmueble: {e}')

    return render(request, 'inmuebles/editar_inmueble.html', {'inmueble': inmueble, 'propietarios': propietarios})

def eliminar_inmueble(request, inmueble_id):
    inmueble = get_object_or_404(Inmueble, id=inmueble_id)
    
    if request.method == "POST":
        inmueble.delete()
        messages.success(request, 'Inmueble eliminado correctamente.')
        return redirect('lista_inmueble')

    return redirect('lista_inmueble')

#------ Reforma -----
def nueva_reforma(request):
    inmuebles = Inmueble.objects.all()

    if request.method == "POST":
        inmueble_id = request.POST.get('inmueble')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        estado = request.POST.get('estado')
        costo_estimado = request.POST.get('costo_estimado').replace(',', '.')

        if not (inmueble_id and descripcion and fecha_inicio and fecha_fin and estado and costo_estimado):
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'reformas/nueva_reforma.html', {'inmuebles': inmuebles})
        
        inmueble = get_object_or_404(Inmueble, id=inmueble_id)
        try:
            Reforma.objects.create(
                inmueble=inmueble, 
                descripcion=descripcion, 
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                estado=estado,
                costo_estimado=float(costo_estimado)
            )
            messages.success(request, 'Reforma registrada exitosamente.')
            return redirect('lista_reforma')
        except Exception as e:
            messages.error(request, f'Error al crear la Reforma: {e}')
    return render(request, 'reformas/nueva_reforma.html', {'inmuebles': inmuebles})

def lista_reforma(request):
    reformas = Reforma.objects.all()
    return render(request, 'reformas/lista_reforma.html', {'reformas': reformas})

def editar_reforma(request, reforma_id):
    reforma = get_object_or_404(Reforma, id=reforma_id)
    inmuebles = Inmueble.objects.all()

    if request.method == "POST":
        inmueble_id = request.POST.get('inmueble', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        fecha_inicio = request.POST.get('fecha_inicio', '').strip()
        fecha_fin = request.POST.get('fecha_fin', '').strip()
        estado = request.POST.get('estado', '').strip()
        costo_estimado = request.POST.get('costo_estimado', '').strip().replace(',', '.')

        if not (inmueble_id and descripcion and fecha_inicio and fecha_fin and estado and costo_estimado):
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'reformas/editar_reforma.html', {'reforma': reforma, 'inmuebles': inmuebles})
        
        try:
            costo_estimado = float(costo_estimado)
        except ValueError:
            messages.error(request, 'El costo estimado debe ser un número válido.')
            return render(request, 'reformas/editar_reforma.html', {'reforma': reforma, 'inmuebles': inmuebles})
        
        try:
            reforma.inmueble_id = inmueble_id
            reforma.descripcion = descripcion
            reforma.fecha_inicio = fecha_inicio
            reforma.fecha_fin = fecha_fin
            reforma.estado = estado
            reforma.costo_estimado = costo_estimado
            reforma.save()

            messages.success(request, 'Reforma actualizada correctamente.')
            return redirect('lista_reforma')
        except Exception as e:
            messages.error(request, f'Error al actualizar la reforma: {e}')

    return render(request, 'reformas/editar_reforma.html', {'reforma': reforma, 'inmuebles': inmuebles})

def eliminar_reforma(request, reforma_id):
    reforma = get_object_or_404(Reforma, id=reforma_id)
    
    if request.method == "POST":
        reforma.delete()
        messages.success(request, 'Reforma eliminada correctamente.')
        return redirect('lista_reforma')

    return redirect('lista_reforma')

#------ Cotizaciones -----
def listado_cotizaciones(request):
    cotizaciones = Cotizacion.objects.all()
    return render(request, 'cotizaciones/listado_cotizacion.html', {'cotizaciones': cotizaciones})

def nueva_cotizacion(request):
    reformas = Reforma.objects.all()

    if request.method == "POST":
        reforma_id = request.POST.get('reforma')
        proveedor = request.POST.get('proveedor')
        monto = request.POST.get('monto')
        aceptada = request.POST.get('aceptada') == "on"
        fecha = request.POST.get('fecha')

        if not (reforma_id and proveedor and monto and fecha):
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'cotizaciones/nueva_cotizacion.html', {'reformas': reformas})
       
        reforma = get_object_or_404(Reforma, id=reforma_id)

        try:
            Cotizacion.objects.create(
                reforma=reforma, 
                proveedor=proveedor, 
                monto=monto, 
                aceptada=aceptada, 
                fecha=fecha
            )
            messages.success(request, 'Cotización registrada exitosamente.')
            return redirect('listado_cotizacion')
        except Exception as e:
            messages.error(request, f'Error al registrar la cotización: {e}')

    return render(request, 'cotizaciones/nueva_cotizacion.html', {'reformas': reformas})

def editar_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)
    reformas = Reforma.objects.all()

    if request.method == "POST":
        reforma_id = request.POST.get('reforma', '').strip()
        proveedor = request.POST.get('proveedor', '').strip()
        monto = request.POST.get('monto', '').strip()
        fecha = request.POST.get('fecha', '').strip()
        aceptada = request.POST.get('aceptada') == "on"

        if not (reforma_id and proveedor and monto and fecha):
            messages.error(request, 'Todos los campos son obligatorios.')
            return render(request, 'cotizaciones/editar_cotizacion.html', {'cotizacion': cotizacion, 'reformas': reformas})

        try:
            cotizacion.reforma_id = reforma_id
            cotizacion.proveedor = proveedor
            cotizacion.monto = monto
            cotizacion.aceptada = aceptada
            cotizacion.fecha = fecha
            cotizacion.save()
            messages.success(request, 'Cotización actualizada correctamente.')
            return redirect('listado_cotizacion')
        except Exception as e:
            messages.error(request, f'Error al actualizar la cotización: {e}')

    return render(request, 'cotizaciones/editar_cotizacion.html', {'cotizacion': cotizacion, 'reformas': reformas})

def eliminar_cotizacion(request, cotizacion_id):
    cotizacion = get_object_or_404(Cotizacion, id=cotizacion_id)

    if request.method == "POST":
        cotizacion.delete()
        messages.success(request, 'Cotización eliminada correctamente.')
        return redirect('listado_cotizacion')

    return render(request, 'cotizaciones/listado_cotizacion.html')