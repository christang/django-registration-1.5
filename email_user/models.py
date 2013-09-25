from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import BaseUserManager, Group, AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _


MAX_EMAIL_LENGTH = 254
MAX_NAME_LENGTH = 30


class EmailUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def _join_group(self, user, group_name):
        """
        Add a user to named group.
        """
        group = Group.objects.get(name=group_name)
        user.groups.add(group)
        return group

    def create_user(self, email, password=None, group_name=None,
                    **extra_fields):
        """
        Create a user who is neither staff or superuser
        """
        user = self._create_user(email, password, False, False,
                                 **extra_fields)
        if group_name:
            self._join_group(user, group_name)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create a superuser

        A superuser can have any email
        """
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class EmailUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(
        _('email address'),
        max_length=MAX_EMAIL_LENGTH,
        unique=True)

    first_name = models.CharField(
        _('first name'),
        max_length=MAX_NAME_LENGTH,
        blank=True)

    last_name = models.CharField(
        _('last name'),
        max_length=MAX_NAME_LENGTH,
        blank=True)

    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'))

    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Deselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
        editable=False)

    objects = EmailUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __unicode__(self):
        return self.get_nice_email()

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def get_nice_email(self):
        """
        Returns email with first_name and last_name prefixed, if available.
        """
        email = self.get_full_name()
        if not email:
            return self.email
        else:
            return ' '.join([email, '<%s>' % self.email])

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
