from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from notes.models import Note

User = get_user_model()


SLUG = 'new-slug'
NOTE_LIST_URL = reverse('notes:list')
NOTE_ADD_URL = reverse('notes:add')
NOTE_SUCCESS_URL = reverse('notes:success')
NOTE_HOME_URL = reverse('notes:home')
LOGIN_URL = reverse('users:login')
LOGOUT_URL = reverse('users:logout')
SIGNUP_URL = reverse('users:signup')
NOTE_EDIT_URL = reverse('notes:edit', args=(SLUG,))
NOTE_DELETE_URL = reverse('notes:delete', args=(SLUG,))
NOTE_DETAIL_URL = reverse('notes:detail', args=(SLUG,))
LOGIN_NEXT_LIST_URL = f'{LOGIN_URL}?next={NOTE_LIST_URL}'
LOGIN_NEXT_SUCCESS_URL = f'{LOGIN_URL}?next={NOTE_SUCCESS_URL}'
LOGIN_NEXT_ADD_URL = f'{LOGIN_URL}?next={NOTE_ADD_URL}'
LOGIN_NEXT_DETAIL_URL = f'{LOGIN_URL}?next={NOTE_DETAIL_URL}'
LOGIN_NEXT_EDIT_URL = f'{LOGIN_URL}?next={NOTE_EDIT_URL}'
LOGIN_NEXT_DELETE_URL = f'{LOGIN_URL}?next={NOTE_DELETE_URL}'


class BaseClassTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.reader = User.objects.create(username='Читатель простой')
        cls.note = Note.objects.create(
            title='Тестовая заметка',
            text='Текст заметки',
            author=cls.author,
            slug=SLUG
        )
        cls.form_data = {
            'text': 'Текст заметки',
            'title': 'Новый заголовок из формы',
            'slug': 'different-slug'
        }
        cls.client_author = Client()
        cls.client_author.force_login(cls.author)
        cls.client_reader = Client()
        cls.client_reader.force_login(cls.reader)
