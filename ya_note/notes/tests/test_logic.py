from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from http import HTTPStatus

from notes.models import Note
from notes.forms import WARNING

from pytils.translit import slugify


User = get_user_model()


class TestLogic(TestCase):
    NOTE_TEXT = 'Текст заметки'

    def setUp(self):
        self.author = User.objects.create(username='Лев Толстой')
        self.form_data = {'text': self.NOTE_TEXT, 'title': 'Заголовок'}

    def test_user_can_create_note_anonymous_user_cant(self):
        url = reverse('notes:add')
        self.client.post(url, data=self.form_data)
        self.assertEqual(Note.objects.count(), 0)
        self.client.force_login(self.author)
        self.client.post(url, data=self.form_data)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.text, self.NOTE_TEXT)
        self.assertEqual(note.title, self.form_data['title'])


class TestNotSlug(TestCase):
    NOTE_TEXT = 'Текст заметки'

    def setUp(self):
        self.author = User.objects.create(username='Лев Толстой')
        self.note = Note.objects.create(
            title='Заголовок',
            text='Текст',
            author=self.author,
            slug='new-slug'
        )
        self.form_data = {
            'text': self.NOTE_TEXT,
            'title': 'Заголовок'}

    def test_not_unique_slug(self):
        self.form_data['slug'] = self.note.slug
        url = reverse('notes:add')
        self.client.force_login(self.author)
        response = self.client.post(url, data=self.form_data)
        form = response.context['form']
        self.assertFormError(form, 'slug', self.note.slug + WARNING)
        self.assertEqual(Note.objects.count(), 1)


class TestEmptySlug(TestCase):
    NOTE_TEXT = 'Текст заметки'

    def setUp(self):
        self.author = User.objects.create(username='Лев Толстой')
        self.form_data = {
            'text': self.NOTE_TEXT,
            'title': 'Заголовок'}

    def test_empty_slug(self):
        url = reverse('notes:add')
        self.client.force_login(self.author)
        response = self.client.post(url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)


class TestContent(TestCase):
    NOTE_TEXT = 'Текст заметки'

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Лев Толстой')
        cls.author_2 = User.objects.create(username='Александр Пушкин')
        cls.note = Note.objects.create(
            title="Тестовая заметка",
            text="Текст заметки",
            author=cls.author,
        )
        cls.form_data = {
            'text': cls.NOTE_TEXT,
            'title': 'Заголовок',
            'slug': 'new-slug'}

    def test_author_can_edit_note(self):
        url = reverse('notes:edit', args=[self.note.slug])
        self.client.force_login(self.author)
        response = self.client.post(url, data=self.form_data)
        self.assertRedirects(response, reverse('notes:success'))
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, self.form_data['title'])
        self.assertEqual(self.note.text, self.form_data['text'])
        self.assertEqual(self.note.slug, self.form_data['slug'])

    def test_other_user_cant_edit_note(self):
        url = reverse('notes:edit', args=[self.note.slug])
        self.client.force_login(self.author_2)
        response = self.client.post(url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)

    def test_author_can_delete_note(self):
        url = reverse('notes:delete', args=[self.note.slug])
        self.client.force_login(self.author)
        response = self.client.post(url)
        self.assertRedirects(response, reverse('notes:success'))
        self.assertEqual(Note.objects.count(), 0)

    def test_other_user_cant_delete_note(self):
        url = reverse('notes:delete', args=[self.note.slug])
        self.client.force_login(self.author_2)
        response = self.client.post(url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(Note.objects.count(), 1)
