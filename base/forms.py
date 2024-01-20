from django.forms import ModelForm
from django import forms
from .models import Activitati
from .models import Goal,Topic

class ActivitatiForm(ModelForm):
    class Meta:
        model = Activitati
        fields = ['topic', 'name', 'description', 'date_time_done', 'rating_intensity', 'hours', 'minutes', 'seconds']
        widgets = {'date_time_done': forms.DateTimeInput(attrs={'type': 'datetime-local'}), }
class GoalForm(forms.ModelForm):
    topics = forms.ModelMultipleChoiceField(
        queryset=Topic.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,  # Set to True if you want the field to be required
    )
    class Meta:
        model = Goal
        fields = ['description', 'goal_type','topics']
        