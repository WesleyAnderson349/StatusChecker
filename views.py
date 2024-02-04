import requests
from django.shortcuts import render
from .forms import URLForm
from urllib.parse import urlparse
import time

def check_website(request):
    status_info = {
        'website_name': None,
        'status_code': None,
        'status_message': None,
        'response_time': None,
        'redirect_url': None
    }

    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                start_time = time.time()  
                response = requests.get(url, timeout=30) 
                end_time = time.time()  
                response_time = end_time - start_time

                website_name = urlparse(url).hostname

                status_code = response.status_code

                status_messages = {
                    200: 'Website is up!',
                    404: 'Website is not found (404)',
                    500: 'Internal Server Error (500)',
                }

                status_message = status_messages.get(status_code, 'Unknown Status')

                # Check for redirection
                if response.url != url:
                    redirect_url = response.url
                else:
                    redirect_url = None

                status_info = {
                    'website_name': website_name,
                    'status_code': status_code,
                    'status_message': status_message,
                    'response_time': response_time,
                    'redirect_url': redirect_url
                }

            except requests.ConnectionError:
                status_info['status_message'] = 'Connection error: Website is down!'
            except requests.exceptions.Timeout:
                status_info['status_message'] = 'Request timed out: Website may be down or too slow to respond.'

    else:
        form = URLForm()

    return render(request, 'WebsiteCheck.html', {'form': form, 'status_info': status_info})
