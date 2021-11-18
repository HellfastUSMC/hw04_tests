from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.forms import PostForm

user = get_user_model()


class TestF(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

    def test_posts_views(self):

        self.cl = Client()

        signup_form = {
            'first_name': 'Vasya',
            'last_name': 'Petrov',
            'username': 'TEST',
            'email': 'ab@cd.ef',
            'password1': 't3Y2!@kjvz4CEFx',
            'password2': 't3Y2!@kjvz4CEFx',
        }

        print('Start testing sign up form and redirect on success...')
        response = self.cl.post(reverse('users:signup'), data=signup_form, follow=True)
        new_user = user.objects.get(pk=1)
        self.assertEqual(signup_form['username'], new_user.username)
        print('User created!')
        self.assertRedirects(response, reverse('posts:index'))
        print('Redirect working!')
        print('Done testing sign up form and redirect on success!')
