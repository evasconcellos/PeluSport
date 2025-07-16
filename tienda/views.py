from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import Producto, Categoria, Perfil, Review
from .forms import RegistroForm, PerfilForm, ReviewForm, ContactoForm, UserForm, PerfilForm, ProductoForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash
from django.urls import reverse_lazy

def home(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()
    return render(request, 'home.html', {'productos': productos, 'categorias': categorias})

def detalle_producto(request, pk):
    producto = Producto.objects.get(pk=pk)
    reviews = Review.objects.filter(producto=producto)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            nueva = form.save(commit=False)
            nueva.usuario = request.user
            nueva.producto = producto
            nueva.save()
            return redirect('detalle_producto', pk=pk)
    else:
        form = ReviewForm()
    return render(request, 'productos/detalle.html', {
        'producto': producto, 'reviews': reviews, 'form': form
    })

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Crear perfil con datos adicionales
            direccion = form.cleaned_data.get('direccion')
            telefono = form.cleaned_data.get('telefono')
            Perfil.objects.create(user=user, direccion=direccion, telefono=telefono)

            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'registration/registro.html', {'form': form})


@login_required
def confirmar_compra(request):
    carrito = request.session.get('carrito', {})
    
    if not carrito:
        messages.warning(request, "Tu carrito está vacío.")
        return redirect('ver_carrito')
    
    request.session['carrito'] = {}
    messages.success(request, "Compra confirmada con éxito. ¡Gracias por tu compra!")
    return redirect('home')

def perfil(request):
    return redirect('editar_perfil')


def editar_perfil(request):
    user = request.user
    perfil, _ = Perfil.objects.get_or_create(user=user)

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
    else:
        user_form = UserForm(instance=user)
        perfil_form = PerfilForm(instance=perfil)

    return render(request, 'usuarios/editar_perfil.html', {
        'user_form': user_form,
        'perfil_form': perfil_form
    })

def buscar(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.filter(nombre__icontains=query)
    return render(request, 'productos/buscar.html', {'productos': productos, 'query': query})

def productos_por_categoria(request, categoria_id):
    categoria = Categoria.objects.get(id=categoria_id)
    productos = Producto.objects.filter(categoria=categoria)
    return render(request, 'productos/lista.html', {'productos': productos, 'categoria': categoria})

def agregar_al_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id = str(producto_id)
    carrito[producto_id] = carrito.get(producto_id, 0) + 1
    request.session['carrito'] = carrito
    return redirect('ver_carrito')

def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    producto_ids = [int(id) for id in carrito.keys()]
    productos = Producto.objects.filter(id__in=producto_ids)
    total = sum(producto.precio * carrito[str(producto.id)] for producto in productos)
    return render(request, 'productos/carrito.html', {
        'productos': productos,
        'carrito': carrito,
        'total': total
    })

def quitar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id = str(producto_id)

    if producto_id in carrito:
        del carrito[producto_id]
        request.session['carrito'] = carrito
        messages.info(request, 'Producto eliminado del carrito.')
    
    return redirect('ver_carrito')

def vaciar_carrito(request):
    request.session['carrito'] = {}
    messages.info(request, 'Carrito vaciado correctamente.')
    return redirect('ver_carrito')

class CambiarPasswordView(PasswordChangeView):
    template_name = 'usuarios/cambiar_password.html'
    success_url = reverse_lazy('perfil')

    def form_valid(self, form):
        response = super().form_valid(form)
        update_session_auth_hash(self.request, form.user)  # ← mantiene la sesión
        messages.success(self.request, "Contraseña actualizada correctamente.")
        return response



def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Mensaje enviado correctamente!')
            return redirect('home')
    else:
        form = ContactoForm()
    return render(request, 'productos/contacto.html', {'form': form})

def about(request):
    return render(request, 'about.html')


def es_superuser(user):
    return user.is_superuser

@login_required
@user_passes_test(es_superuser)
def crear_producto(request):
    form = ProductoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'productos/crear_producto.html', {'form': form})

@login_required
@user_passes_test(es_superuser)
def editar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    form = ProductoForm(request.POST or None, request.FILES or None, instance=producto)
    if form.is_valid():
        form.save()
        return redirect('detalle_producto', pk=producto.pk)
    return render(request, 'productos/editar_producto.html', {'form': form, 'producto': producto})

@login_required
@user_passes_test(es_superuser)
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('home')
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})

