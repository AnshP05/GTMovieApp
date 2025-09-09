from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Movie, Review
from .forms import ReviewForm

def search(request):
    query = request.GET.get("q")
    results = Movie.objects.filter(title__icontains=query) if query else []
    return render(request, "movies/search_results.html", {
        "results": results,
        "query": query,
    })

def home(request):
    query = request.GET.get("q", "")
    movies = Movie.objects.all()
    if query:
        movies = movies.filter(title__icontains=query)
    return render(request, "movies/home.html", {"movies": movies, "query": query})


def about(request):
    return render(request, "movies/about.html")


def movie_detail(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    reviews = movie.reviews.all()
    form = ReviewForm()
    return render(request, "movies/movie_detail.html", {
        "movie": movie,
        "reviews": reviews,
        "form": form
    })


# ---------- Reviews ----------

@login_required
def review_create(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.movie = movie
            review.user = request.user
            review.save()
            messages.success(request, "Review added!")
            return redirect("movies:movie_detail", pk=movie.pk)
    else:
        form = ReviewForm()
    return render(request, "movies/review_form.html", {"form": form, "movie": movie})


@login_required
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.info(request, "Review updated.")
            return redirect("movies:movie_detail", pk=review.movie.pk)
    else:
        form = ReviewForm(instance=review)
    return render(request, "movies/review_form.html", {"form": form, "movie": review.movie})


@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk, user=request.user)
    movie_pk = review.movie.pk
    if request.method == "POST":
        review.delete()
        messages.warning(request, "Review deleted.")
        return redirect("movies:movie_detail", pk=movie_pk)
    return render(request, "movies/review_confirm_delete.html", {"review": review})
