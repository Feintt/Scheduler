from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from requests.utils import dict_from_cookiejar, cookiejar_from_dict
import requests


# Create your views here.

@login_required
def schedule(request):
    """
    This view will render the schedule of the user, it will get the schedule from the session,
    if it's not there, it will get it from the API and save it in the session.
    :param request:
    :return:
    """
    days = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']

    if 'schedule' not in request.session:
        cookies = request.session['api_cookies']
        token = request.session['token']
        session = requests.Session()
        session.cookies = cookiejar_from_dict(cookies)
        headers = {'Authorization': 'token ' + token}
        schedule_url = 'http://flow-api:8000/user/schedule/'
        response = session.get(schedule_url, headers=headers)
        request.session['schedule'] = response.json()

    return render(request, 'Dashboard/schedule.html', {'schedule': request.session['schedule'], 'days': days})
