from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('result', views.summary, name='result'),
    # روابط CRUD
    path('submissions/', views.submission_list, name='submission_list'),
    path('submissions/new/', views.submission_create, name='submission_create'),
    path('submissions/<int:pk>/', views.submission_detail, name='submission_detail'),
    path('submissions/<int:pk>/edit/', views.submission_edit, name='submission_edit'),
    path('submissions/<int:pk>/delete/', views.submission_delete, name='submission_delete'),
]