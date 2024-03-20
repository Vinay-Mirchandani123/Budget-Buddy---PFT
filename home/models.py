from django.db import models

# Create your models here.

# class userInfo(request):
#     income 
#     impExpense
#     unimpExpense
#     saving= income-impExpense-unimpExpense
#     goal

# class goalTime(request):
#     userTime=
#     time=models.DateField(_(""), auto_now=False, auto_now_add=False)
#     overTime=userTime+time
class salary(models.Model):
    fixed_salary = models.IntegerField(null=False, blank=False)
    var_salary = models.IntegerField(null=False, blank=False)

class expense(models.Model):
    fixed_expense = models.IntegerField(null=False, blank=False)
    var_expense = models.IntegerField(null=False, blank=False)

class goal(models.Model):
    price=models.IntegerField(null=False, blank=False)
    time=models.DateField(null=False, blank=False)
    start_time=models.DateTimeField(auto_now_add=True, blank=False)
    
    
