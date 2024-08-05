from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
from Users.models import User
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def leads(request):
    if request.user.is_employee:
        leads = Leads.objects.filter(Q(owner=request.user) | Q(next_action_owner=request.user))
    else:
        leads = Leads.objects.all()

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    country = request.GET.get('country')
    industry = request.GET.get('industry')
    status = request.GET.get('status')
    project_type = request.GET.get('project_type')

    if price_min:
        leads = leads.filter(estimated_project_value__gte=price_min)
    if price_max:
        leads = leads.filter(estimated_project_value__lte=price_max)
    if country:
        leads = leads.filter(address__icontains=country)
    if industry:
        leads = leads.filter(industry__icontains=industry)
    if status:
        leads = leads.filter(status__icontains=status)
    if project_type:
        leads = leads.filter(project_type__icontains=project_type)

    paginator_ref = Paginator(leads, 10)
    page_number = request.GET.get('page')
    page_object = paginator_ref.get_page(page_number)
    
    context = {
        'leads': leads,
        'page_object': page_object
    }

    if request.user.is_employee:
        return render(request, 'leads/staff-leads.html', context)
    return render(request, 'leads/leads.html', context)


@login_required 
def create_lead(request):
    if not request.user.is_manager:
        print("unauthorized access")
        return render(request, 'dashboard/no_access.html')
    
    if request.method == 'POST':
        # Extract data from the POST request
        name = request.POST.get('name')
        company = request.POST.get('company')
        country = request.POST.get('country')
        industry = request.POST.get('industry')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        project_type = request.POST.get('project_type')
        project_size = request.POST.get('project_size')
        bess_size = request.POST.get('bess_size')
        estimated_project_value = request.POST.get('estimated_project_value')
        status = request.POST.get('status')
        next_action = request.POST.get('next_action')
        next_action_scheduled_on = request.POST.get('next_action_scheduled_on')
        year = request.POST.get('year')
        due_date = request.POST.get('due_date')
       
        owner_user = request.user
        source = request.POST.get('source')
        next_action_owner_username = request.POST.get('next_action_owner')

        # Get the corresponding User object for next_action_owner
        next_action_owner_user = User.objects.get(username=next_action_owner_username)

        # Create a new Leads object
        new_lead = Leads.objects.create(
            name=name,
            company=company,
            country=country,
            industry=industry,
            email=email,
            phone=phone,
            address=address,
            project_type=project_type,
            project_size=project_size,
            bess_size=bess_size,
            estimated_project_value=estimated_project_value,
            status=status,
            next_action=next_action,
            next_action_scheduled_on=next_action_scheduled_on,
            year=year,
            due_date=due_date,
            owner=owner_user,
            source=source,
            next_action_owner=next_action_owner_user
        )
        return redirect('leads:leads')

    users = User.objects.all()
    context = {
        'users': users
    }

    return render(request, 'leads/create_new_lead.html', context)

@login_required
def edit_lead(request, id):
    lead = Leads.objects.get(id=id)
    if request.method == 'POST':
        lead.name = request.POST.get('name', lead.name)
        lead.company = request.POST.get('company', lead.company)
        lead.country = request.POST.get('country', lead.country)
        lead.industry = request.POST.get('industry', lead.industry)
        lead.email = request.POST.get('email', lead.email)
        lead.phone = request.POST.get('phone', lead.phone)
        lead.address = request.POST.get('address', lead.address)
        lead.project_type = request.POST.get('project_type', lead.project_type)
        lead.project_size = request.POST.get('project_size', lead.project_size)
        lead.estimated_project_value = request.POST.get('estimated_project_value', lead.estimated_project_value)
        lead.status = request.POST.get('status', lead.status)
        lead.next_action = request.POST.get('next_action', lead.next_action)
        lead.next_action_scheduled_on = request.POST.get('next_action_scheduled_on', lead.next_action_scheduled_on)

        # Assuming that the owner is being updated or assigned to the current user
        owner_username = request.user.username
        owner_user = User.objects.get(username=owner_username)
        # Perform any necessary updates or assignments related to the owner

        lead.save()
        return redirect('leads:leads')

    users = User.objects.all()
    context = {
        'users': users,
        'lead': lead
    }
    return render(request, 'leads/edit_lead.html', context)

@login_required
def delete_lead(request, id):
    if not request.user.is_manager:
        print("unauthorized access")
        return render(request, 'dashboard/no_access.html')
    
    lead = Leads.objects.get(id=id)
    lead.delete()
    return redirect('leads:leads')

