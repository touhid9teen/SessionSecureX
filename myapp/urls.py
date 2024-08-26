from django.urls import path
from . import views

urlpatterns = [
    path('items/', views.TodoView.as_view(), name='todo-list'),
    path('items/<int:pk>/', views.TodoDetailView.as_view(), name='todo-detail'),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
]
