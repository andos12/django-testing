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
        object_list = response.context['object_list']
        self.assertIn(self.note, object_list)
        self.assertContains(response, self.note.title)
        first_note = object_list[0]
        self.assertIn(first_note, object_list)

    def test_notes_not_in_context_for_another_user(self):
        response = self.client_reader.get(NOTE_LIST_URL)
        self.assertNotIn(self.note, response.context['object_list'])
        self.assertNotContains(response, self.note.title)

    def test_pages_contains_form(self):
        urls = (
            (NOTE_ADD_URL),
            (NOTE_EDIT_URL),
        )
        for name in urls:
            with self.subTest(name=name):
                response = self.client_author.get(name)
                self.assertIn('form', response.context)
                self.assertIsInstance(response.context['form'], NoteForm)
