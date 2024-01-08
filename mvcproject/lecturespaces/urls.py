from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import create_and_save_flashcard

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('create/', views.create_lecturespace, name='create_lecturespace'),
    path('explore/', views.explore_lecturespaces, name='explore_lecturespaces'),
    path('lecturespace/<int:lecturespace_id>/', views.lecturespace_detail, name='lecturespace_detail'),
    path('lecturespace/<int:lecturespace_id>/create_flashcard/', create_and_save_flashcard, name='create_flashcard'),
    
   # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
 
 #   path('signup/', views.signup, name='signup'),  # Add this line for signup
 #   path('login/', views.login, name='login'), 
]
