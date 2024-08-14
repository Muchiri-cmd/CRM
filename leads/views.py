from django.shortcuts import render,redirect
# from django.contrib.auth.models import User
from Users.models import User
from .models import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import os 
from dotenv import load_dotenv
import threading
from django.utils import timezone
from datetime import timedelta
from datetime import datetime

def send_email_in_thread(subject, message, from_email, recepient_list):
    send_mail(subject, message, from_email, recepient_list, fail_silently=False)

def filter_leads(request,leads):
    price_min = request.GET.get('price_min')
    price_max = request.GET.get('price_max')
    country = request.GET.get('country')
    size_min = request.GET.get('size_min')
    size_max = request.GET.get('size_max')

    if price_min:
        leads = leads.filter(estimated_project_value__gte=price_min)
    if price_max:
        leads = leads.filter(estimated_project_value__lte=price_max)
    if country:
        leads = leads.filter(address__icontains=country)
    if size_min:
        leads = leads.filter(project_size__gte=size_min)
    if size_max:
        leads = leads.filter(project_size__lte=size_max)

    return leads

def create_google_calendar_url(event_title, event_date, details, location):
    base_url = "https://www.google.com/calendar/render?action=TEMPLATE"
    url = f"{base_url}&text={event_title}&dates={event_date}/{event_date}&details={details}&location={location}"
    return url

def format_date_for_google_calendar(dt):
    if isinstance(dt, str):
        # Convert string to datetime object if necessary
        dt = datetime.fromisoformat(dt) 
    return dt.strftime('%Y%m%d')

def send_calendar_invite(lead):
     if lead.next_action == 'Meeting':
            load_dotenv()
            subject = "New Meeting Scheduled"
            from_email = os.getenv('EMAIL_HOST_USER')
            recipient_list = [lead.next_action_owner.email]
            event_title = f"Meeting with {lead.company}"
            
            # Convert lead.next_action_scheduled_on to datetime if it's a string
            scheduled_on = datetime.fromisoformat(lead.next_action_scheduled_on) if isinstance(lead.next_action_scheduled_on, str) else lead.next_action_scheduled_on
            event_date = format_date_for_google_calendar(scheduled_on)
            
            details = ""
            location = ""  

            calendar_url = create_google_calendar_url(event_title, event_date, details, location)

            message = (
                f"Hi {lead.next_action_owner.username},\n\n"
                f"A meeting has been scheduled for {lead.company} on {lead.next_action_scheduled_on}. "
                f"Please add this meeting to your Google Calendar by clicking the link below:\n\n"
                f"{calendar_url}\n\n"
                f"Best regards,\nYour Team"
            )

            email_thread = threading.Thread(target=send_email_in_thread, args=(subject, message, from_email, recipient_list))
            email_thread.start()

def paginate_leads(leads, request):
    paginator_ref = Paginator(leads, 10)
    page_number = request.GET.get('page')
    page_object = paginator_ref.get_page(page_number)
    return page_object

    
# Create your views here.
@login_required
def leads(request):
    if request.user.is_employee:
        leads = Leads.objects.filter(Q(owner=request.user) | Q(next_action_owner=request.user))
    else:
        leads = Leads.objects.all()

    leads = filter_leads(request, leads).order_by('due_date')
    page_object = paginate_leads(leads, request)
    
    context = { 'leads': leads, 'page_object': page_object}
    template = 'leads/staff-leads.html' if request.user.is_employee else 'leads/leads.html'
    return render(request, template, context)

