from django.urls import path
from . import views

urlpatterns=[
    path('login/',views.loginPage,name="login"),
    path('logout/',views.logoutUser,name="logout"),
    path('register/',views.registerPage,name="register"),
    path('',views.home,name="Home"),
    path('progress-reports/', views.progress_reports, name='progress_reports'),
    path('real-time-monitoring/', views.real_time_monitoring, name='real_time_monitoring'),
    path('goal_setting/', views.goal_setting, name='goal_setting'),
    path('complete_goal/', views.complete_goal, name='complete_goal'),
    path('mark_goal_done/<int:goal_id>/', views.mark_goal_done, name='mark_goal_done'),
    path('activitati/<str:pk>/',views.activitati,name="activitati"),
    path('creaza-activitati/',views.creazaActivitati,name="creaza-activitati"),
    path('update-activitati/<str:pk>/',views.updateActivitati,name="update-activitati"),
    path('delete-activitati/<str:pk>/',views.deleteActivitati,name="delete-activitati"),
    
]

