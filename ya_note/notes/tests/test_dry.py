from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()

# NOTE_LIST_URL = reverse('notes:list')
# NOTE_ADD_URL = reverse('notes:add')
# NOTE_SUCCESS_URL = reverse('notes:success')
# NOTE_HOME_URL = reverse('notes:home')
# LOGIN_URL = reverse('users:login')
# LOGOUT_URL = reverse('users:logout')
# SIGNUP_URL = reverse('users:signup')
# NOTE_EDIT_URL = lambda slug: reverse('notes:edit', args=(slug,))
# NOTE_DELETE_URL = lambda slug: reverse('notes:delete', args=(slug,))
# NOTE_DETAIL_URL = lambda slug: reverse('notes:detail', args=(slug,))


class BaseClassTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title="Тестовая заметка",
            text="Текст заметки",
            author=cls.author
        )
        cls.form_data = {
            'text': 'Текст заметки',
            'title': 'Заголовок',
            'slug': 'new-slug'
        }
        cls.NOTE_LIST_URL = reverse('notes:list')
        cls.NOTE_ADD_URL = reverse('notes:add')
        cls.NOTE_SUCCESS_URL = reverse('notes:success')
        cls.NOTE_HOME_URL = reverse('notes:home')
        cls.LOGIN_URL = reverse('users:login')
        cls.LOGOUT_URL = reverse('users:logout')
        cls.SIGNUP_URL = reverse('users:signup')
        cls.NOTE_EDIT_URL = reverse('notes:edit', args=(cls.note.slug,))
        cls.NOTE_DELETE_URL = reverse('notes:delete', args=(cls.note.slug,))
        cls.NOTE_DETAIL_URL = reverse('notes:detail', args=(cls.note.slug,))
        cls.login_next_list_url = f'{cls.LOGIN_URL}?next={cls.NOTE_LIST_URL}'
        cls.login_next_success_url = f'{cls.LOGIN_URL}?next={
            cls.NOTE_SUCCESS_URL}'
        cls.login_next_add_url = f'{cls.LOGIN_URL}?next={cls.NOTE_ADD_URL}'
        cls.login_next_detail_url = f'{cls.LOGIN_URL}?next={
            cls.NOTE_DETAIL_URL}'
        cls.login_next_edit_url = f'{cls.LOGIN_URL}?next={cls.NOTE_EDIT_URL}'
        cls.login_next_delete_url = f'{cls.LOGIN_URL}?next={
            cls.NOTE_DELETE_URL}'

    def setUp(self):
        super().setUp()
        self.client_author = Client()
        self.client_author.force_login(self.author)
        self.client_reader = Client()
        self.client_reader.force_login(self.reader)
