from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib import messages
from goal.models import Salary, Expense, Goal
from datetime import datetime
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.views import View
from .models import *
from .serializers import *
from datetime import datetime, timedelta

# from .models import Profile

# # Create your views here.


# def progress(request):
#     # Retrieve data from models
#     
#     goals = Goal.objects.all()

#     # Prepare data for chart
#     salary_data = {'labels': ['Fixed Salary', 'Variable Salary'],
#                    'data': [sum(s.fix_salary for s in salaries), sum(s.var_salary for s in salaries)]}

#     expense_data = {'labels': ['Fixed Expense', 'Variable Expense'],
#                     'data': [sum(e.fix_expense for e in expenses), sum(e.var_expense for e in expenses)]}

#     goal_data = {'labels': [g.goal_name for g in goals],
#                  'data': [g.amount for g in goals]}

#     # Pass data to the template
#     context = {
#         'salary_data': salary_data,
#         'expense_data': expense_data,
#         'goal_data': goal_data,
#     }

#     return render(request, "mainbase.html", context)



def dashboard(request):
    return render(request, "dashboard.html")

def goalprogress(request):
    # Retrieve data from models
    goals = Goal.objects.filter(user=request.user)
    
    # Prepare data for chart
    
    goal_labels = [goal.goal_name for goal in goals]
    goal_amounts = [goal.amount for goal in goals]
    goal_time=[goal.start_time for goal in goals]
    # Pass data to the template
    context = {
        'goal_labels': goal_labels,
        'goal_amounts': goal_amounts, 
        'goal_time': goal_time
    }

    return render(request, "goalprogress.html",context)

def expenseprogress(request):
    expenses = Expense.objects.filter(user=request.user)
    # Prepare data for chart
    
    expense_labels = [expense.exp_name for expense in expenses]
    expense_fix = [expense.fix_expense for expense in expenses]
    expense_var = [expense.var_expense for expense in expenses]
    exp_time=[expense.start_time for expense in expenses]
    # Pass data to the template
    context = {
        'expense_labels': expense_labels,
        'expense_fix': expense_fix,
        'expense_var': expense_var,
        'exp_time':exp_time
    }

    return render(request, "expenseprogress.html", context)

def incomeprogress(request):
    # Retrieve data from models
    
    salaries = Salary.objects.filter(user=request.user)
    salary_labels = [salary.sal_name for salary in salaries]
    salary_var = [salary.var_salary for salary in salaries]
    salary_fix = [salary.fix_salary for salary in salaries]
    sal_time=[salary.start_time for salary in salaries]
    # Pass data to the template
    context = {
        
        'salary_labels': salary_labels,
        'salary_var': salary_var,
        'salary_fix': salary_fix,
        'sal_time':sal_time
    }

    return render(request, "incomeprogress.html", context)

def mainprogress(request):
    # Retrieve data from models
    goals = Goal.objects.filter(user=request.user)# #
    ##goals_labels.append(last_updated.strftime('%Y-%m-%d'))
    # #         remaining_amounts.append(remaining_amount)

    # #         # Increment date by 15 days
    # #         last_updated += timedelta(days=15)
    # context = {
    #     'goals_labels': goals_labels,
    #     'remaining_amounts': remaining_amounts,    
    # }

    # return render(request, "mainprogress.html", context)
    goal_labels = [goal.goal_name for goal in goals]
    goal_amounts = [goal.amount for goal in goals]
    # Pass data to the template
    context = {
        'goal_labels': goal_labels,
        'goal_amounts': goal_amounts,   
    }

    return render(request, "goalprogress.html", context)

# goal/views.py



# def goal_chart(request):
#     # Fetch all goals for the current user
#     goals = Goal.objects.filter(user=request.user)

#     # Initialize data lists for chart
#     labels = []  # Labels for x-axis (dates)
#     remaining_amounts = []  # Remaining amounts for each goal

#     # Get today's date
#     today = datetime.now().date()

    # Loop through each goal and calculate remaining amount every 15 days
    # for goal in goals:
        # remaining_amount = goal.remaining_amount
        # last_updated = goal.last_updated.date()

        # while last_updated <= today:
        #     labels.append(last_updated.strftime('%Y-%m-%d'))
        #     remaining_amounts.append(remaining_amount)

        #     # Increment date by 15 days
        #     last_updated += timedelta(days=15)

#     # Pass data to the template
#     context = {
#         'labels': labels,
#         'remaining_amounts': remaining_amounts,
#     }

#     return render(request, 'goal_chart.html', context)



def salary(request, username):
    if request.method == "POST":
        sal_name=request.POST['sal_name']
        fix_salary = request.POST["fix_salary"]
        var_salary = request.POST["var_salary"]
        user = username
        income = Salary(sal_name=sal_name,user=user,fix_salary=fix_salary, var_salary=var_salary,start_time=datetime.today())
        income.save()
        messages.success(request, "salary entered successfully")

    return render(request, "salary.html")


def expense(request,username):
    if request.method == "POST":
        exp_name = request.POST["exp_name"]
        fix_expense = request.POST["fix_expense"]
        var_expense = request.POST["var_expense"]
        user = username
        kharcha = Expense(
           user=user, exp_name=exp_name, fix_expense=fix_expense, var_expense=var_expense,start_time=datetime.today()
        )
        kharcha.save()
        messages.success(request, "expense entered successfully")
    return render(request, "expense.html")


def goal(request,username):
    if request.method == "POST":
        goal_name = request.POST["goal_name"]
        amount = request.POST["amount"]
        goalDeadline = request.POST["goalDeadline"]
        user = username
        start_time=datetime.today()
        
        achieve = Goal(
            user=user,
            goal_name=goal_name,
            amount=amount,
            goalDeadline=goalDeadline,
            start_time=start_time,
        )
        achieve.save()
        messages.success(request, "goal entered successfully")
    return render(request, "goal.html")


# def goal_chart(request):
#     goals = Goal.objects.all()
#     goal_labels = [Goal.goal_name for goal in goals]
#     goal_amounts = [Goal.goal_amount for goal in goals]
#     goal_data = {
#         'labels': goal_labels,
#         'amounts': goal_amounts,
#     }
#     return render(request, 'goal_chart.html', {'goal_data': goal_data})

# def goal_chart_data(request):
#     goals = Goal.objects.all()
#     goal_labels = [goal.name for goal in goals]
#     goal_amounts = [goal.amount for goal in goals]
#     data = {
#         'labels': goal_labels,
#         'amounts': goal_amounts,
#     }
#     return JsonResponse(data)


class salDataView(APIView):
    def get(self, request):
        data = Salary.objects.all()
        serializer = salDataSerializer(data, many=True)
        return JsonResponse(serializer.data,  safe=False)
    
class expDataView(APIView):
    def get(self, request):
        data = Expense.objects.all()
        serializer = expDataSerializer(data, many=True)
        return JsonResponse(serializer.data,  safe=False)

class goalDataView(APIView):
    def get(self, request):
        data = Goal.objects.all()
        serializer = goalDataSerializer(data, many=True)
        return JsonResponse(serializer.data,  safe=False)
