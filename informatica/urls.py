from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Vistas de los usuarios que tienen rol Pañol
    path('prestamo/nuevo/', views.registrar_prestamo, name='registrar_prestamo'),
    path('prestamo/listado/', views.listar_prestamos, name='listar_prestamos'),

    # Vista de los administradores
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # CRUD de los Docentes
    path('admin/docentes/', views.listar_docentes, name='admin_listar_docentes'),
    path('admin/docentes/nuevo/', views.crear_docente, name='admin_crear_docente'),
    path('admin/docentes/editar/<int:pk>/', views.editar_docente, name='admin_editar_docente'),
    path('admin/docentes/eliminar/<int:pk>/', views.eliminar_docente, name='admin_eliminar_docente'),
    
    # CRUD de materiales
    path('admin/materiales/', views.listar_materiales, name='admin_listar_materiales'),
    path('admin/materiales/nuevo/', views.crear_material, name='admin_crear_material'),
    path('admin/materiales/editar/<int:pk>/', views.editar_material, name='admin_editar_material'),
    path('admin/materiales/eliminar/<int:pk>/', views.eliminar_material, name='admin_eliminar_material'),

    # CRUD de los usuarios
    path('admin/usuarios/', views.listar_usuarios, name='admin_listar_usuarios'),
    path('admin/usuarios/nuevo/', views.crear_usuario, name='admin_crear_usuario'),
    path('admin/usuarios/editar/<int:pk>/', views.editar_usuario, name='admin_editar_usuario'),
    path('admin/usuarios/eliminar/<int:pk>/', views.eliminar_usuario, name='admin_eliminar_usuario'),
]