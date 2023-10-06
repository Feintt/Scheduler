import requests
from bs4 import BeautifulSoup


def authenticate_people_soft(userid, pwd):
    session = requests.Session()

    # Step 1: Initial GET request to fetch the login page
    initial_url = 'https://upsite.up.edu.mx/psp/CAMPUS/?cmd=login&languageCd=ESP'
    initial_response = session.get(initial_url)

    # Step 2: Extract CSRF token using BeautifulSoup
    soup = BeautifulSoup(initial_response.text, 'html.parser')

    # Assuming the CSRF token is in a hidden input field, adjust the selector as needed
    csrf_token_input = soup.find('input', attrs={'name': 'lcsrf_token'})
    csrf_token = csrf_token_input['value'] if csrf_token_input else None

    if not csrf_token:
        # Handle missing CSRF token
        return False

    # Step 3: POST request with the csrf_token and persisted cookies
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://upsite.up.edu.mx',
        'Referer': 'https://upsite.up.edu.mx/psp/CAMPUS/?cmd=login&languageCd=ESP',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/117.0.0.0 Safari/537.36 Edg/117.0.2045.55',
        'sec-ch-ua': '"Microsoft Edge";v="117", "Not;A=Brand";v="8", "Chromium";v="117"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'macOS',
    }

    data = {
        'lcsrf_token': csrf_token,
        'timezoneOffset': 300,
        'ptmode': 'f',
        'ptlangcd': 'ESP',
        'ptinstalledlang': 'ENG%2CESP',
        'userid': userid,
        'pwd': pwd,
        'ptlangsel': 'ESP'
    }

    response = session.post(initial_url, headers=headers, data=data)

    # Check response content or status to determine if login was successful
    if 'login_error' not in response.text:
        return True
    return False
