# -*- coding: utf8 -*-
from unittest import skipIf

import django
from django.contrib.auth import authenticate
from django.test.utils import override_settings
from django.utils import unittest

from mock import patch, MagicMock

from nopassword.backends.base import NoPasswordBackend
from nopassword.backends.sms import TwilioBackend
from nopassword.models import LoginCode
from nopassword.utils import get_user_model


class AuthenticationBackendTests(unittest.TestCase):
    @override_settings(AUTH_USER_MODULE='tests.NoUsernameUser')
    def test_authenticate_with_custom_user_model(self):
        """When a custom user model is used that doesn't have a field
        called "username" return `None`
        """
        result = authenticate(username='username')
        self.assertIsNone(result)

    @skipIf(django.VERSION < (1, 5), 'Custom user not supported')
    @patch('nopassword.backends.sms.TwilioRestClient')
    @override_settings(AUTH_USER_MODEL='tests.PhoneNumberUser', NOPASSWORD_TWILIO_SID="aaaaaaaa",
                       NOPASSWORD_TWILIO_AUTH_TOKEN="bbbbbbbb", DEFAULT_FROM_NUMBER="+15555555")
    def test_twilio_backend(self, mock_object):
        self.user = get_user_model().objects.create(username='twilio_user')
        self.code = LoginCode.create_code_for_user(self.user, next='/secrets/')
        self.assertEqual(len(self.code.code), 20)
        self.assertIsNotNone(authenticate(username=self.user.username, code=self.code.code))
        self.assertEqual(LoginCode.objects.filter(user=self.user, code=self.code.code).count(), 0)

        self.backend = TwilioBackend()
        self.backend.twilio_client.messages.create = MagicMock()

        self.backend.send_login_code(self.code)
        self.assertTrue(mock_object.called)
        self.assertTrue(self.backend.twilio_client.messages.create.called)

        authenticate(username=self.user.username)
        self.assertEqual(LoginCode.objects.filter(user=self.user).count(), 1)

        self.user.delete()


class TestBackendUtils(unittest.TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create(username='test_user')
        self.inactive_user = get_user_model().objects.create(username='inactive', is_active=False)
        self.backend = NoPasswordBackend()

    def tearDown(self):
        self.user.delete()
        self.inactive_user.delete()

    def test_verify_user(self):
        self.assertTrue(self.backend.verify_user(self.user))
        self.assertFalse(self.backend.verify_user(self.inactive_user))

    def test_send_login_code(self):
        self.assertRaises(NotImplementedError, self.backend.send_login_code, code=None)
