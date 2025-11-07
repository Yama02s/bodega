from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Prestamo, Docente, Material

# Formulario que tiene el Pañol para registrar prestamos

class PrestamoForm(forms.ModelForm):
    docente = forms.ModelChoiceField(
        queryset=Docente.objects.filter(activo=True)
    )
    material = forms.ModelChoiceField(
        queryset=Material.objects.filter(activo=True)
    )

    class Meta:
        model = Prestamo
        fields = ['docente', 'material', 'cantidad']

    def clean_cantidad(self):
        cantidad = self.cleaned_data.get('cantidad')
        material = self.cleaned_data.get('material')
        
        if cantidad <= 0:
            raise forms.ValidationError("La cantidad debe ser mayor a cero.")
        
        if material and cantidad > material.stock:
            raise forms.ValidationError(f"No hay suficiente stock. Stock actual: {material.stock}")
            
        return cantidad

# --- Formularios de Admin (CRUD Personalizado) ---

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = ['nombre', 'apellido', 'rut', 'email', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'rut': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['nombre', 'descripcion', 'stock', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

# Formulario para crear usuarios
class CustomUserCreationForm(UserCreationForm):
    
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Rol (Grupo)"
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'grupo',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['grupo'].widget.attrs.update({'class': 'form-select'})
        for field in ['username', 'first_name', 'last_name', 'email']:
             self.fields[field].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            grupo = self.cleaned_data.get('grupo')
            user.groups.add(grupo)
        return user

# Formulario para EDITAR usuarios (Admin/Pañol)
class CustomUserChangeForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        label="Rol (Grupo)"
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'grupo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['grupo'].initial = self.instance.groups.first()

        self.fields['grupo'].widget.attrs.update({'class': 'form-select'})
        for field in self.fields:
            if field != 'is_active':
                self.fields[field].widget.attrs.update({'class': 'form-control'})
            else:
                self.fields[field].widget.attrs.update({'class': 'form-check-input'})

    def save(self, commit=True):
        user = super().save(commit=False)
        grupo = self.cleaned_data.get('grupo')
        if commit:
            user.save()
            user.groups.clear() 
            user.groups.add(grupo)
        return user