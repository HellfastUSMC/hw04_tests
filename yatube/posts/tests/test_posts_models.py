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
        group_obj = TestM.group
        title = group_obj.title
        slug = group_obj.slug
        desc = group_obj.description
        g_str = group_obj.__str__()

        post_obj = TestM.post
        author = post_obj.author
        text = post_obj.text
        p_str = post_obj.__str__()

        print('Start testing models...')

        print('Start testing groups model...')
        self.assertEqual(title, 'TestGroup', 'title группы неверный')
        self.assertEqual(slug, 'TG', 'slug группы неверный')
        self.assertEqual(desc, 'DESC', 'desc группы неверный')
        self.assertEqual(
            group_obj._meta.get_field('title').verbose_name,
            'Название группы', 'title.verbose_name группы неверный'
        )
        self.assertEqual(
            group_obj._meta.get_field('title').help_text,
            'Введите название группы', 'title.help_text группы неверный'
        )
        self.assertEqual(
            group_obj._meta.get_field('slug').verbose_name,
            'Адрес группы', 'slug.verbose_name группы неверный'
        )
        self.assertEqual(
            group_obj._meta.get_field('slug').help_text,
            'Введите адрес группы', 'slug.help_text группы неверный'
        )
        self.assertEqual(
            group_obj._meta.get_field('description').verbose_name,
            'Описание группы', 'description.verbose_name группы неверный'
        )
        self.assertEqual(
            group_obj._meta.get_field('description').help_text,
            'Введите описание группы', 'description.help_text группы неверный'
        )
        self.assertEqual(g_str, title, '__str__ группы неверный')
        print('Testing groups model done!')

        print('Start testing posts model...')
        self.assertEqual(author, TestM.user, 'user поста неверный')
        self.assertEqual(text, 'TEST POST ' * 10, 'text поста неверный')
        self.assertEqual(
            post_obj._meta.get_field('text').verbose_name,
            'Текст поста', 'text.verbose_name поста неверный'
        )
        self.assertEqual(
            post_obj._meta.get_field('text').help_text,
            'Введите текст поста в поле выше', 'text.help_text поста неверный'
        )
        self.assertEqual(
            post_obj._meta.get_field('group').verbose_name,
            'Группа поста', 'group.verbose_name поста неверный'
        )
        self.assertEqual(
            post_obj._meta.get_field('group').help_text,
            'Выберите группу', 'group.help_text поста неверный'
        )
        self.assertEqual(p_str, text[:15], '__str__ поста неверный')
        print('Testing posts model done!')

        print('Testing models done!')
