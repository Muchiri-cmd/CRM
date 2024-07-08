from django.shortcuts import render
from django.contrib.admin.models import LogEntry


# Create your views here.
def activity_view(request):
    latest_actions = LogEntry.objects.all().order_by('-action_time')[:10]  
    
    context = {
         'latest_actions': latest_actions
    }   
    return render(request, 'activity/activity.html', context)