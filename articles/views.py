from django.shortcuts import render,redirect
from .models import Review
from .forms import ReviewForm

# Create your views here.
def index(request):
    reviews =  Review.objects.all()
    context={
        'reviews':reviews
    }
    return render(request, 'articles/index.html',context)


def create(request):
    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review_form.save()
            return redirect('articles:index')
    else:
        review_form = ReviewForm()
    context = {
        'review_form' : review_form
    }
    return render(request,'articles/create.html',context = context)

def detail(request,pk):
    review = Review.objects.get(pk=pk)

    context = {
        'review' : review
    }
    return render(request, 'articles/detail.html',context)
