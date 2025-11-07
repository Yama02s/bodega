from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Prestamo, Material, Docente
from .forms import (
    PrestamoForm, DocenteForm, MaterialForm, 
    CustomUserCreationForm, CustomUserChangeForm
)
from django.db import transaction
from django.contrib.auth.models import User, Group



# ---- Decoradores de Seguridad  ----
def es_panol(user):
    return user.groups.filter(name='Pañol').exists()

def es_admin(user):
    return user.groups.filter(name='Administrador').exists() or user.is_superuser

# ---- Vistas Comunes ----
@login_required
def home(request):
    """Página de inicio que redirige según el rol."""
    if es_admin(request.user):
        return redirect('admin_dashboard')
    elif es_panol(request.user):
        return redirect('registrar_prestamo')
    else:
        messages.error(request, 'No tienes un rol asignado.')
        return redirect('login')


# La vesta del rol de Pañol 
@login_required
@user_passes_test(es_panol, login_url='home')
def registrar_prestamo(request):
    """(POST) Permite al rol Pañol registrar un préstamo."""
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    prestamo = form.save(commit=False)
                    prestamo.usuario_pañol = request.user
                    material = prestamo.material
                    material.stock -= prestamo.cantidad
                    material.save()
                    prestamo.save()
                    messages.success(request, 'Préstamo registrado exitosamente.')
                    return redirect('listar_prestamos')
            except Exception as e:
                messages.error(request, f'Error al registrar el préstamo: {e}')
    else:
        form = PrestamoForm()
    form.fields['docente'].widget.attrs.update({'class': 'form-select'})
    form.fields['material'].widget.attrs.update({'class': 'form-select'})
    form.fields['cantidad'].widget.attrs.update({'class': 'form-control'})

    return render(request, 'informatica/prestamo_form.html', {'form': form})

@login_required
@user_passes_test(es_panol, login_url='home')
def listar_prestamos(request):
    """(GET) Vista para que el Pañol vea los préstamos realizados."""
    prestamos = Prestamo.objects.all().order_by('-fecha_prestamo')
    return render(request, 'informatica/prestamo_list.html', {'prestamos': prestamos})


# Las vistas CRUD para el Administrador

@login_required
@user_passes_test(es_admin, login_url='home')
def admin_dashboard(request):
    """Dashboard principal para el Administrador."""
    num_docentes = Docente.objects.count()
    num_materiales = Material.objects.count()
    num_panol = User.objects.filter(groups__name='Pañol').count()
    num_admin = User.objects.filter(groups__name='Administrador').count()
    
    context = {
        'num_docentes': num_docentes,
        'num_materiales': num_materiales,
        'num_panol': num_panol,
        'num_admin': num_admin,
    }
    return render(request, 'informatica/admin/admin_dashboard.html', context)

# CRUD de los docentes

@login_required
@user_passes_test(es_admin, login_url='home')
def listar_docentes(request):
    docentes = Docente.objects.all()
    return render(request, 'informatica/admin/docente_list.html', {'docentes': docentes})

@login_required
@user_passes_test(es_admin, login_url='home')
def crear_docente(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Docente creado exitosamente.')
            return redirect('admin_listar_docentes')
    else:
        form = DocenteForm()
    return render(request, 'informatica/admin/docente_form.html', {'form': form, 'accion': 'Crear'})

@login_required
@user_passes_test(es_admin, login_url='home')
def editar_docente(request, pk):
    docente = get_object_or_404(Docente, pk=pk)
    if request.method == 'POST':
        form = DocenteForm(request.POST, instance=docente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Docente actualizado exitosamente.')
            return redirect('admin_listar_docentes')
    else:
        form = DocenteForm(instance=docente)
    return render(request, 'informatica/admin/docente_form.html', {'form': form, 'accion': 'Editar'})

@login_required
@user_passes_test(es_admin, login_url='home')
def eliminar_docente(request, pk):
    docente = get_object_or_404(Docente, pk=pk)
    if request.method == 'POST':
        docente.delete()
        messages.success(request, 'Docente eliminado exitosamente.')
        return redirect('admin_listar_docentes')
    return render(request, 'informatica/admin/confirm_delete.html', {'objeto': docente, 'tipo': 'Docente'})

# CRUD de los materiales

@login_required
@user_passes_test(es_admin, login_url='home')
def listar_materiales(request):
    materiales = Material.objects.all()
    return render(request, 'informatica/admin/material_list.html', {'materiales': materiales})

@login_required
@user_passes_test(es_admin, login_url='home')
def crear_material(request):
    if request.method == 'POST':
        form = MaterialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material creado exitosamente.')
            return redirect('admin_listar_materiales')
    else:
        form = MaterialForm()
    return render(request, 'informatica/admin/material_form.html', {'form': form, 'accion': 'Crear'})

@login_required
@user_passes_test(es_admin, login_url='home')
def editar_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        form = MaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            messages.success(request, 'Material actualizado exitosamente.')
            return redirect('admin_listar_materiales')
    else:
        form = MaterialForm(instance=material)
    return render(request, 'informatica/admin/material_form.html', {'form': form, 'accion': 'Editar'})

@login_required
@user_passes_test(es_admin, login_url='home')
def eliminar_material(request, pk):
    material = get_object_or_404(Material, pk=pk)
    if request.method == 'POST':
        material.delete()
        messages.success(request, 'Material eliminado exitosamente.')
        return redirect('admin_listar_materiales')
    return render(request, 'informatica/admin/confirm_delete.html', {'objeto': material, 'tipo': 'Material'})

# CRUD de los usuarios

@login_required
@user_passes_test(es_admin, login_url='home')
def listar_usuarios(request):
    usuarios = User.objects.filter(is_superuser=False)
    return render(request, 'informatica/admin/usuario_list.html', {'usuarios': usuarios})

@login_required
@user_passes_test(es_admin, login_url='home')
def crear_usuario(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('admin_listar_usuarios')
    else:
        form = CustomUserCreationForm()
    return render(request, 'informatica/admin/usuario_form.html', {'form': form, 'accion': 'Crear'})

@login_required
@user_passes_test(es_admin, login_url='home')
def editar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('admin_listar_usuarios')
    else:
        form = CustomUserChangeForm(instance=usuario)
    return render(request, 'informatica/admin/usuario_form.html', {'form': form, 'accion': 'Editar'})

@login_required
@user_passes_test(es_admin, login_url='home')
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, 'Usuario eliminado exitosamente.')
        return redirect('admin_listar_usuarios')
    return render(request, 'informatica/admin/confirm_delete.html', {'objeto': usuario, 'tipo': 'Usuario'})