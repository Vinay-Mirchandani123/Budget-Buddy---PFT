from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Salary(models.Model):
    user = models.CharField(max_length=100)
    fix_salary = models.IntegerField(null=False, blank=False)
    var_salary = models.IntegerField(null=False, blank=False)
    start_time=models.DateField(null=True, blank=True)
    time=models.IntegerField(null=False, blank=False)
    totalsalary=models.IntegerField(null=False, blank=False)
    last_salary_date=models.DateField(null=True, blank=True)
    def __str__(self):
        return self.user
    
    

class Expense(models.Model):
    user = models.CharField(max_length=100)
    fix_expense = models.IntegerField(null=False, blank=False)
    var_expense = models.IntegerField(null=False, blank=False)
    start_time=models.DateField(null=True, blank=True)
    time=models.IntegerField(null=False, blank=False)
    totalexpense=models.IntegerField(null=False, blank=False)
    last_expense_date=models.DateField(null=True, blank=True)
    
    
    def __str__(self):
        return self.user

class Goal(models.Model):
    user = models.CharField(max_length=100)
    goal_name=models.CharField(max_length=100,null=False, blank=False)
    amount=models.IntegerField(null=False, blank=False)
    goalDeadline=models.DateField(null=False, blank=False)
    remainmonth=models.IntegerField(null=False, blank=False)
    remainyear=models.IntegerField(null=False, blank=False)
    remaindays=models.IntegerField(null=False, blank=False)
    start_time=models.DateField(null=True, blank=True)
    time=models.IntegerField(null=False, blank=False)
    remainingamount=models.IntegerField(null=False, blank=False)
    days_in_month=models.IntegerField(null=False, blank=False)
    percentage=models.IntegerField(null=True, blank=False)

    def __str__(self):
        return self.user