from Users.models import User

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
        # stages = request.POST.get('stages')
        next_action = request.POST.get('stages')
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
            # stages = stages,
            next_action=next_action,
            next_action_scheduled_on=next_action_scheduled_on,
            year=year,
            due_date=due_date,
            owner=owner_user,
            source=source,
            next_action_owner=next_action_owner_user
        )
        if (next_action_owner_user):
            load_dotenv()
            subject = "New Lead has been assigned to you"
            from_email = os.getenv('EMAIL_HOST_USER')
            recepient_list=[next_action_owner_user.email]
            message = f"Hi {next_action_owner_user.username},\n\nA new lead {company} has been assigned to you. Please login to your account to view the details."
            
            email_thread = threading.Thread(target=send_email_in_thread, args=(subject, message, from_email, recepient_list))
            email_thread.start()

        if (next_action == 'Meeting'):
           send_calendar_invite(new_lead)

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
        # lead.stage = request.POST.get('stages', lead.stage)
        lead.next_action = request.POST.get('stages', lead.next_action)
        lead.next_action_owner = User.objects.get(username=request.POST.get('next_action_owner', lead.next_action_owner.username))
        lead.next_action_scheduled_on = request.POST.get('next_action_scheduled_on', lead.next_action_scheduled_on)
        lead.due_date = request.POST.get('due_date', lead.due_date)
        # Assuming that the owner is being updated or assigned to the current user
        owner_username = request.user.username
        owner_user = User.objects.get(username=owner_username)
        # Perform any necessary updates or assignments related to the owner

        lead.save()
        send_calendar_invite(lead)
       

        return redirect('leads:leads')

    users = User.objects.all()
    context = {'users': users,'lead': lead}
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
        leads = Leads.objects.filter(
            (Q(owner=request.user) | Q(next_action_owner=request.user)) & Q(status='Won')
        )
    else:
        leads = Leads.objects.filter(status='Won')
  
    leads = filter_leads(request, leads)
    page_object = paginate_leads(leads, request)
    
    context = { 'leads': leads,'page_object': page_object}
    template = 'leads/staff-leads.html' if request.user.is_employee else 'leads/leads.html'

    return render(request, template, context)

# @login_required
def cold(request):
    if request.user.is_employee:
        leads = Leads.objects.filter(
            (Q(owner=request.user) | Q(next_action_owner=request.user)) & Q(status='Cold')
        )
    else:
        leads = Leads.objects.filter(status='Cold')
  
    leads = filter_leads(request, leads)
    page_object = paginate_leads(leads, request)

    context = { 'leads': leads,'page_object': page_object}

    template = 'leads/staff-leads.html' if request.user.is_employee else 'leads/leads.html'
    return render(request, template, context)

@login_required
def new_leads(request):
    if request.user.is_employee:
        leads = Leads.objects.filter(
            (Q(owner=request.user) | Q(next_action_owner=request.user)) & Q(status='Fresh')
        )
    else:
        leads = Leads.objects.filter(status='Fresh')

    leads = filter_leads(request, leads)
    page_object = paginate_leads(leads, request)

    context = {'leads': leads,'page_object': page_object}
    template = 'leads/staff-leads.html' if request.user.is_employee else 'leads/leads.html'
    return render(request, template, context)

@login_required
def site_surveys(request):
    if request.user.is_employee:
        leads = Leads.objects.filter(
            (Q(owner=request.user) | Q(next_action_owner=request.user)) & Q(next_action='Site Visit')
        )
    else:
        leads = Leads.objects.filter(next_action='Site Visit')

    leads = filter_leads(request, leads)
    page_object = paginate_leads(leads, request)

    context = { 'leads': leads,'page_object': page_object}

    template = 'leads/staff-leads.html' if request.user.is_employee else 'leads/leads.html'
    return render(request, template, context)

@login_required
def proposals(request):
    if request.user.is_employee:
        leads = Leads.objects.filter(
            (Q(owner=request.user) | Q(next_action_owner=request.user)) & Q(next_action='Proposal')
        )
    else:
        leads = Leads.objects.filter(next_action='Proposal')

    leads = filter_leads(request, leads)
    page_object = paginate_leads(leads, request)
    
    context = {'leads': leads,'page_object': page_object}
    template = 'leads/staff-leads.html' if request.user.is_employee else 'leads/leads.html'
    return render(request, template, context)
    
def meetings(request):
    if request.user.is_employee:
        leads = Leads.objects.filter(
            (Q(owner=request.user) | Q(next_action_owner=request.user)) & Q(next_action='Meeting')
        )
    else:
        leads = Leads.objects.filter(next_action='Meeting')

    leads = filter_leads(request, leads)
    page_object = paginate_leads(leads, request)
    
    context = {'leads': leads,'page_object': page_object}
    template = 'leads/staff-leads.html' if request.user.is_employee else 'leads/leads.html'
    return render(request, template, context)

def due_in_a_week(request):
    if request.user.is_employee:
        leads = Leads.objects.filter(
            (Q(owner=request.user) | Q(next_action_owner=request.user))
        )
    else:
        leads = Leads.objects.all()

    now = timezone.now()
    one_week_from_now = now + timedelta(weeks=1)
    due_in_next_week = leads.filter(
        due_date__gte=now,
        due_date__lte=one_week_from_now
    )

    leads = filter_leads(request, due_in_next_week)
    page_object = paginate_leads(leads, request)

    context = {'leads': leads,'page_object': page_object}
    template = 'leads/staff-leads.html' if request.user.is_employee else 'leads/leads.html'
    return render(request, template, context)
