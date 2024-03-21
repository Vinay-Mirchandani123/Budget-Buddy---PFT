from django.contrib import admin
from django.urls import path
from goal import views


urlpatterns = [
    path("goalprogress", views.goalprogress, name='goalprogress'),
    path("expenseprogress", views.expenseprogress, name='expenseprogress'),
    path("incomeprogress", views.incomeprogress, name='incomeprogress'),
    path("mainprogress", views.mainprogress, name='mainprogress'),
    path("salary/<str:username>/", views.salary, name='salary'),
    path("expense/<str:username>/", views.expense, name='expense'),
    path("goal/<str:username>/", views.goal, name='goal'),
    path("dashboard", views.dashboard, name='dashboard'),

]