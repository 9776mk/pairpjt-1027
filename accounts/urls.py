from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
  path("", views.index, name='index'),
  path('signup/', views.signup, name='signup'),
  path('login/', views.login, name='login'),
  path('logout/', views.logout, name='logout'),
  path('detail/<int:pk>/', views.detail, name='detail'),
  path('update/', views.update, name='update'),
  path('password/', views.password, name='password'),
  path('delete/', views.delete, name='delete'),
  path('follow/<int:pk>', views.follow, name='follow'),
  path('profile/<int:pk>/', views.profile, name='profile'),
]