import os
from unittest import mock

from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError
from django.utils.six import StringIO

from django.contrib.auth import get_user_model


class TestCreateUserCommand(TestCase):

    def setUp(self):
        self.UserModel = get_user_model()

    def test_required_arguments(self):
        expected_error_msg = ('Error: the following '
                              'arguments are required: username, email')

        with self.assertRaisesRegexp(CommandError, expected_error_msg):
            call_command('createuser')

    def test_user_creation_noinput(self):
        with open(os.devnull, 'w') as dest:
            call_command('createuser',  'joe', 'joe@example.com',
                         noinput=True, stdout=dest, stderr=dest)
        no_user_created = False

        try:
            created_user = self.UserModel.objects.get(username='joe')
        except self.UserModel.DoesNotExist:
            no_user_created = True

        self.assertFalse(no_user_created)
        self.assertEqual(created_user.email, 'joe@example.com')
        self.assertFalse(created_user.has_usable_password())

    def test_user_creation_already_exists(self):
        self.UserModel.objects.create_user('joe', 'joe@example.com')
        out = StringIO()
        with self.assertRaises(SystemExit):
            call_command('createuser', 'joe', 'joe#@example.com',
                         noinput=True, stderr=out)
        self.assertIn('Error: That username is already taken', out.getvalue())

    @mock.patch('getpass.getpass')
    def test_user_creation_interactive(self, getpw):
        getpw.return_value = 'randompassword'

        out = StringIO()
        call_command('createuser', 'joe', 'joe@example.com', stdout=out)
        no_user_created = False
        try:
            created_user = self.UserModel.objects.get(username='joe')
        except self.UserModel.DoesNotExist:
            no_user_created = True

        self.assertFalse(no_user_created)
        self.assertEqual(created_user.email, 'joe@example.com')
        self.assertTrue(created_user.has_usable_password())
        self.assertTrue(created_user.check_password('randompassword'))
        self.assertFalse(created_user.check_password('random'))
