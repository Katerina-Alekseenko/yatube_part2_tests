from django.contrib.auth import get_user_model
from django.test import TestCase

from ..models import Group, Post

User = get_user_model()

NUMBER_OF_POSTS = 15


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='NoName')
        cls.group = Group.objects.create(
            title='test_title',
            description='test_description',
            slug='test_slug',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая пост',
        )

    def test_models_have_correct_object_names(self):
        """Проверяем, что у моделей корректно работает __str__."""
        post = PostModelTest.post
        expected_object = post.text[:NUMBER_OF_POSTS]
        self.assertEqual(expected_object, str(post.text[:NUMBER_OF_POSTS]))

    def test_verbose_name(self):
        """verbose_name в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        verbose_group = post._meta.get_field('group').verbose_name
        verbose_author = post._meta.get_field('author').verbose_name
        self.assertEqual('Группа постов', verbose_group)
        self.assertEqual('Автор', verbose_author)

    def test_help_text(self):
        """help_text в полях совпадает с ожидаемым."""
        post = PostModelTest.post
        help_text_group = post.text
        self.assertEqual(help_text_group, str(post))
