from django.db.models import Q
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from datetime import date
from django.db.models import Sum
from datetime import datetime, timedelta, time
import random
# Create your views here.

def Index(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['email']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request,user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'index.html',d)

def Logout(request):
    logout(request)
    return redirect('index')


def register(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['name']
        e = request.POST['email']
        m = request.POST['mobilenumber']
        p = request.POST['password']
        try:
            user = User.objects.create_user(username=e, password=p, first_name=f,last_name=m)
            error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'register.html',d)



def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('index')
    today = datetime.now().date()
    yesterday = today - timedelta(1)
    seven = today - timedelta(7)
    thirty = today - timedelta(30)
    year = today - timedelta(365)

    tc = tblexpense.objects.filter(expensedate=today,user=request.user.id).aggregate(Sum('expensecost'))
    yc = tblexpense.objects.filter(expensedate=yesterday,user=request.user.id).aggregate(Sum('expensecost'))
    sc = tblexpense.objects.filter(expensedate__gte=seven,expensedate__lte=today,user=request.user.id).aggregate(Sum('expensecost'))
    thc = tblexpense.objects.filter(expensedate__gte=thirty, expensedate__lte=today, user=request.user.id).aggregate(Sum('expensecost'))
    yrc = tblexpense.objects.filter(expensedate__gte=year, expensedate__lte=today,user=request.user.id).aggregate(Sum('expensecost'))
    totalexpense = tblexpense.objects.filter(user=request.user.id).aggregate(Sum('expensecost'))

    d = {'tc':tc,'yc':yc,'sc':sc,'thc':thc,'yrc':yrc,'totalexpense':totalexpense}
    return render(request,'dashboard.html',d)


def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error}
    return render(request,'changepassword.html',d)


def add_expense(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    if request.method=="POST":
        u = User.objects.filter(username=request.user.username).first()
        de = request.POST['dateexpense']
        it = request.POST['item']
        ci = request.POST['costitem']
        try:
            tblexpense.objects.create(user=u,expensedate=de,expenseitem=it,expensecost=ci,notedate=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'add_expense.html', d)


def manage_expense(request):
    if not request.user.is_authenticated:
        return redirect('index')
    expense = tblexpense.objects.filter(user=request.user.id)
    d = {'expense':expense}
    return render(request, 'manage_expense.html', d)

def delete_expense(request,pid):
    if not request.user.is_authenticated:
        return redirect('index')
    expense = tblexpense.objects.get(id=pid)
    expense.delete()
    return redirect('manage_expense')

def expense_datewisedetail(request):
    if not request.user.is_authenticated:
        return redirect('index')
    return render(request, 'expense_datewisedetail.html')



def expense_datewise(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "POST":
        fd = request.POST['fromdate']
        td = request.POST['todate']


        expense = tblexpense.objects.filter(Q(expensedate__gte=fd) & Q(expensedate__lte=td),user=request.user.id).values('expensedate').annotate(totaldaily=Sum('expensecost'))
        expensecount = tblexpense.objects.filter(Q(expensedate__gte=fd) & Q(expensedate__lte=td)).count()
        expensetotal = tblexpense.objects.filter(Q(expensedate__gte=fd) & Q(expensedate__lte=td),user=request.user.id).values('expensedate').annotate(totaldaily=Sum('expensecost')).aggregate(Sum('totaldaily'))

        '''for i in expenseabc:
                total = total + i.totaldaily'''


        d = {'expense': expense,'fd':fd,'td':td,'expensecount':expensecount,'expensetotal':expensetotal}
        return render(request, 'expense_datewisedetail.html', d)
    return render(request, 'expense_datewise.html')


def userprofile(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    user=User.objects.get(id=request.user.id)
    if request.method == 'POST':
        f = request.POST['fullname']

        u = request.POST['contactnumber']

        user.first_name=f
        user.last_name=u
        try:
            user.save()
            error = "no"
        except:
            error="yes"
    d = {'error':error,'user':user}
    return render(request, 'userprofile.html',d)