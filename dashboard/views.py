from django.shortcuts import render
from leads.models import Leads
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required 
def index(request):
    new_leads = Leads.objects.all().count()
    site_surveys_count = Leads.objects.filter(status='Site Survey').count()
    site_surveys = Leads.objects.filter(status='Site Survey')
    proposals_count = Leads.objects.filter(status='Proposal').count()
    proposals = Leads.objects.filter(status='Proposal')

    won_count = Leads.objects.filter(status='Won').count()

    fresh_leads = Leads.objects.filter(status='Fresh')
    fresh_leads_count = Leads.objects.filter(status='Fresh').count()
    won = Leads.objects.filter(status='Won')
    engineering_design = Leads.objects.filter(status='Engineering Design')
    po_received = Leads.objects.filter(status='PO Received')

   
    paginator_ref = Paginator(fresh_leads, 10)
    page_number = request.GET.get('page')
    page_object = paginator_ref.get_page(page_number)


    context = {
        'new_leads': new_leads,
        'site_surveys': site_surveys,
        'proposals': proposals,
        'fresh_leads': fresh_leads,
        'fresh_leads_count': fresh_leads_count,
        'enginering_design': engineering_design,
        'won':won,
        'won_count':won_count,
        'po_received': po_received,
        'site_surveys_count': site_surveys_count,
        'proposals_count': proposals_count,
        'page_object': page_object
        
    }
    return render(request, 'dashboard/index.html',context)