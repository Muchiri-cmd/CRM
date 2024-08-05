from django.shortcuts import render
from leads.models import Leads
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
@login_required 
def index(request):
    if request.user.is_employee:
       leads = Leads.objects.filter(Q(owner=request.user) | Q(next_action_owner=request.user))
    elif request.user.is_manager:
        leads = Leads.objects.all()
    else:
        leads = Leads.objects.none()

    site_surveys = leads.filter(status='Site Survey')
    proposals = leads.filter(status='Proposal')
    won = leads.filter(status='Won')
    fresh_leads = leads.filter(status='Fresh')
    engineering_design = leads.filter(status='Engineering Design')

    # Pagination 
    paginator_ref = Paginator(fresh_leads, 10)
    page_number = request.GET.get('page')
    page_object = paginator_ref.get_page(page_number)

    context = {
        'new_leads': leads.count(),
        'site_surveys': site_surveys,
        'proposals': proposals,
        'fresh_leads': fresh_leads,
        'fresh_leads_count': fresh_leads.count(),
        'engineering_design': engineering_design,
        'won': won,
        'won_count': won.count(),
        'site_surveys_count': site_surveys.count(),
        'proposals_count': proposals.count(),
        'page_object': page_object,
    }

    if request.user.is_employee:
        return render(request, 'dashboard/staff.html', context)
    elif request.user.is_manager:
        return render(request, 'dashboard/index.html', context)
    else:
        return render(request, 'dashboard/no_access.html')