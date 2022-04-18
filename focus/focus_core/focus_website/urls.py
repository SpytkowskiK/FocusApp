from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),

    path('', views.TaskList.as_view(), name='tasks'),
    path('task/<int:pk>', views.TaskDetail.as_view(), name='task'),

    path('create/', views.TaskCreate.as_view(), name='create'),
    path('personal/', views.PersonalCreate.as_view(), name='personal'),
    path('update/<int:pk>/', views.TaskUpdate.as_view(), name='update'),
    path('task-view/<int:pk>/', views.PersonalTask.as_view(), name='task-view'),
    path('delete/<int:pk>/', views.TaskDelete.as_view(), name='delete'),
]
