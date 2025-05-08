from http import HTTPStatus

from notes.forms import NoteForm

from .test_dry import (
    BaseClassTest,
    NOTE_LIST_URL,
    NOTE_ADD_URL,
    get_note_edit_url
)


class TestContent(BaseClassTest):

    def test_notes_in_context(self):
        self.force_login_author()
        response = self.client.get(NOTE_LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn(self.note, response.context['object_list'])

    def test_notes_list_for_different_users(self):
        self.force_login_reader()
        response = self.client.get(NOTE_LIST_URL)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_pages_contains_form(self):
        urls = (
            (NOTE_ADD_URL, None),
            (get_note_edit_url(self.note.slug), None),
        )
        self.force_login_author()
        for name, args in urls:
            with self.subTest(name=name, args=args):
                response = self.client.get(name)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
