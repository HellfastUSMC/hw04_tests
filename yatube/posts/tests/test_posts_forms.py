from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from posts.forms import PostForm
from ..models import Post, Group

user = get_user_model()


class TestF(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = user.objects.create_user(username='VUser')
        cls.user2 = user.objects.create_user(username='AnotherVUser')
        cls.group = Group.objects.create(
            title='VTestGroup',
            slug='VTG',
            description='VDESC'
        )

    def test_posts_views(self):

        self.cl = Client()
        self.cl.force_login(self.user)
        self.anon_cl = Client()
        self.cl2 = Client()
        self.cl2.force_login(self.user2)

        local_gr_slug = self.group.slug
        #local_post = self.post
        local_username = self.user.username
        local_user = self.user
        local_group = self.group

        templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:post_create'): 'posts/create_post.html',
        }

        post_form = {
            'text': 'TEST ENTRY',
            'group': local_group.pk,
        }

        print('Start testing post create form and redirect on success...')
        response = self.cl.post(reverse('posts:post_create'), data=post_form, follow=True)
        post_entry = Post.objects.get(pk=1)
        self.assertEqual(post_form['text'], post_entry.text)
        print('Post created!')
        self.assertRedirects(response, reverse('posts:profile', kwargs={'username': f'{local_username}'}))
        print('Redirect working!')
        print('Done testing post create form and redirect on success!')

        print('Start testing post edit form and redirect on success...')
        response = self.cl.post(reverse('posts:post_edition', kwargs={'post_id': f'{post_entry.pk}'}), data={'text': 'CHANGED!'}, follow=True)
        changed_post = Post.objects.get(pk=1)
        self.assertEqual('CHANGED!', changed_post.text)
        print('Post edited!')
        self.assertRedirects(response, reverse('posts:post_detail', kwargs={'post_id': f'{post_entry.pk}'}))
        print('Redirect working!')
        print('Done testing post edit form and redirect on success!')


        print('Start testing post edit form with another user and redirect to view...')
        response = self.cl2.post(reverse('posts:post_edition', kwargs={'post_id': f'{post_entry.pk}'}), data={'text': 'Hahahaha!!!1', 'group': local_group.pk}, follow=True)
        self.assertEqual('CHANGED!', changed_post.text)
        print('Post is not edited!')
        self.assertRedirects(response, reverse('posts:post_detail', kwargs={'post_id': f'{post_entry.pk}'}))
        print('Redirect working!')
        print('Done testing post edit form with another user and redirect to view!')