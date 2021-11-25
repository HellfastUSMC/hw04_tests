from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from time import sleep

from ..models import Post, Group

user = get_user_model()


class TestV(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.cl = Client()
        cls.user = user.objects.create_user(username='VUser')
        cls.user_2 = user.objects.create_user(username='VAnotherUser')
        cls.group = Group.objects.create(
            title='VTestGroup',
            slug='VTG',
            description='VDESC'
        )
        cls.post1 = Post.objects.create(
            author=cls.user,
            text='V TEST POST ' * 3,
            group=cls.group,
        )
        cls.post2 = Post.objects.create(
            author=cls.user,
            text='V TEST POST ' * 3,
            group=cls.group,
        )
        cls.post3 = Post.objects.create(
            author=cls.user,
            text='V TEST POST ' * 3,
            group=cls.group,
        )
        cls.post4 = Post.objects.create(
            author=cls.user,
            text='V TEST POST ' * 3,
            group=cls.group,
        )
        cls.post5 = Post.objects.create(
            author=cls.user,
            text='V TEST POST ' * 3,
            group=cls.group,
        )
        cls.post6 = Post.objects.create(
            author=cls.user,
            text='V TEST POST ' * 3,
            group=cls.group,
        )
        cls.post7 = Post.objects.create(
            author=cls.user,
            text='V TEST POST ' * 3,
            group=cls.group,
        )
        cls.post8 = Post.objects.create(
            author=cls.user,
            text='V TEST POST ' * 3,
            group=cls.group,
        )
        cls.post9 = Post.objects.create(
            author=cls.user,
            text='V TEST POST ' * 3,
            group=cls.group,
        )
        cls.post10 = Post.objects.create(
            author=cls.user,
            text='V TEST POST ' * 3,
            group=cls.group,
        )
        cls.post13 = Post.objects.create(
            author=cls.user_2,
            text='V TEST POST ' * 3,
        )
        cls.post11 = Post.objects.create(
            author=cls.user,
            text='V TEST POST ' * 3,
        )
        sleep(0.1)
        cls.post12 = Post.objects.create(
            author=cls.user,
            text='V TEST POST ' * 3,
            group=cls.group,
        )
        cls.auth_cl = Client()
        cls.auth_cl.force_login(TestV.user)
        cls.auth_another = Client()
        cls.auth_another.force_login(TestV.user_2)

        cls.templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list',
                    kwargs={'slug': f'{cls.group.slug}'}):
                        'posts/group_list.html',
            reverse('posts:post_detail',
                    kwargs={'post_id': f'{cls.post12.pk}'}):
                        'posts/post_detail.html',
            reverse('posts:profile',
                    kwargs={'username': f'{cls.user.username}'}):
                        'posts/profile.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edition',
                    kwargs={'post_id': f'{cls.post12.pk}'}):
                        'posts/create_post.html',
        }

        cls.post_form_fields = {
            'group': forms.ModelChoiceField,
            'text': forms.CharField,
        }

    def test_views_templates(self):

        for reverse_name, template in self.templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.auth_cl.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_views_paginator_and_post_object_index_page(self):

        response = self.auth_cl.get(reverse('posts:index'))
        post_el = response.context.get('page_obj')[0]
        self.assertEqual(post_el.pk, self.post12.pk)
        self.assertEqual(post_el.text, self.post12.text)
        self.assertEqual(post_el.author, self.post12.author)
        self.assertEqual(post_el.group, self.post12.group)

        self.assertEqual(
            len(response.context['page_obj'].object_list),
            settings.POSTS_ON_PAGE
        )

        response = self.auth_cl.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj'].object_list), 3)

    def test_views_paginator_and_post_object_group_page(self):
        response = self.auth_cl.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': f'{self.group.slug}'}
            )
        )
        post_el = response.context.get('page_obj')[0]
        self.assertEqual(post_el.pk, self.post12.pk)
        self.assertEqual(post_el.text, self.post12.text)
        self.assertEqual(post_el.author, self.post12.author)
        self.assertEqual(post_el.group, self.post12.group)

        self.assertEqual(
            len(response.context['page_obj'].object_list),
            settings.POSTS_ON_PAGE
        )

        response = self.auth_cl.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': f'{self.group.slug}'}
            ) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj'].object_list), 1)

    def test_post_obj_affilation_group_and_profile_pages(self):

        response = self.auth_cl.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': f'{self.group.slug}'}
            )
        )

        for post in response.context.get('page_obj'):
            self.assertEqual(post.group, self.group)

    def test_views_paginator_and_post_object_profile_page(self):

        response = self.auth_cl.get(
            reverse(
                'posts:profile',
                kwargs={'username': f'{self.user.username}'}
            )
        )
        post_el = response.context.get('page_obj')[0]
        self.assertEqual(post_el.pk, self.post12.pk)
        self.assertEqual(post_el.text, self.post12.text)
        self.assertEqual(post_el.author, self.post12.author)
        self.assertEqual(post_el.group, self.post12.group)

        for post in response.context.get('page_obj'):
            self.assertEqual(post.author, self.user)

        self.assertEqual(
            len(response.context['page_obj'].object_list),
            settings.POSTS_ON_PAGE
        )

        response = self.auth_cl.get(
            reverse(
                'posts:profile',
                kwargs={'username': f'{self.user.username}'}
            ) + '?page=2'
        )
        self.assertEqual(len(response.context['page_obj'].object_list), 2)

    def test_views_post_detail_page(self):

        response = self.auth_cl.get(
            reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{self.post12.pk}'}
            )
        )
        post_el = response.context.get('post')
        self.assertEqual(post_el.pk, self.post12.pk)
        self.assertEqual(post_el.text, self.post12.text)
        self.assertEqual(post_el.author, self.post12.author)
        self.assertEqual(post_el.group, self.post12.group)

    def test_views_create_post_form_fields(self):

        response = self.auth_cl.get(reverse('posts:post_create'))
        for field, f_type in self.post_form_fields.items():
            with self.subTest(field=field):
                self.assertIsInstance(
                    response.context['form'].fields.get(field),
                    f_type
                )

        response = self.auth_cl.get(
            reverse(
                'posts:post_edition',
                kwargs={'post_id': f'{self.post12.pk}'}
            )
        )
        for field, f_type in self.post_form_fields.items():
            with self.subTest(field=field):
                self.assertIsInstance(
                    response.context['form'].fields.get(field),
                    f_type
                )
