from notes.forms import NoteForm
from notes.models import Note

from .test_dry import (
    BaseClassTest,
)


class TestContent(BaseClassTest):

    def test_notes_in_context(self):
        response = self.client_author.get(self.NOTE_LIST_URL)
        self.assertIn(self.note, response.context['object_list'])
        note_in_list = Note.objects.get()
        self.assertEqual(note_in_list.title, self.note.title)
        self.assertEqual(note_in_list.text, self.note.text)
        self.assertEqual(note_in_list.slug, self.note.slug)
        self.assertEqual(note_in_list.author, self.note.author)

    def test_notes_list_for_author(self):
        response = self.client_author.get(self.NOTE_LIST_URL)
        self.assertIn(self.note, response.context['object_list'])

    def test_pages_contains_form(self):
        urls = (
            (self.NOTE_ADD_URL),
            (self.NOTE_EDIT_URL),
        )
        for name in urls:
            with self.subTest(name=name):
                response = self.client_author.get(name)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
