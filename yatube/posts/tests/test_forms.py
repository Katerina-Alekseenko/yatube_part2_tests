from http import HTTPStatus
from django.test import Client, TestCase
from django.urls import reverse

from ..models import Group, Post, User


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create(username='NoName')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост',
        )
        cls.group = Group.objects.create(
            title='test_title',
            slug='first',
            description='test_description'
        )
        cls.post_edit = Post.objects.create(
            text='Тестовый текст',
            author=cls.user,
            group=cls.group
        )
        cls.group_edit = Group.objects.create(
            title='Тестовая группа',
            slug='test-group',
            description='Описание'
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_create_post(self):
        """Проверка формы создания нового поста."""
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Текст из формы',
            'group': self.group.id,
        }
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': f'{self.user}'})
        )
        self.assertEqual(Post.objects.count(), posts_count + 1)
        self.assertTrue(Post.objects.filter(
            text='Текст из формы',
            author=self.user,
            group=self.group.id,).exists()
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_post(self):
        """Проверка формы редактирования поста"""
        old_text = self.post_edit
        form_data = {'text': 'Текст записанный в форму',
                     'group': self.group_edit.id}
        response = self.authorized_client.post(
            reverse('posts:post_edit', kwargs={'post_id': self.post_edit.pk}),
            data=form_data,
            follow=True,
        )
        error_post = 'Данные поста не совпадают'
        self.assertTrue(Post.objects.filter(
            author=self.user,
            group=self.group_edit.id,
            pub_date=self.post_edit.pub_date).exists(), error_post
        )
        error_change = 'Пользователь не может изменить содержание поста'
        self.assertNotEqual(old_text.text, form_data['text'], error_change)
        self.assertEqual(response.status_code, HTTPStatus.OK)
