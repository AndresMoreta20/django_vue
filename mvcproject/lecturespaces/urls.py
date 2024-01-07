from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('create/', views.create_lecturespace, name='create_lecturespace'),
    path('explore/', views.explore_lecturespaces, name='explore_lecturespaces'),
    path('lecturespace/<int:lecturespace_id>/', views.lecturespace_detail, name='lecturespace_detail'),
]
