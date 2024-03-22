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
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    subject=models.CharField(max_length=100)
    message=models.TextField()
    date=models.DateField()
    def __str__(self):
        return self.name


    
    
    
    
