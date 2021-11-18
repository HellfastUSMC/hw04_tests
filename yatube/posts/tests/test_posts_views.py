from django import forms
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

    def test_posts_views(self):

        self.auth_cl = Client()
        self.auth_cl.force_login(TestV.user)
        self.anon_cl = Client()
        self.auth_another = Client()
        self.auth_another.force_login(TestV.user_2)

        local_gr_slug = TestV.group.slug
        local_post_id = TestV.post12.pk
        local_username = TestV.user.username
        local_user = TestV.user
        local_group = TestV.group

        templates = {
            reverse('posts:index'): 'posts/index.html',
            reverse('posts:group_list', kwargs={'slug': f'{local_gr_slug}'}):
            'posts/group_list.html',
            reverse('posts:post_detail', kwargs={'post_id': f'{local_post_id}'}):
            'posts/post_detail.html',
            reverse('posts:profile', kwargs={'username': f'{local_username}'}):
            'posts/profile.html',
            reverse('posts:post_create'): 'posts/create_post.html',
            reverse('posts:post_edition', kwargs={'post_id': f'{local_post_id}'}):
            'posts/create_post.html',
        }

        post_form_fields = {
            'group': forms.ModelChoiceField,
            'text': forms.CharField,
        }

        print('Start testing posts views...')

        print('Start testing views templates in posts...')
        for reverse_name, template in templates.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.auth_cl.get(reverse_name)
                self.assertTemplateUsed(response, template)
        print('Done testing views templates in posts!')

        response = self.auth_cl.get(reverse('posts:index'))
        post_el = response.context.get('page_obj')[0]
        self.assertEqual(post_el.pk, self.post12.pk)
        self.assertEqual(post_el.text, self.post12.text)
        self.assertEqual(post_el.author, self.post12.author)
        self.assertEqual(post_el.group, self.post12.group)

        self.assertEqual(len(response.context['page_obj'].object_list), 10)

        response = self.auth_cl.get(reverse('posts:index') + '?page=2')
        self.assertEqual(len(response.context['page_obj'].object_list), 3)

        response = self.auth_cl.get(reverse('posts:group_list', kwargs={'slug': f'{local_gr_slug}'}))
        post_el = response.context.get('page_obj')[0]
        self.assertEqual(post_el.pk, self.post12.pk)
        self.assertEqual(post_el.text, self.post12.text)
        self.assertEqual(post_el.author, self.post12.author)
        self.assertEqual(post_el.group, self.post12.group)

        self.assertEqual(len(response.context['page_obj'].object_list), 10)

        for post in response.context.get('page_obj'):
            self.assertEqual(post.group, local_group)

        response = self.auth_cl.get(reverse('posts:group_list', kwargs={'slug': f'{local_gr_slug}'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj'].object_list), 1)

        response = self.auth_cl.get(reverse('posts:profile', kwargs={'username': f'{local_username}'}))
        post_el = response.context.get('page_obj')[0]
        self.assertEqual(post_el.pk, self.post12.pk)
        self.assertEqual(post_el.text, self.post12.text)
        self.assertEqual(post_el.author, self.post12.author)
        self.assertEqual(post_el.group, self.post12.group)

        for post in response.context.get('page_obj'):
            self.assertEqual(post.author, local_user)

        self.assertEqual(len(response.context['page_obj'].object_list), 10)

        response = self.auth_cl.get(reverse('posts:profile', kwargs={'username': f'{local_username}'}) + '?page=2')
        self.assertEqual(len(response.context['page_obj'].object_list), 2)

        response = self.auth_cl.get(reverse('posts:post_detail', kwargs={'post_id': f'{local_post_id}'}))
        post_el = response.context.get('post')
        self.assertEqual(post_el.pk, self.post12.pk)
        self.assertEqual(post_el.text, self.post12.text)
        self.assertEqual(post_el.author, self.post12.author)
        self.assertEqual(post_el.group, self.post12.group)

        response = self.auth_cl.get(reverse('posts:post_create'))
        for field, f_type in post_form_fields.items():
            with self.subTest(field=field):
                self.assertIsInstance(response.context['form'].fields.get(field), f_type)

        response = self.auth_cl.get(reverse('posts:post_edition', kwargs={'post_id': f'{local_post_id}'}))
        for field, f_type in post_form_fields.items():
            with self.subTest(field=field):
                self.assertIsInstance(response.context['form'].fields.get(field), f_type)