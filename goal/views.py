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
from datetime import datetime,timedelta
import calendar
from django.db.models import Sum
count=1
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
    goals = Goal.objects.filter(user=request.user)
    salaries = Salary.objects.filter(user=request.user)
    expenses=Expense.objects.filter(user=request.user)
    # Prepare data for chart
    goal_amounts = [goal.amount for goal in goals]
    total_goal_amount = sum(goal_amounts)

    salary_fix_total = sum(s.fix_salary for s in salaries)
    salary_var_total = sum(s.var_salary for s in salaries)

    expense_fix_total = sum(e.fix_expense for e in expenses)
    expense_var_total = sum(e.var_expense for e in expenses)
    
    savings = salary_fix_total+salary_var_total - expense_fix_total-expense_var_total
    remainingsaving=savings
    # for s in salaries:
    #     salary1 = salary_var + salary_fix
    #     s.totalsalary = salary1
    #     s.save()
        
    goal_labels = [goal.goal_name for goal in goals]
    goal_amounts = [goal.amount for goal in goals]
    goal_time=[goal.start_time for goal in goals]
    salary_var = [salary.var_salary for salary in salaries]
    salary_fix = [salary.fix_salary for salary in salaries]
    sal_time=[salary.time for salary in salaries]
    expense_fix = [expense.fix_expense for expense in expenses]
    expense_var = [expense.var_expense for expense in expenses]
    exp_time=[expense.time for expense in expenses]
    for goal in goals:
        if remainingsaving > 0:
            if goal.remainingamount >= remainingsaving:
                goal.remainingamount -= remainingsaving
                remainingsaving = 0
            else:
                remainingsaving -= goal.remainingamount
                goal.remainingamount = 0
            goal.save()
    # Pass data to the template
    context = {
        'goal_labels': goal_labels,
        'goal_amounts': goal_amounts, 
        'goal_time': goal_time,
        'expense_fix': expense_fix,
        'expense_var': expense_var,
        'exp_time':exp_time,
        'salary_var': salary_var,
        'salary_fix': salary_fix,
        'sal_time':sal_time,
        'total_goal_amount': total_goal_amount,
        'salary_fix_total': salary_fix_total,
        'salary_var_total': salary_var_total,
        'expense_fix_total': expense_fix_total,
        'expense_var_total': expense_var_total,
        'savings':savings,
        'goals':goals,
        'salaries':salaries,
        'expenses':expenses,
        'remainingsaving':remainingsaving
    }
    return render(request, "dashboard.html",context)

def goalprogress(request):
    # Retrieve data from models
    goals = Goal.objects.filter(user=request.user)
    salaries = Salary.objects.filter(user=request.user)
    expenses=Expense.objects.filter(user=request.user)
    # Prepare data for chart
    
    goal_labels = [goal.goal_name for goal in goals]
    goal_amounts = [goal.amount for goal in goals]
    goal_time=[goal.time for goal in goals]
    goal_deadlines=[goal.goalDeadline for goal in goals]
    total_goal_amount = sum(goal_amounts)

    salary_fix_total = sum(s.fix_salary for s in salaries)
    salary_var_total = sum(s.var_salary for s in salaries)

    expense_fix_total = sum(e.fix_expense for e in expenses)
    expense_var_total = sum(e.var_expense for e in expenses)
    
    savings = salary_fix_total+salary_var_total - expense_fix_total-expense_var_total
    remainsavings=savings
    salary_var = [salary.var_salary for salary in salaries]
    salary_fix = [salary.fix_salary for salary in salaries]
    sal_time=[salary.time for salary in salaries]
    expense_fix = [expense.fix_expense for expense in expenses]
    expense_var = [expense.var_expense for expense in expenses]
    exp_time=[expense.time for expense in expenses]
    
    # Calculate remaining time for each goal
    today = datetime.now().date()
    for goal in goals:
        remaining_month = (goal.remainmonth - (today.month - goal.start_time.month))%12
        # Update the goal_remaining_time field in the model instance
        goal.remainmonth =remaining_month
        goal.save()
    for goal in goals:
        remaining_year = goal.remainyear - (today.year - goal.start_time.year)
        goal.remainyear = remaining_year
        goal.save()
    
    for goal in goals:
        goal.remainingamount = goal.amount
        goal.save()
    for goal in goals:
        if savings > 0:
            if goal.remainingamount >= savings:
                goal.remainingamount -= savings
                savings = 0
            else:
                savings -= goal.remainingamount
                goal.remainingamount = 0
            goal.save()
    context = {
        'goal_labels': goal_labels,
        'goal_amounts': goal_amounts, 
        'goal_time': goal_time,
        'goal_deadline': goal_deadlines,
        'goals':goals,
        'expense_fix': expense_fix,
        'expense_var': expense_var,
        'exp_time':exp_time,
        'salary_var': salary_var,
        'salary_fix': salary_fix,
        'sal_time':sal_time,
        'total_goal_amount': total_goal_amount,
        'salary_fix_total': salary_fix_total,
        'salary_var_total': salary_var_total,
        'expense_fix_total': expense_fix_total,
        'expense_var_total': expense_var_total,
        'savings':savings,
        'remainsavings':remainsavings
        # 'goal_remaintime':goal_remaintime,
    }

    return render(request, "goalprogress.html",context)