@login_required
def won(request):
    if request.user.is_employee:
        leads = Leads.objects.filter((Q(owner=request.user) | Q(next_action_owner=request.user)) & Q(status='Won'))
    else:
        leads = Leads.objects.filter(status='Won')

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    country = request.GET.get('country')
    industry = request.GET.get('industry')
    status = request.GET.get('status')
    project_type = request.GET.get('project_type')

    if price_min:
        leads = leads.filter(estimated_project_value__gte=price_min)
    if price_max:
        leads = leads.filter(estimated_project_value__lte=price_max)
    if country:
        leads = leads.filter(address__icontains=country)
    if industry:
        leads = leads.filter(industry__icontains=industry)
    if status:
        leads = leads.filter(status__icontains=status)
    if project_type:
        leads = leads.filter(project_type__icontains=project_type)

    paginator_ref = Paginator(leads, 10)
    page_number = request.GET.get('page')
    page_object = paginator_ref.get_page(page_number)

    context = {
        'leads': leads,
        'page_object': page_object
    }
    # return render(request, 'leads/filtered_leads.html', context)
    if request.user.is_employee:
        return render(request, 'leads/staff-filtered.html', context)
    return render(request, 'leads/filtered_leads.html', context)

@login_required
def new_leads(request):
    if request.user.is_employee:
        leads = Leads.objects.filter((Q(owner=request.user) | Q(next_action_owner=request.user)) & Q(status='Fresh'))
    else:
        leads = Leads.objects.all()

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    country = request.GET.get('country')
    industry = request.GET.get('industry')
    status = request.GET.get('status')
    project_type = request.GET.get('project_type')

    if price_min:
        leads = leads.filter(estimated_project_value__gte=price_min)
    if price_max:
        leads = leads.filter(estimated_project_value__lte=price_max)
    if country:
        leads = leads.filter(address__icontains=country)
    if industry:
        leads = leads.filter(industry__icontains=industry)
    if status:
        leads = leads.filter(status__icontains=status)
    if project_type:
        leads = leads.filter(project_type__icontains=project_type)

    paginator_ref = Paginator(leads, 10)
    page_number = request.GET.get('page')
    page_object = paginator_ref.get_page(page_number)

    context = {
        'leads': leads,
        'page_object': page_object
    }
    if request.user.is_employee:
        return render(request, 'leads/staff-filtered.html', context)
    return render(request, 'leads/filtered_leads.html', context)

@login_required
def site_surveys(request):
    if request.user.is_employee:
        leads = Leads.objects.filter((Q(owner=request.user) | Q(next_action_owner=request.user)) & Q(status='Site Survey'))
    else:
       leads = Leads.objects.all()

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    country = request.GET.get('country')
    industry = request.GET.get('industry')
    status = request.GET.get('status')
    project_type = request.GET.get('project_type')

    if price_min:
        leads = leads.filter(estimated_project_value__gte=price_min)
    if price_max:
        leads = leads.filter(estimated_project_value__lte=price_max)
    if country:
        leads = leads.filter(address__icontains=country)
    if industry:
        leads = leads.filter(industry__icontains=industry)
    if status:
        leads = leads.filter(status__icontains=status)
    if project_type:
        leads = leads.filter(project_type__icontains=project_type)

    paginator_ref = Paginator(leads, 10)
    page_number = request.GET.get('page')
    page_object = paginator_ref.get_page(page_number)

    context = {
        'leads': leads,
        'page_object': page_object
    }
    if request.user.is_employee:
        return render(request, 'leads/staff-filtered.html', context)
    return render(request, 'leads/filtered_leads.html', context)

@login_required
def proposals(request):
    if request.user.is_employee:
        leads = Leads.objects.filter((Q(owner=request.user) | Q(next_action_owner=request.user)) & Q(status='Site Survey'))
    else:
       leads = Leads.objects.all()

    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    country = request.GET.get('country')
    industry = request.GET.get('industry')
    status = request.GET.get('status')
    project_type = request.GET.get('project_type')

    if price_min:
        leads = leads.filter(estimated_project_value__gte=price_min)
    if price_max:
        leads = leads.filter(estimated_project_value__lte=price_max)
    if country:
        leads = leads.filter(address__icontains=country)
    if industry:
        leads = leads.filter(industry__icontains=industry)
    if status:
        leads = leads.filter(status__icontains=status)
    if project_type:
        leads = leads.filter(project_type__icontains=project_type)

    paginator_ref = Paginator(leads, 10)
    page_number = request.GET.get('page')
    page_object = paginator_ref.get_page(page_number)

    context = {
        'leads': leads,
        'page_object': page_object
    }
    if request.user.is_employee:
        return render(request, 'leads/staff-filtered.html', context)
    return render(request, 'leads/filtered_leads.html', context)