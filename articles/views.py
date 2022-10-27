from django.shortcuts import render, redirect
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def index(request):
    reviews = Review.objects.order_by("-id")
    context = {"reviews": reviews}
    return render(request, "articles/index.html", context)

@login_required
def create(request):
    if request.method == "POST":
        # DB에 저장하는 로직
        review_form = ReviewForm(request.POST, request.FILES)
        if review_form.is_valid():
            review = review_form.save(commit = False)
            review.user = request.user
            review_form.save()
            return redirect("articles:index")
    else:
        review_form = ReviewForm()
    context = {"review_form": review_form}
    return render(request, "articles/create.html", context=context)

@login_required
def update(request, pk):
    review = Review.objects.get(pk=pk)
    if request.method == 'POST':
        form = ReviewForm(request.POST, request.FILES, instance=review,)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', review.pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'form': form
    }
    return render(request, 'articles/update.html', context=context)

def detail(request, pk):
    review = Review.objects.get(pk=pk)
    context = {
        'review': review,
    }
    return render(request, 'articles/detail.html', context)

@login_required
def delete(request, pk):
    review = Review.objects.get(pk=pk)
    review.delete()
    return redirect("articles:index")


def like(request, pk):
    review = Review.objects.get(pk=pk)
    #로그인 한 유저가 좋아요를 눌렀다면
    if request.user in review.like_users.all():
    # 좋아요 삭제
        review.like_users.remove(request.user)
    else:
    # 좋아요 추가하고
        review.like_users.add(request.user)
    # 상세 페이지로 redirect
    return redirect('articles:detail', pk)
    