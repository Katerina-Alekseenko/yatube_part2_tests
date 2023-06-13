from http import HTTPStatus
from django.test import Client, TestCase

from ..models import Group, Post, User


class StaticURLTests(TestCase):
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
            slug='test_slug',
            description='test_description',
        )

    def setUp(self):
        self.guest_client = Client()
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_for_authorized_exists(self):
        """Страница доступна авторизованным пользователям."""
        testing_urls = '/create/'
        response = self.authorized_client.get(testing_urls)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_edit_url_for_author_exists(self):
        """Cтраница редактирования поста доступна только автору поста"""
        testing_url = f'/posts/{self.post.id}/edit/'
        response = self.authorized_client.get(testing_url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            'posts/index.html': '/',
            'posts/group_list.html': f'/group/{self.group.slug}/',
            'posts/profile.html': f'/profile/{self.user}/',
            'posts/post_detail.html': f'/posts/{self.post.id}/',
            'posts/create_post.html': '/create/',
        }
        for template, address in templates_url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertTemplateUsed(response, template)

    def test_unexisting_page_404(self):
        response = self.guest_client.get('/n0t_ex15ting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
