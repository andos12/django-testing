from notes.forms import NoteForm

from .test_dry import (
    BaseClassTest,
    NOTE_ADD_URL,
    NOTE_EDIT_URL,
    NOTE_LIST_URL
)


class TestContent(BaseClassTest):

    def test_notes_in_context(self):
        response = self.client_author.get(NOTE_LIST_URL)
        notes = response.context['object_list']
        self.assertIn(self.note, notes)
        note_from_context = notes.get(id=self.note.id)
        self.assertEqual(note_from_context.title, self.note.title)
        self.assertEqual(note_from_context.text, self.note.text)
        self.assertEqual(note_from_context.slug, self.note.slug)
        self.assertEqual(note_from_context.author, self.note.author)

    def test_notes_not_in_context_for_another_user(self):
        response = self.client_reader.get(NOTE_LIST_URL)
        self.assertNotIn(self.note, response.context['object_list'])

    def test_pages_contains_form(self):
        urls = (
            (NOTE_ADD_URL),
            (NOTE_EDIT_URL),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client_author.get(url)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
