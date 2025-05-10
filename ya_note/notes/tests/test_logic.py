from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note
from .test_dry import (
    BaseClassTest,
    NOTE_ADD_URL,
    NOTE_DELETE_URL,
    NOTE_EDIT_URL,
    NOTE_SUCCESS_URL
)


class TestLogic(BaseClassTest):
    def test_anonymous_user_cant_create_note(self):
        Note.objects.all().delete()
        self.client.post(NOTE_ADD_URL, data=self.form_data)
        self.assertEqual(Note.objects.count(), 0)

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        response = self.client_author.post(NOTE_ADD_URL, data=self.form_data)
        self.assertRedirects(response, NOTE_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.slug, self.form_data['slug'])
        self.assertEqual(new_note.author, self.author)

    def test_not_unique_slug(self):
        self.form_data['slug'] = self.note.slug
        notes_before = list(Note.objects.order_by('id'))
        response = self.client_author.post(
            NOTE_ADD_URL, data=self.form_data)
        self.assertFormError(
            response.context['form'],
            'slug',
            self.note.slug + WARNING
        )
        notes_after = list(Note.objects.order_by('id'))
        self.assertListEqual(notes_after, notes_before)

    def test_empty_slug(self):
        Note.objects.all().delete()
        self.form_data['slug'] = ''
        response = self.client_author.post(
            NOTE_ADD_URL, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.first()
        expected_slug = slugify(self.form_data['title'])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.text, self.form_data['text'])
        self.assertEqual(new_note.title, self.form_data['title'])
        self.assertEqual(new_note.author, self.author)

    def test_author_can_edit_note(self):
        response = self.client_author.post(
            NOTE_EDIT_URL,
            data=self.form_data
        )
        self.assertRedirects(response, NOTE_SUCCESS_URL)
        note_after = Note.objects.get(id=self.note.id)
        self.assertEqual(note_after.title, self.form_data['title'])
        self.assertEqual(note_after.text, self.form_data['text'])
        self.assertEqual(note_after.slug, self.form_data['slug'])
        self.assertEqual(note_after.author, self.note.author)

    def test_client_reader_cant_edit_note_from_client_author(self):
        response = self.client_reader.post(
            NOTE_EDIT_URL,
            data=self.form_data
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_author_can_delete_note(self):
        current_note_count = Note.objects.count()
        response = self.client_author.delete(NOTE_DELETE_URL)
        self.assertRedirects(response, NOTE_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), current_note_count - 1)
        self.assertFalse(Note.objects.filter(slug=self.note.slug).exists())

    def test_client_reader_cant_delete_note_from_client_author(self):
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())
        response = self.client_reader.post(NOTE_DELETE_URL)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertTrue(Note.objects.filter(id=self.note.id).exists())
        current_note_after = Note.objects.get(id=self.note.id)
        self.assertEqual(current_note_after.title, self.note.title)
        self.assertEqual(current_note_after.text, self.note.text)
        self.assertEqual(current_note_after.slug, self.note.slug)
        self.assertEqual(current_note_after.author, self.note.author)
