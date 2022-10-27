from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "articles"

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.detail, name="detail"),
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/like/", views.like, name="like"), 
    path('<int:pk>/comments/',views.comment_create, name='comment_create'),
    path('<int:review_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    path('<int:review_pk>/comments/<int:comment_pk>/update/', views.comments_update, name='comments_update'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)