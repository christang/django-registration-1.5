from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login

from registration import signals
from registration.views import RegistrationView as BaseRegistrationView

try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = get_user_model()

class RegistrationView(BaseRegistrationView):
    """
    A registration backend which implements the simplest possible
    workflow: a user supplies an email address and password (the
    bare minimum for a useful account), and is immediately signed
    up and logged in).
    
    """
    def register(self, request, **cleaned_data):
        email, password = cleaned_data['email'], cleaned_data['password1']
        User.objects.create_user(email, password)

        new_user = authenticate(email=email, password=password)
        login(request, new_user)
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.
        
        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_success_url(self, request, user):
        return user.get_absolute_url(), (), {}
