from http import HTTPStatus

from .test_dry import (
    BaseClassTest,
    LOGIN_URL,
    LOGIN_NEXT_LIST_URL,
    LOGIN_NEXT_SUCCESS_URL,
    LOGIN_NEXT_ADD_URL,
    LOGIN_NEXT_DETAIL_URL,
    LOGIN_NEXT_DELETE_URL,
    LOGIN_NEXT_EDIT_URL,
    LOGOUT_URL,
    NOTE_ADD_URL,
    NOTE_DETAIL_URL,
    NOTE_DELETE_URL,
    NOTE_EDIT_URL,
    NOTE_HOME_URL,
    NOTE_LIST_URL,
    NOTE_SUCCESS_URL,
    SIGNUP_URL,
)


class TestRoutes(BaseClassTest):
    def test_response(self):
        test_list = [
            [NOTE_HOME_URL, self.client, HTTPStatus.OK, 'get'],
            [LOGIN_URL, self.client, HTTPStatus.OK, 'get'],
            [LOGOUT_URL, self.client, HTTPStatus.OK, 'post'],
            [SIGNUP_URL, self.client, HTTPStatus.OK, 'get'],
            [NOTE_LIST_URL, self.client_author, HTTPStatus.OK, 'get'],
            [NOTE_SUCCESS_URL, self.client_author, HTTPStatus.OK, 'get'],
            [NOTE_ADD_URL, self.client_author, HTTPStatus.OK, 'get'],
            [NOTE_DETAIL_URL, self.client_author,
                HTTPStatus.OK, 'get'],
            [NOTE_EDIT_URL, self.client_author,
                HTTPStatus.OK, 'get'],
            [NOTE_DELETE_URL, self.client_author,
                HTTPStatus.OK, 'get'],
            [NOTE_DETAIL_URL, self.client_reader,
                HTTPStatus.NOT_FOUND, 'get'],
            [NOTE_EDIT_URL, self.client_reader,
                HTTPStatus.NOT_FOUND, 'get'],
            [NOTE_DELETE_URL, self.client_reader,
                HTTPStatus.NOT_FOUND, 'get'],
            [NOTE_LIST_URL, self.client, HTTPStatus.FOUND, 'get'],
            [NOTE_SUCCESS_URL, self.client, HTTPStatus.FOUND, 'get'],
            [NOTE_ADD_URL, self.client, HTTPStatus.FOUND, 'get'],
            [NOTE_DETAIL_URL, self.client,
                HTTPStatus.FOUND, 'get'],
            [NOTE_EDIT_URL, self.client,
                HTTPStatus.FOUND, 'get'],
            [NOTE_DELETE_URL, self.client,
                HTTPStatus.FOUND, 'get'],
        ]

        for url, client, expected_status, method in test_list:
            with self.subTest(url=url, client=client):
                if method == 'get':
                    response = client.get(url)
                elif method == 'post':
                    response = client.post(url)
                self.assertEqual(response.status_code, expected_status)

    def test_redirects_for_anonymous(self):
        test_list = [
            [NOTE_LIST_URL, LOGIN_NEXT_LIST_URL],
            [NOTE_SUCCESS_URL, LOGIN_NEXT_SUCCESS_URL],
            [NOTE_ADD_URL, LOGIN_NEXT_ADD_URL],
            [NOTE_DETAIL_URL, LOGIN_NEXT_DETAIL_URL],
            [NOTE_EDIT_URL, LOGIN_NEXT_EDIT_URL],
            [NOTE_DELETE_URL, LOGIN_NEXT_DELETE_URL],
        ]
        for url, expected_redirect in test_list:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, expected_redirect)
