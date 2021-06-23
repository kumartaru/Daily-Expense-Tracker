from django.db import models

# Create your models here.


from django.db import models
from django.contrib.auth.models import User


class tblexpense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    expensedate = models.DateField()
    expenseitem = models.CharField(max_length=100, null=True)
    expensecost = models.CharField(max_length=20, null=True)
    notedate    = models.DateField()
    def __str__(self):
        return self.user.username