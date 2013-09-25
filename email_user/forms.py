from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from email_user.models import EmailUser


class EmailUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(EmailUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = EmailUser
        fields = ("email",)


class EmailUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(EmailUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = EmailUser