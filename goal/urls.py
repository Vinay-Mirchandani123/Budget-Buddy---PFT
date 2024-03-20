from django.contrib import admin
from django.urls import path
from goal import views


urlpatterns = [
    path("progress", views.progress, name='progress'),
    path("salary/<str:username>/", views.salary, name='salary'),
    path("expense/<str:username>/", views.expense, name='expense'),
    path("goal/<str:username>/", views.goal, name='goal'),
    # path('chart/', goal_chart, name='goal_chart'),
    # path('chart-data/', goal_chart_data, name='goal_chart_data')

]