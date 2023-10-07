from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from requests.utils import dict_from_cookiejar
import requests


# Create your views here.

@login_required
def schedule(request):

    if 'schedule' not in request.session:
        cookies = request.session['cookies']
        token = request.session['token']
        session = requests.Session()
        session.cookies = requests.utils.cookiejar_from_dict(cookies)
        headers = {'Authorization': 'token ' + token}
        schedule_url = 'http://flow-api:8000/user/schedule/'
        response = session.get(schedule_url, headers=headers)
        request.session['schedule'] = response.json()

    return render(request, 'Dashboard/schedule.html', {'schedule': request.session['schedule']})
