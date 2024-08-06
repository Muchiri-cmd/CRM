from django.shortcuts import render
from leads.models import Leads
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

# Create your views here.
@login_required 
def index(request):
    if request.user.is_employee:
       leads = Leads.objects.filter(Q(owner=request.user) | Q(next_action_owner=request.user))
    elif request.user.is_manager:
        leads = Leads.objects.all()
    else:
        leads = Leads.objects.none()

    site_surveys = leads.filter(next_action='Site Survey').order_by('created_at')[:5]
    proposals = leads.filter(next_action='Proposal').order_by('created_at')[:5]
    won = leads.filter(status='Won').order_by('created_at')[:5]
    fresh_leads = leads.filter(Q(status='Fresh') | Q(status='New Lead')).order_by('-created_at')[:5]
    cold = leads.filter(status='Cold')
    meeting = leads.filter(next_action='Meeting').order_by('created_at')[:5]

    now = timezone.now()
    one_week_from_now = now + timedelta(weeks=1)
    due_in_next_week = Leads.objects.filter(
        due_date__gte=now,
        due_date__lte=one_week_from_now
    )

    new_leads_count = leads.filter(Q(status='Fresh') | Q(status='New Lead')).count()
    cold_count = leads.filter(status='Cold').count()
    won_count = leads.filter(status='Won').count()
    site_surveys_count = leads.filter(next_action='Site Survey').count()
    proposals_count = leads.filter(next_action='Proposal').count()

    # Pagination 
    paginator_ref = Paginator(fresh_leads, 10)
    page_number = request.GET.get('page')
    page_object = paginator_ref.get_page(page_number)

    context = {
        'new_leads': fresh_leads,
        'site_surveys': site_surveys,
        'proposals': proposals,
        'fresh_leads': fresh_leads,
        'fresh_leads_count': new_leads_count,
        'won': won,
        'cold': cold,   
        'cold_count': cold_count,
        'won_count': won_count,
        'site_surveys_count': site_surveys_count,
        'proposals_count': proposals_count,
        'meeting': meeting,
        'page_object': page_object,
        'leads_due_in_a_week': due_in_next_week,
    }

    if request.user.is_employee:
        return render(request, 'dashboard/staff.html', context)
    elif request.user.is_manager:
        return render(request, 'dashboard/index.html', context)
    else:
        return render(request, 'dashboard/no_access.html')