def expenseprogress(request):
    expenses = Expense.objects.filter(user=request.user)
    # Prepare data for chart
    expense_fix = [expense.fix_expense for expense in expenses]
    expense_var = [expense.var_expense for expense in expenses]
    exp_time=[expense.time for expense in expenses]
    # Pass data to the template
    context = {
        'expense_fix': expense_fix,
        'expense_var': expense_var,
        'exp_time':exp_time
    }

    return render(request, "expenseprogress.html", context)

def incomeprogress(request):
    # Retrieve data from models
    
    salaries = Salary.objects.filter(user=request.user)
    salary_var = [salary.var_salary for salary in salaries]
    salary_fix = [salary.fix_salary for salary in salaries]
    sal_time=[salary.time for salary in salaries]
    # Pass data to the template
    context = {
        'salary_var': salary_var,
        'salary_fix': salary_fix,
        'sal_time':sal_time
    }

    return render(request, "incomeprogress.html", context)

def user_count(request):
    # Count the number of users
    user_count = User.objects.count()
    
    # Pass the user count to the template
    context = {
        'user_count': user_count
    }
    return render(request, "dashboard.html", context)

def mainprogress(request):
    # Retrieve data from models
    goals = Goal.objects.filter(user=request.user)
    salaries = Salary.objects.filter(user=request.user)
    expenses=Expense.objects.filter(user=request.user)
    # Prepare data for chart
    goal_amounts = [goal.amount for goal in goals]
    total_goal_amount = sum(goal_amounts)

    salary_fix_total = sum(s.fix_salary for s in salaries)
    salary_var_total = sum(s.var_salary for s in salaries)

    expense_fix_total = sum(e.fix_expense for e in expenses)
    expense_var_total = sum(e.var_expense for e in expenses)
    
    savings = salary_fix_total+salary_var_total - expense_fix_total-expense_var_total
    goal_labels = [goal.goal_name for goal in goals]
    goal_amounts = [goal.amount for goal in goals]
    goal_time=[goal.time for goal in goals]
    salary_var = [salary.var_salary for salary in salaries]
    salary_fix = [salary.fix_salary for salary in salaries]
    sal_time=[salary.time for salary in salaries]
    expense_fix = [expense.fix_expense for expense in expenses]
    expense_var = [expense.var_expense for expense in expenses]
    exp_time=[expense.time for expense in expenses]
    # Pass data to the template
    context = {
        'goal_labels': goal_labels,
        'goal_amounts': goal_amounts, 
        'goal_time': goal_time,
        'expense_fix': expense_fix,
        'expense_var': expense_var,
        'exp_time':exp_time,
        'salary_var': salary_var,
        'salary_fix': salary_fix,
        'sal_time':sal_time,
        'total_goal_amount': total_goal_amount,
        'salary_fix_total': salary_fix_total,
        'salary_var_total': salary_var_total,
        'expense_fix_total': expense_fix_total,
        'expense_var_total': expense_var_total,
        'savings':savings,
        'goals':goals,
    }

    return render(request, "mainprogress.html",context)

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
    global count
    # Fetch the existing salary data if it exists
    salary = Salary.objects.filter(user=username).first()
    if request.method == "POST":
        fix_salary = request.POST["fix_salary"]
        var_salary = request.POST["var_salary"]
        user = username
        start_time=datetime.today()
        totalsalary=int(int(fix_salary)+int(var_salary))
        year=start_time.year
        month=start_time.month
        day=start_time.day
        time = year * 100 + month
        # If salary data exists, update it
        if salary is not None:
            salary.fix_salary = fix_salary
            salary.var_salary = var_salary
            salary.totalsalary = totalsalary
            salary.start_time = start_time
            salary.time = time
            salary.last_salary_date = datetime.now()
            salary.save()
        else:
            # If salary data does not exist, create it
            salary = Salary(totalsalary=totalsalary,user=user,fix_salary=fix_salary, var_salary=var_salary,start_time=start_time, time=time,last_salary_date=datetime.now())
            salary.save()
        messages.success(request, "Income entered successfully")
    # Check if a month has passed since the last salary entry
    last_salary = Salary.objects.filter(user=username).order_by('-last_salary_date').first()
    if last_salary is not None and last_salary.last_salary_date is not None and datetime.now().date() < last_salary.last_salary_date + timedelta(days=30):
        form_enabled = False
        messages.success(request, "You have entered your Income, Now you can enter it after 30days")
    else:
        form_enabled = True

    return render(request, "salary.html", {"form_enabled": form_enabled, "salary": salary})



