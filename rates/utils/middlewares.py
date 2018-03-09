from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.deprecation import MiddlewareMixin


class DemoAuthMiddleware(MiddlewareMixin):
    '''
    Creates and authenticates demo-user (demo usecase only)
    '''
    def process_request(self, request):
        if not request.user.is_authenticated:
            demo_user, demopass = 'DemoUser', 'demouser'
            try:
                user = User.objects.get(username=demo_user)
            except User.DoesNotExist:
                user = User.objects.create_user(demo_user, 'demouser@foo.bar', demopass)
            user = authenticate(username=demo_user, password=demopass)
            request.user = user
        return None