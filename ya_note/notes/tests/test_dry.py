from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()

NOTE_LIST_URL = reverse('notes:list')
NOTE_ADD_URL = reverse('notes:add')
NOTE_SUCCESS_URL = reverse('notes:success')
NOTE_HOME_URL = reverse('notes:home')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')


def get_note_edit_url(slug):
    return reverse('notes:edit', args=(slug,))


def get_note_delete_url(slug):
    return reverse('notes:delete', args=(slug,))


def get_note_detail_url(slug):
    return reverse('notes:detail', args=(slug,))


class BaseClassTest(TestCase):
    NOTE_TEXT = 'Текст заметки'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title="Тестовая заметка",
            text="Текст заметки",
            author=cls.author
        )

    def force_login_author(self):
        self.client.force_login(self.author)

    def force_login_reader(self):
        self.client.force_login(self.reader)

    def form_data(self):
        self.form_data = {
            'text': self.NOTE_TEXT,
            'title': 'Заголовок',
            'slug': 'new-slug'
        }
        return self.form_data
