import os

import requests
from django.shortcuts import redirect, render
from django.shortcuts import get_object_or_404

from .forms import MovieForm
from .models import Movie


def home(request):
    if request.method == "POST":
        form = MovieForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = MovieForm()

    query = request.GET.get("q", "").strip() or "Batman"
    api_key = os.getenv("OMDB_API_KEY", "").strip() #troquei pra não jogar a api no github
    api_movies = []
    api_error = ""

    if not api_key:
        api_error = "Configure a variável OMDB_API_KEY antes de iniciar o servidor."
    else:
        try:
            response = requests.get(
                "https://www.omdbapi.com/",
                params={"apikey": api_key, "s": query, "type": "movie"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()

            if data.get("Response") == "True":
                api_movies = data.get("Search", [])[:10]
            else:
                api_error = data.get("Error", "Nenhum filme encontrado.")
        except (requests.RequestException, ValueError):
            api_error = "Não foi possível consultar a OMDb. Confira a chave e tente novamente."

    return render(request, "index.html", {
        "api_movies": api_movies,
        "api_error": api_error,
        "query": query,
        "movies": Movie.objects.order_by("id"),
        "form": form,
    })

def update_movie(request, movie_id):

    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        form = MovieForm(request.POST, instance=movie)

        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = MovieForm(instance=movie)

    return render(
        request,
        "edit_movie.html",
        {
            "form": form,
            "movie": movie
    })


def delete_movie(request, movie_id):
    if request.method == "POST":
        Movie.objects.filter(id=movie_id).delete()
    return redirect("home")
