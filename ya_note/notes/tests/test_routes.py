from http import HTTPStatus

from .test_dry import (
    BaseClassTest,
    NOTE_ADD_URL,
    NOTE_SUCCESS_URL,
    NOTE_HOME_URL,
    NOTE_LIST_URL,
    LOGIN_URL,
    LOGOUT_URL,
    SIGNUP_URL,
    get_note_delete_url,
    get_note_detail_url,
    get_note_edit_url,
)


class TestRoutes(BaseClassTest):
    def test_response(self):
        test_list = [
            [NOTE_HOME_URL, None, HTTPStatus.OK, 'get'],
            [LOGIN_URL, None, HTTPStatus.OK, 'get'],
            [LOGOUT_URL, None, HTTPStatus.OK, 'post'],
            [SIGNUP_URL, None, HTTPStatus.OK, 'get'],
            [NOTE_LIST_URL, self.author, HTTPStatus.OK, 'get'],
            [NOTE_SUCCESS_URL, self.author, HTTPStatus.OK, 'get'],
            [NOTE_ADD_URL, self.author, HTTPStatus.OK, 'get'],
            [get_note_detail_url(self.note.slug), self.author,
                HTTPStatus.OK, 'get'],
            [get_note_edit_url(self.note.slug), self.author,
                HTTPStatus.OK, 'get'],
            [get_note_delete_url(self.note.slug), self.author,
                HTTPStatus.OK, 'get'],
            [get_note_detail_url(self.note.slug), self.reader,
                HTTPStatus.NOT_FOUND, 'get'],
            [get_note_edit_url(self.note.slug), self.reader,
                HTTPStatus.NOT_FOUND, 'get'],
            [get_note_delete_url(self.note.slug), self.reader,
                HTTPStatus.NOT_FOUND, 'get'],
        ]

        for url, user, expected_status, method in test_list:
            with self.subTest(url=url, user=user):
                if user is not None:
                    self.client.force_login(user)
                if method == 'get':
                    response = self.client.get(url)
                elif method == 'post':
                    response = self.client.post(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirects_for_anonymous(self):
        test_list = [
            [NOTE_LIST_URL,
                f'{LOGIN_URL}?next={NOTE_LIST_URL}'],
            [NOTE_SUCCESS_URL,
                f'{LOGIN_URL}?next={NOTE_SUCCESS_URL}'],
            [NOTE_ADD_URL,
                f'{LOGIN_URL}?next={NOTE_ADD_URL}'],
            [get_note_detail_url(self.note.slug),
                f'{LOGIN_URL}?next={get_note_detail_url(self.note.slug)}'],
            [get_note_edit_url(self.note.slug),
                f'{LOGIN_URL}?next={get_note_edit_url(self.note.slug)}'],
            [get_note_delete_url(self.note.slug),
                f'{LOGIN_URL}?next={get_note_delete_url(self.note.slug)}'],
        ]
        for url, expected_redirect in test_list:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, expected_redirect)
