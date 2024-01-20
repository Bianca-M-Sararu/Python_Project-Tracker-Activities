from django.shortcuts import render ,redirect,get_object_or_404
from django.http import HttpResponse
from django .contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from .models import Activitati,Topic,Goal
from .forms import ActivitatiForm,GoalForm
from django.http import JsonResponse,HttpResponseNotFound
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import pygal
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Activitati, Goal
from django.db.models import Sum
from django.db.models.functions import TruncDate




'''activitate=[
    {'id':1 , 'name':'Adauga Activitate'},
    {'id':2 , 'name':'Inregistrare'},
    {'id':3 , 'name':'Cont'},
]'''
# Create your views here.

def loginPage(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('Home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            User.objects.get(username = username)
        except:
            messages.error(request,'Acest utilizator nu exista')

        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('Home')
        else :
            messages.error(request,'Acest utilizator sau parola nu exista')

    context = {'page':page}
    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('Home')

def registerPage(request):
    page = 'register'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('Home')
        else:
            messages.error(request,'In timpul inregistrarii a aparut o eroare ')

    return render(request,'base/login_register.html',{'form' : form})



@login_required(login_url='login')
def home(request):
    q = request.GET.get('q') if request.GET.get('q') else ''
    user_activitati = Activitati.objects.filter(host=request.user)
    activitate = user_activitati.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )
    
    topics = Topic.objects.all()
    numara_activitati = activitate.count()

    context = {'activitate': activitate, 'topics': topics, 'numara_activitati': numara_activitati}
    return render(request, 'base/Home.html', context)

def activitati(request,pk):
    activitati = Activitati.objects.get(id=pk)
    context={'activitati':activitati}
    return render(request,'base/activitati.html',context)


@login_required(login_url='login')
def progress_reports(request):
    activities = Activitati.objects.filter(host=request.user)
    total_seconds = sum(activity.duration_in_seconds for activity in activities)
    activity_data = [{'value': activity.duration_in_seconds, 'label': activity.name} for activity in activities]
    for data_point in activity_data:
        data_point['percentage'] = (data_point['value'] / total_seconds) * 100
    activity_pie_chart = pygal.Pie()
    for data_point in activity_data:
        activity_pie_chart.add(data_point['label'], [{'value': data_point['percentage'], 'label': f"{data_point['label']} - {data_point['percentage']:.2f}%"}])

    activity_chart = activity_pie_chart.render(is_unicode=True)
    return render(request, 'base/progress_reports.html', {
        'activity_chart': activity_chart,
    })


@login_required(login_url='login')
def real_time_monitoring(request):
    user = request.user

    user_activitati = Activitati.objects.filter(host=user)
    activity_labels = [activitati.name for activitati in user_activitati]
    activity_durations = [activitati.duration_in_seconds for activitati in user_activitati]
    activities_by_day = user_activitati.annotate(date=TruncDate('date_time_done')).values('date').annotate(total_duration=Sum('duration_in_seconds'))
    context = {
        'user_activitati': user_activitati,
        'activity_labels': activity_labels,
        'activity_durations': activity_durations,
        'activities_by_day': activities_by_day,
    }

    return render(request, 'base/real_time_monitoring.html', context)

@login_required(login_url='login')
def goal_setting(request):
    goals = Goal.objects.filter(user=request.user)
    form = GoalForm()

    if request.method == 'POST':
        form = GoalForm(request.POST)
        if form.is_valid():
            goal = form.save(commit=False)
            goal.user = request.user
            goal.save()
            return redirect('goal_setting')

    context = {'goals': goals, 'form': form}
    return render(request, 'base/goal_setting.html', context)

@login_required(login_url='login')
def complete_goal(request):
    if request.method == 'POST':
        goal_id = request.POST.get('goal_id')
        goal = get_object_or_404(Goal, id=goal_id)
        goal.completed = True
        goal.save()

        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})
    
@login_required
def mark_goal_done(request, goal_id):
    try:
        goal = Goal.objects.get(id=goal_id, user=request.user)
        goal.completed = not goal.completed
        goal.save()
        if goal.completed:
            messages.success(request, 'Congratulations! You completed the goal. Keep up the good work!')
        else:
             messages.info(request, 'Goal marked as not done. You can do it!')

        return redirect('goal_setting')
    except goal.completed == goal.completed:
        return HttpResponseNotFound("Goal already.")

from datetime import timedelta

from datetime import datetime

@login_required(login_url='login')
def real_time_monitoring(request):
    user = request.user
    selected_date_str = request.GET.get('selected_date')

    if selected_date_str:
        try:
            selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
            user_activitati = Activitati.objects.filter(host=user, date_time_done__date=selected_date)
        except ValueError:
          
            user_activitati = Activitati.objects.filter(host=user)
    else:
        user_activitati = Activitati.objects.filter(host=user)

    context = {
        'user_activitati': user_activitati,
    }

    return render(request, 'base/real_time_monitoring.html', context)



@login_required(login_url='login')
def creazaActivitati(request):
    form = ActivitatiForm()

    if request.method == 'POST':
        form = ActivitatiForm(request.POST)
        if form.is_valid():
            activitati = form.save(commit=False)
            activitati.host = request.user
            activitati.save()

            
            duration_in_seconds = (
                activitati.minutes * 60 +
                activitati.hours * 3600 +
                activitati.seconds
            )

            
            activitati.duration_in_seconds = duration_in_seconds
            activitati.save()

            return redirect('Home')

    context = {'form': form}
    return render(request, 'base/activitati_forma.html', context)

@login_required(login_url ='login')
def updateActivitati(request,pk):
    activitati = Activitati.objects.get(id=pk)

    if request.user != activitati.host:
        return HttpResponse('Nu ai permisiunea de a fi aici! ')

    if request.method == 'POST':
        form = ActivitatiForm(request.POST, instance=activitati)
        if form.is_valid():
            form.save()
            return redirect('Home')

    form = ActivitatiForm(instance=activitati)
    context = {'form':form}
    return render(request, 'base/activitati_forma.html',context)

@login_required(login_url ='login')
def deleteActivitati(request,pk):
    activitati = Activitati.objects.get(id=pk)

    if request.user != activitati.host:
        return HttpResponse('Nu ai permisiunea de a fi aici! ')
    
    if request.method == 'POST' :
        activitati.delete()
        return redirect('Home')
    return render(request , 'base/delete.html',{'obj':activitati})

