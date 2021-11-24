from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

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
        cls.test_post = Post.objects.create(
            text='TEST EDIT TEXT',
            group=cls.group,
            author=cls.user
        )
        cls.cl = Client()
        cls.cl.force_login(cls.user)
        cls.cl2 = Client()
        cls.cl2.force_login(cls.user2)

    def test_post_create(self):

        local_username = self.user.username
        local_group = self.group

        post_form = {
            'text': 'TEST ENTRY',
            'group': local_group.pk,
        }

        print('Start testing post create form and redirect on success...')
        response = self.cl.post(
            reverse('posts:post_create'),
            data=post_form,
            follow=True
        )
        post_entry = Post.objects.latest('pk')
        self.assertEqual(post_form['text'], post_entry.text)
        self.assertEqual(local_group, post_entry.group)
        print('Post created!')
        self.assertRedirects(
            response,
            reverse('posts:profile', kwargs={'username': f'{local_username}'})
        )

        post_on_profile_page = response.context.get('page_obj')[0]
        self.assertEqual(
            post_entry.pk,
            post_on_profile_page.pk
        )
        print('Redirect working!')

        response = self.client.get(
            reverse(
                'posts:group_list',
                kwargs={'slug': f'{local_group.slug}'}
            )
        )

        post_on_group_page = response.context.get('page_obj')[0]
        self.assertEqual(
            post_entry.pk,
            post_on_group_page.pk
        )

        response = self.client.get(reverse('posts:index'))

        post_on_index_page = response.context.get('page_obj')[0]
        self.assertEqual(
            post_entry.pk,
            post_on_index_page.pk
        )

    def test_post_edit(self):

        print('Start testing post edit form and redirect on success...')
        response = self.cl.post(
            reverse(
                'posts:post_edition',
                kwargs={'post_id': f'{self.test_post.pk}'}
            ),
            data={'text': 'CHANGED!'}, follow=True
        )

        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{self.test_post.pk}'}
            )
        )
        changed_post = Post.objects.get(pk=self.test_post.pk)
        print(changed_post.text)
        self.assertEqual('CHANGED!', changed_post.text)
        print('Post edited!')
        print('Redirect working!')
        print('Done testing post edit form and redirect on success!')

        print(
            'Start testing post edit form with '
            'another user and redirect to view...'
        )

    def test_post_edit_diff_user(self):

        local_group = self.group

        response = self.cl2.post(
            reverse(
                'posts:post_edition',
                kwargs={'post_id': f'{self.test_post.pk}'}
            ),
            data={'text': 'Some new text', 'group': local_group.pk},
            follow=True
        )
        self.assertEqual('TEST EDIT TEXT', self.test_post.text)
        print('Post is not edited!')
        self.assertRedirects(
            response,
            reverse(
                'posts:post_detail',
                kwargs={'post_id': f'{self.test_post.pk}'}
            )
        )
        print('Redirect working!')
        print(
            'Done testing post edit form with '
            'another user and redirect to view!'
        )

        response = self.client.post(
            reverse(
                'posts:post_edition',
                kwargs={'post_id': f'{self.test_post.pk}'}
            ),
            data={'text': 'Some new text', 'group': local_group.pk},
            follow=True
        )
        self.assertEqual('TEST EDIT TEXT', self.test_post.text)
        print('Post is not edited!')
        self.assertRedirects(
            response,
            reverse('users:login', args=('?next=/posts/1/edit/',)) # HERE!!!!!!!!!!!!!!!!!
        )
