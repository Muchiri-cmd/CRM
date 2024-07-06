from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from .models import *

# Create your views here.
def leads(request):
    return render(request, 'base.html')

def create_lead(request):
    if request.POST:
       # Extract data from the POST request
        name = request.POST.get('name')
        company = request.POST.get('company')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        project_size = request.POST.get('project_size')
        estimated_project_value = request.POST.get('estimated_project_value')
        status = request.POST.get('status')
        next_action = request.POST.get('next_action')
        next_action_scheduled_on = request.POST.get('scheduledOn')
        owner_username = request.POST.get('owner') 
        source = request.POST.get('source')
        next_action_owner = request.POST.get('next_action_owner')

        # Get the corresponding User object for next_action_owner
        owner_user = User.objects.get(username=owner_username)
        next_action_owner = User.objects.get(username=next_action_owner)

        # Create a new Leads object
        new_lead = Leads.objects.create(
            name=name,
            company=company,
            email=email,
            phone=phone,
            address=address,
            project_size=project_size,
            estimated_project_value=estimated_project_value,
            status=status,
            next_action=next_action,
            next_action_scheduled_on=next_action_scheduled_on,
            owner=owner_user,  
            source=source,
            next_action_owner=next_action_owner
        )
        return redirect('leads:leads')

    users = User.objects.all()
    context = {
        'users': users
    }
    print(users)
    return render(request, 'leads/create_new_lead.html',context)