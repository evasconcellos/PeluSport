from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Perfil, Review, Contacto, Producto


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)
    direccion = forms.CharField(max_length=255, required=False)
    telefono = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'direccion', 'telefono']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['direccion', 'telefono', 'avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if not avatar.content_type.startswith('image'):
                raise forms.ValidationError('El archivo debe ser una imagen.')
            if avatar.size > 2 * 1024 * 1024:  # 2MB
                raise forms.ValidationError('La imagen no puede superar los 2MB.')
        return avatar



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['texto']


class ContactoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = ['nombre', 'email', 'mensaje']
        widgets = {
            'mensaje': forms.Textarea(attrs={'rows': 4})
        }

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio', 'imagen', 'categoria']
