from django.shortcuts import render, redirect

from .models import Review, Comment
from .forms import ReviewForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import articles


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
    comment_form = CommentForm()
    context = {
        'review': review,
        'comments' : review.comment_set.all(),
        'comment_form' : comment_form,
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
    
def search(request):
    search = request.GET.get('search')
    reviews = Review.objects.filter(title__contains=search) | Review.objects.filter(content__contains=search) | Review.objects.filter(movie_name__contains=search)
    context = {
        'search' : search,
        'reviews' : reviews,
    }
    return render(request, 'articles/search.html', context)

def comment_create(request,pk):
    review = Review.objects.get(pk=pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = review
        comment.user = request.user
        comment.save()
    return redirect('articles:detail',review.pk)

def comments_delete(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    comment.delete()
    return redirect('articles:detail', review_pk)

def comments_update(request, review_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment,)
        if form.is_valid():
            form.save()
            #return redirect('articles:index', review.pk)
            return redirect('articles:detail',review_pk)
    else:
        form = CommentForm(instance=comment)
    context = {
        'form': form,
        'comment': comment,
        'review' : review_pk,

    }
    return render(request, 'articles/comments_update.html', context=context)   

    

