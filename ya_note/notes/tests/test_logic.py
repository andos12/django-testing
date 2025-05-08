from http import HTTPStatus

from pytils.translit import slugify

from notes.forms import WARNING
from notes.models import Note

from .test_dry import (
    BaseClassTest,
    NOTE_ADD_URL,
    NOTE_SUCCESS_URL,
    get_note_delete_url,
    get_note_edit_url
)


class TestLogic(BaseClassTest):
    def test_anonymous_user_cant_create_note(self):
        Note.objects.all().delete()
        form = self.form_data()
        self.client.post(NOTE_ADD_URL, data=form)
        self.assertEqual(Note.objects.count(), 0)

    def test_user_can_create_note(self):
        Note.objects.all().delete()
        form = self.form_data()
        self.force_login_author()
        self.client.post(NOTE_ADD_URL, data=form)
        self.assertEqual(Note.objects.count(), 1)
        note = Note.objects.get()
        self.assertEqual(note.text, form['text'])
        self.assertEqual(note.title, form['title'])
        self.assertEqual(note.slug, form['slug'])
        self.assertEqual(note.author, self.author)

    def test_not_unique_slug(self):
        current_note_before = Note.objects.get()
        form = self.form_data()
        form['slug'] = self.note.slug
        self.force_login_author()
        response = self.client.post(NOTE_ADD_URL, data=form)
        form = response.context['form']
        self.assertFormError(form, 'slug', self.note.slug + WARNING)
        current_note_after = Note.objects.get()
        self.assertEqual(current_note_after, current_note_before)

    def test_empty_slug(self):
        Note.objects.all().delete()
        form = self.form_data()
        form.pop('slug')
        self.force_login_author()
        response = self.client.post(NOTE_ADD_URL, data=form)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertEqual(Note.objects.count(), 1)
        new_note = Note.objects.get()
        expected_slug = slugify(form['title'])
        self.assertEqual(new_note.slug, expected_slug)
        self.assertEqual(new_note.text, form['text'])
        self.assertEqual(new_note.title, form['title'])
        self.assertEqual(new_note.author, self.author)

    def test_author_can_edit_note(self):
        form = self.form_data()
        self.force_login_author()
        response = self.client.post(
            get_note_edit_url(self.note.slug),
            data=form
        )
        self.assertRedirects(response, NOTE_SUCCESS_URL)
        note = Note.objects.get()
        self.assertEqual(note.title, form['title'])
        self.assertEqual(note.text, form['text'])
        self.assertEqual(note.slug, form['slug'])
        self.assertEqual(note.author, self.author)

    def test_other_user_cant_edit_note(self):
        form = self.form_data()
        self.force_login_reader()
        response = self.client.post(
            get_note_edit_url(self.note.slug),
            data=form
        )
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_from_db = Note.objects.get(id=self.note.id)
        self.assertEqual(self.note.title, note_from_db.title)
        self.assertEqual(self.note.text, note_from_db.text)
        self.assertEqual(self.note.slug, note_from_db.slug)
        self.assertEqual(self.note.author, note_from_db.author)

    def test_author_can_delete_note(self):
        current_note_count = Note.objects.count()
        self.force_login_author()
        response = self.client.delete(get_note_delete_url(self.note.slug))
        self.assertRedirects(response, NOTE_SUCCESS_URL)
        self.assertEqual(Note.objects.count(), current_note_count - 1)

    def test_other_user_cant_delete_note(self):
        current_note_before = Note.objects.get(id=self.note.id)
        self.force_login_reader()
        response = self.client.post(get_note_delete_url(self.note.slug))
        current_note_after = Note.objects.get(id=self.note.id)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(current_note_after.title, current_note_before.title)
        self.assertEqual(current_note_after.text, current_note_before.text)
        self.assertEqual(current_note_after.slug, current_note_before.slug)
        self.assertEqual(current_note_after.author, current_note_before.author)
