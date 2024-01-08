from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import create_and_save_flashcard, save_flashcard, save_lecturespace, like_flashcard, dislike_flashcard  

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('create/', views.create_lecturespace, name='create_lecturespace'),
    path('explore/', views.explore_lecturespaces, name='explore_lecturespaces'),
    path('lecturespace/<int:lecturespace_id>/', views.lecturespace_detail, name='lecturespace_detail'),
    path('lecturespace/<int:lecturespace_id>/create_flashcard/', create_and_save_flashcard, name='create_flashcard'),
    path('lecturespace/save/<int:lecturespace_id>/', save_lecturespace, name='save_lecturespace'),
    path('flashcard/save/<int:flashcard_id>/', save_flashcard, name='save_flashcard'),
    path('flashcard/like/<int:flashcard_id>/', like_flashcard, name='like_flashcard'),
    path('flashcard/dislike/<int:flashcard_id>/', dislike_flashcard, name='dislike_flashcard'),
    path('lecturespace/unsave/<int:lecturespace_id>/', views.unsave_lecturespace, name='unsave_lecturespace'),
    path('flashcard/unsave/<int:flashcard_id>/', views.unsave_flashcard, name='unsave_flashcard'),


   # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
 
 #   path('signup/', views.signup, name='signup'),  # Add this line for signup
 #   path('login/', views.login, name='login'), 
]