def expense(request, username):
    # Fetch the existing expense data if it exists
    expense = Expense.objects.filter(user=username).first()
    if request.method == "POST":
        fix_expense = request.POST["fix_expense"]
        var_expense = request.POST["var_expense"]
        user = username
        start_time=datetime.today()
        totalexpense=int(int(var_expense)+int(fix_expense))
        year=start_time.year
        month=start_time.month
        day=start_time.day
        time = year * 100 + month
        # If expense data exists, update it
        if expense is not None:
            expense.fix_expense = fix_expense
            expense.var_expense = var_expense
            expense.totalexpense = totalexpense
            expense.start_time = start_time
            expense.time = time
            expense.last_expense_date = datetime.now()
            expense.save()
        else:
            # If expense data does not exist, create it
            expense = Expense(totalexpense=totalexpense, user=user, fix_expense=fix_expense, var_expense=var_expense, start_time=start_time, time=time, last_expense_date=datetime.now())
            expense.save()
        messages.success(request, "Expense entered successfully")
    # Check if a day has passed since the last expense entry
    last_expense = Expense.objects.filter(user=username).order_by('-last_expense_date').first()
    if last_expense is not None and last_expense.last_expense_date is not None and datetime.now().date() < last_expense.last_expense_date + timedelta(days=30):
        form_enabled = False
        messages.success(request, "You have entered your Expense, Now you can enter it after 1 day")
    else:
        form_enabled = True
    return render(request, "expense.html", {"form_enabled": form_enabled, "expense": expense})



