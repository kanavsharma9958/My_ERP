from django.shortcuts import render
from reception.models import Notice # <-- Notice मॉडल को इम्पोर्ट करें

def home_view(request):
    # सबसे नए और एक्टिव 5 नोटिस को ढूंढें
    notices = Notice.objects.filter(is_active=True).order_by('-publish_date')[:5]
    
    context = {
        'notices': notices
    }
    return render(request, 'core/home.html', context)