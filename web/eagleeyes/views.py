from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from clips import models
import re
from datetime import datetime

def index(request):
    date_query = request.GET.get('date', '')

    date = datetime.now()
    date_match = re.match(r'(\d{4})-(\d{2})-(\d{2})', date_query)
    if date_match:
        date = datetime.fromisoformat(date_query)

    clips = models.Clip.objects.filter(timestamp__year=date.year, timestamp__month=date.month, timestamp__day=date.day)
    context = {'clips': clips, 'selected_date': date.strftime('%m/%d/%Y')} # this is how we get variables to our templates 
                               # could do date filtering somewhere in here 

    return render(request, 'home.html', context)

def login_view(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return HttpResponseRedirect("/n1.html")# Redirect to a success page.
    return render(request, 'enter.html', {'login_form': form })