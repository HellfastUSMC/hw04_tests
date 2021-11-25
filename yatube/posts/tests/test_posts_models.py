from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

user = get_user_model()


class TestM(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.user = user.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='TestGroup',
            slug='TG',
            description='DESC',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='TEST POST ' * 10,
        )

    def test_objects_names(self):
        group_obj = Group.objects.latest('pk')
        title = group_obj.title
        slug = group_obj.slug
        desc = group_obj.description
        g_str = group_obj.__str__()

        self.assertEqual(title, self.group.title, 'title группы неверный')
        self.assertEqual(slug, self.group.slug, 'slug группы неверный')
        self.assertEqual(desc, self.group.description, 'desc группы неверный')
        self.assertEqual(
            group_obj._meta.get_field('title').verbose_name,
            self.group._meta.get_field('title').verbose_name,
            'title.verbose_name группы неверный'
        )
        self.assertEqual(
            group_obj._meta.get_field('title').help_text,
            self.group._meta.get_field('title').help_text,
            'title.help_text группы неверный'
        )
        self.assertEqual(
            group_obj._meta.get_field('slug').verbose_name,
            self.group._meta.get_field('slug').verbose_name,
            'slug.verbose_name группы неверный'
        )
        self.assertEqual(
            group_obj._meta.get_field('slug').help_text,
            self.group._meta.get_field('slug').help_text,
            'slug.help_text группы неверный'
        )
        self.assertEqual(
            group_obj._meta.get_field('description').verbose_name,
            self.group._meta.get_field('description').verbose_name,
            'description.verbose_name группы неверный'
        )
        self.assertEqual(
            group_obj._meta.get_field('description').help_text,
            self.group._meta.get_field('description').help_text,
            'description.help_text группы неверный'
        )
        self.assertEqual(g_str, title, '__str__ группы неверный')

    def test_post_model(self):

        post_obj = Post.objects.latest('pk')
        author = post_obj.author
        text = post_obj.text
        p_str = post_obj.__str__()

        self.assertEqual(author, TestM.user, 'user поста неверный')
        self.assertEqual(text, self.post.text, 'text поста неверный')
        self.assertEqual(
            post_obj._meta.get_field('text').verbose_name,
            self.post._meta.get_field('text').verbose_name,
            'text.verbose_name поста неверный'
        )
        self.assertEqual(
            post_obj._meta.get_field('text').help_text,
            self.post._meta.get_field('text').help_text,
            'text.help_text поста неверный'
        )
        self.assertEqual(
            post_obj._meta.get_field('group').verbose_name,
            self.post._meta.get_field('group').verbose_name,
            'group.verbose_name поста неверный'
        )
        self.assertEqual(
            post_obj._meta.get_field('group').help_text,
            self.post._meta.get_field('group').help_text,
            'group.help_text поста неверный'
        )
        self.assertEqual(p_str, text[:15], '__str__ поста неверный')
