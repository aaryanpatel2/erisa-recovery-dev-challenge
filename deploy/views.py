import os
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def github_webhook(request):
    if request.method == 'POST':
        # Run git pull to update code
        repo_path = os.path.expanduser('~apdev/erisa-recovery-dev-challenge')
        os.system(f'cd {repo_path} && git pull')

        # Run migrations (just in case models were changed)
        os.system(f'cd {repo_path} && python3 manage.py migrate --no-input')

        # Reload web app
        os.system(f'touch /var/www/apdev_pythonanywhere_com_wsgi.py')

        return HttpResponse('Deployment successful!', status=200)

    return HttpResponseBadRequest('Invalid request')
