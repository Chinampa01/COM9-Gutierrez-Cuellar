# capa de vista/presentación

from django.shortcuts import redirect, render
from .layers.services import services
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def index_page(request):
    return render(request, 'index.html')

# esta función obtiene 2 listados que corresponden a las imágenes de la API y los favoritos del usuario, y los usa para dibujar el correspondiente template.
# si el opcional de favoritos no está desarrollado, devuelve un listado vacío.
def home(request):
    images = services.getAllImages()
    favourite_list = services.getAllFavourites(request) if request.user.is_authenticated else []
    return render(request, 'home.html', { 'images': images, 'favourite_list': favourite_list })

def search(request):
    search_msg = request.POST.get('query', '')
    # si el texto ingresado no es vacío, trae las imágenes y favoritos desde services.py,
    # y luego renderiza el template (similar a home).
    if (search_msg != ''):
        images = services.getAllImages(search_msg)  # Filtra imágenes según el término
        favourite_list = []
        return render(request, 'home.html', {'images': images, 'favourite_list': favourite_list})
    else:
        return redirect('home')


# Estas funciones se usan cuando el usuario está logueado en la aplicación.
@login_required
def getAllFavouritesByUser(request):
    favourite_list = services.getAllFavourites(request)
    return render(request, 'favourites.html', { 'favourite_list': favourite_list })

@login_required
def saveFavourite(request):
    services.saveFavourite(request)
    return redirect(home)

@login_required
def deleteFavourite(request,fav_id):
    # Llama a la capa de servicios para eliminar el favorito con el ID proporcionado
    services.deleteFavourite(fav_id)  # Pasa fav_id directamente
    return redirect('favoritos')  # Redirige a la página de favoritos después de eliminar

@login_required
def exit(request):
    logout(request)
    return redirect(home)