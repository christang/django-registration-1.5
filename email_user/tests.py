from django.db import IntegrityError
from django.test import TestCase
from email_user.models import EmailUser


class SimpleTest(TestCase):

    def create_superuser(self):
        email = 'superuser@justice-league.org'
        password = 'krypton1te'
        return email, password, EmailUser.objects.create_superuser(email, password)

    def create_user(self):
        email = 'user@example.com'
        password = 'user123'
        return email, password, EmailUser.objects.create_user(email, password)

    def test_can_create_superuser(self):
        self.create_superuser()

        qs = EmailUser.objects.all()
        self.assertEqual(1, qs.count())

        user = qs[0]
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_create_other_user_types(self):
        self.create_user()

        qs = EmailUser.objects.all()
        self.assertEqual(1, qs.count())

        user = qs[0]
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_cannot_create_user_with_same_email(self):
        email, p, u = self.create_user()
        self.assertRaises(IntegrityError, EmailUser.create_user, email)
