from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus

from ..models import Post, Group

user = get_user_model()


class TestU(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.cl = Client()
        cls.user = user.objects.create_user(username='HasNoName')
        cls.user_non_author = user.objects.create_user(username='AnotherUser')
        cls.post = Post.objects.create(
            author=cls.user,
            text='U TEST POST ' * 10,
        )
        cls.group = Group.objects.create(
            title='UTestGroup',
            slug='UTG',
            description='UDESC',
        )

    def test_posts_urls(self):

        self.auth_cl = Client()
        self.auth_cl.force_login(TestU.user)
        self.anon_cl = Client()
        self.non_author_cl = Client()
        self.non_author_cl.force_login(TestU.user_non_author)

        local_gr_slug = TestU.group.slug
        local_post_id = TestU.post.pk
        local_username = TestU.user.username

        templates = {
            '/': 'posts/index.html',
            f'/group/{local_gr_slug}/': 'posts/group_list.html',
            f'/posts/{local_post_id}/': 'posts/post_detail.html',
            f'/profile/{local_username}/': 'posts/profile.html',
            '/create/': 'posts/create_post.html',
            f'/posts/{local_post_id}/edit/': 'posts/create_post.html',
        }

        print('Start testing posts urls...')

        print('Start testing posts urls templates...')
        for adress, template in templates.items():
            with self.subTest(adress=adress):
                response = self.auth_cl.get(adress)
                self.assertTemplateUsed(
                    response,
                    template,
                    f"There's problem in {template} with adress - {adress}"
                )
        print('Done testing posts urls templates!')

        print('Start testing create post for authed user...')
        response = self.auth_cl.get('/create/')
        self.assertEqual(
            response.reason_phrase,
            'OK',
            f'Wrong status - {response.status_code} {response.reason_phrase},'
            f'{HTTPStatus(response.status_code).description}'
        )
        print('Done testing create post for authed user!')

        print('Start testing edit post for author user...')
        response = self.auth_cl.get(f'/posts/{local_post_id}/edit/')
        self.assertEqual(
            response.reason_phrase,
            'OK',
            f'Wrong status - {response.status_code} {response.reason_phrase},'
            f'{HTTPStatus(response.status_code).description}'
        )
        print('Done testing create post for author user!')

        print('Start testing 404 page...')
        response = self.auth_cl.get('/wrong_page_404/')
        self.assertEqual(
            response.reason_phrase,
            'Not Found',
            f'Wrong status - {response.status_code} {response.reason_phrase},'
            f'{HTTPStatus(response.status_code).description}'
        )
        print('Done testing 404 page!')

        print('Start testing create page redirect for anon user...')
        response = self.anon_cl.get('/create/')
        self.assertRedirects(
            response,
            '/auth/login/?next=/create/'
        )
        print('Done testing create page redirect for anon user!')

        print('Start testing edit post page redirect for anon user...')
        response = self.anon_cl.get(f'/posts/{local_post_id}/edit/')
        self.assertRedirects(
            response,
            f'/auth/login/?next=/posts/{local_post_id}/edit/'
        )
        print('Done testing edit post page redirect for anon user!')

        print('Start testing edit post page redirect for non author user...')
        response = self.non_author_cl.get(f'/posts/{local_post_id}/edit/')
        self.assertRedirects(
            response,
            f'/posts/{local_post_id}/'
        )
        print('Done testing edit post page redirect for non author user!')
