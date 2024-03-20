from django.contrib import admin

from .models import Salary, Expense, Goal

# Register your models here.

admin.site.register(Salary),
admin.site.register(Expense),
admin.site.register(Goal)