def goal(request,username):
    income_exists = Salary.objects.filter(user=username).exists()
    expense_exists = Expense.objects.filter(user=username).exists()

    if not income_exists or not expense_exists:
        messages.warning(request, "Please enter your income and expense first.")
        return redirect("/goal/salary/user.username")
    if request.method == "POST":
        goalDeadline = request.POST["goalDeadline"]
        
        # Check if the deadline is greater than today's date
        if datetime.strptime(goalDeadline, '%Y-%m-%d').date() > datetime.now().date():
            goal_name = request.POST["goal_name"]
            amount = request.POST["amount"]
            user = username
            today = datetime.now().date()
            days_in_month = calendar.monthrange(today.year, today.month)[1]
            start_time = datetime.today()
            remainingamount = amount
            if datetime.strptime(goalDeadline, '%Y-%m-%d').date().day < datetime.now().date().day:
                remaining_month = (datetime.strptime(goalDeadline, '%Y-%m-%d').date().year - start_time.year) * 12 + \
                               (datetime.strptime(goalDeadline, '%Y-%m-%d').date().month - start_time.month) - 1
                remaining_year = datetime.strptime(goalDeadline, '%Y-%m-%d').date().year - start_time.year
            # remaining_days = (datetime.strptime(goalDeadline, '%Y-%m-%d').date().year - start_time.year) * 12 + \
            #                    (datetime.strptime(goalDeadline, '%Y-%m-%d').date().month - start_time.month)*30 + \
            #                        (datetime.strptime(goalDeadline, '%Y-%m-%d').date().day - start_time.day) 
                
                remaining_days = datetime.strptime(goalDeadline, '%Y-%m-%d').date().day + days_in_month-datetime.now().date().day
                
            else:    
                remaining_month = (datetime.strptime(goalDeadline, '%Y-%m-%d').date().year - start_time.year) * 12 + \
                                (datetime.strptime(goalDeadline, '%Y-%m-%d').date().month - start_time.month)
                remaining_year = datetime.strptime(goalDeadline, '%Y-%m-%d').date().year - start_time.year
                # remaining_days = (datetime.strptime(goalDeadline, '%Y-%m-%d').date().year - start_time.year) * 12 + \
                #                    (datetime.strptime(goalDeadline, '%Y-%m-%d').date().month - start_time.month)*30 + \
                #                        (datetime.strptime(goalDeadline, '%Y-%m-%d').date().day - start_time.day) 
                
                remaining_days = datetime.strptime(goalDeadline, '%Y-%m-%d').date().day - datetime.now().date().day
            time = start_time.year * 100 + start_time.month
            
            # Calculate the total income and expense of the user
            total_income = Salary.objects.filter(user=username).aggregate(Sum('totalsalary'))['totalsalary__sum']
            total_expense = Expense.objects.filter(user=username).aggregate(Sum('totalexpense'))['totalexpense__sum']
            savings_rate = total_income - total_expense

            # Check if the user's salary and expense are enough to meet the goal amount
            if savings_rate < int(amount):
                if remaining_month > 0:
                    required_expense_reduction = int((int(amount) - (savings_rate*remaining_month))/remaining_month)
                else :
                    required_expense_reduction = int(int(amount) - (savings_rate*remaining_month))
                if savings_rate > 0 and required_expense_reduction > 0:
                    required_months = int(amount) / savings_rate
                    if (start_time.month+required_months) > 12:
                        required_year =int((start_time.month+required_months)/12)+start_time.year
                        required_month= int(start_time.month+required_months)%12
                        req=float((start_time.month+required_months)%12-required_month)*calendar.monthrange(required_year, required_month)[1]
                        required_days = int(start_time.day+req)+1
                        
                        if required_days>calendar.monthrange(required_year, required_month)[1]:
                            required_days=required_days-calendar.monthrange(required_year, required_month)[1]
                            required_month=required_month+1
                            if required_month > 12:
                                required_year=required_year+1
                                required_month=required_month/12
                                required_days=required_days-calendar.monthrange(required_year, required_month)[1]
                            
                            
                        
                    else:
                        required_year = start_time.year
                        required_month = required_months/12+start_time.month
                        required_days = remaining_days
                        
                    
                    messages.warning(request, f"Your current income and expense are not enough to meet the goal amount. You need to reduce your expense by at least Rs. {required_expense_reduction} or If you donot want to decrease your expense, you should increase your goal deadline to {required_year}-{required_month}-{required_days}. You can also consider opting for an investment method to increase your variable salary.")
                    return render(request, "goal.html")
                elif savings_rate < 0:
                    messages.warning(request, "You are not currently saving any money. Please consider increasing your income or decreasing your expenses.")
                    return render(request, "goal.html")
            # Create the goal instance only if the deadline is valid
            
            achieve = Goal(
                user=user,
                goal_name=goal_name,
                amount=amount,
                goalDeadline=goalDeadline,
                start_time=start_time,
                time=time,
                remainmonth=remaining_month,
                remainyear=remaining_year,
                remainingamount=remainingamount,
                remaindays=remaining_days,
                days_in_month=days_in_month
            )
            achieve.save()
            messages.success(request, "Goal entered successfully")
        else:
            messages.warning(request, "Invalid deadline. Deadline should be greater than today date.")
    # if request.method == "POST":
    #     goalDeadline = request.POST["goalDeadline"]
        
    #     #working
    #     if datetime.strptime(goalDeadline, '%Y-%m-%d').date() > datetime.now().date():
    #         goal_name = request.POST["goal_name"]
    #         amount = request.POST["amount"]
    #     else:
    #         messages.error(request, "Invalid deadline. Deadline should be greater than today's date.")
    #     user = username
    #     start_time=datetime.today()
    #     today = datetime.now().date()
    #     deadyear= goalDeadline[0:4]
    #     deadmonth=goalDeadline[5:7]
    #     deadday=goalDeadline[8:]
    #     remainingamount=amount
        
    #     # remaining_time = year*12 + month*30 +day 
        
        
    #     year=start_time.year
    #     month=start_time.month
    #     day=start_time.day
    #     remaining_month = (int(deadyear) - int(year))*12 + ((int(deadmonth))-int(month))
    #     remaining_year =int(deadyear) -  int(year)
    #     time = year * 100 + month

    #     achieve = Goal(
    #         user=user,
    #         goal_name=goal_name,
    #         amount=amount,
    #         goalDeadline=goalDeadline,
    #         start_time=start_time,
    #         time=time,
    #         remainmonth=remaining_month,
    #         remainyear=remaining_year,
    #         remainingamount=remainingamount
    #     )
    #     achieve.save()
    #     messages.success(request, "goal entered successfully")
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
        return JsonResponse(serializer.data, safe=False)