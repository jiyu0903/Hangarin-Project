from django.urls import path
from .views import delete_task, edit_task, home, login_view, logout_view, add_task

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('add/', add_task, name='add_task'),
    path('delete/<int:id>/', delete_task, name='delete_task'),
    path('edit/<int:id>/', edit_task, name='edit_task'),
]