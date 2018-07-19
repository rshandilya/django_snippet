# middleware.py

from django.core import exceptions
from django.contrib.auth.views import logout

# list of IPs we want to allow. in this ex: company's public IP
ALLOWED_IPS = ('127.0.0.1',)

class IPRestrictMiddleware(object):

    def process_request(self, request):
        ip = self.get_client_ip(request)
        restrict_user = request.user.groups.filter(name='Restrict').exists() and ip not in ALLOWED_IPS
        if restrict_user:
            logout(request)
            raise exceptions.PermissionDenied

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

# settings.py
MIDDLEWARE_CLASSES = (
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'path.to.IPRestrictMiddleware',
    ...
)
