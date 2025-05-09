from http import HTTPStatus

from .test_dry import (
    BaseClassTest
)


class TestRoutes(BaseClassTest):
    def test_response(self):
        test_list = [
            [self.NOTE_HOME_URL, self.client, HTTPStatus.OK, 'get'],
            [self.LOGIN_URL, self.client, HTTPStatus.OK, 'get'],
            [self.LOGOUT_URL, self.client, HTTPStatus.OK, 'post'],
            [self.SIGNUP_URL, self.client, HTTPStatus.OK, 'get'],
            [self.NOTE_LIST_URL, self.client_author, HTTPStatus.OK, 'get'],
            [self.NOTE_SUCCESS_URL, self.client_author, HTTPStatus.OK, 'get'],
            [self.NOTE_ADD_URL, self.client_author, HTTPStatus.OK, 'get'],
            [self.NOTE_DETAIL_URL, self.client_author,
                HTTPStatus.OK, 'get'],
            [self.NOTE_EDIT_URL, self.client_author,
                HTTPStatus.OK, 'get'],
            [self.NOTE_DELETE_URL, self.client_author,
                HTTPStatus.OK, 'get'],
            [self.NOTE_DETAIL_URL, self.client_reader,
                HTTPStatus.NOT_FOUND, 'get'],
            [self.NOTE_EDIT_URL, self.client_reader,
                HTTPStatus.NOT_FOUND, 'get'],
            [self.NOTE_DELETE_URL, self.client_reader,
                HTTPStatus.NOT_FOUND, 'get'],
            [self.NOTE_LIST_URL, self.client, HTTPStatus.FOUND, 'get'],
            [self.NOTE_SUCCESS_URL, self.client, HTTPStatus.FOUND, 'get'],
            [self.NOTE_ADD_URL, self.client, HTTPStatus.FOUND, 'get'],
            [self.NOTE_DETAIL_URL, self.client,
                HTTPStatus.FOUND, 'get'],
            [self.NOTE_EDIT_URL, self.client,
                HTTPStatus.FOUND, 'get'],
            [self.NOTE_DELETE_URL, self.client,
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
            [self.NOTE_LIST_URL, self.login_next_list_url],
            [self.NOTE_SUCCESS_URL, self.login_next_success_url],
            [self.NOTE_ADD_URL, self.login_next_add_url],
            [self.NOTE_DETAIL_URL, self.login_next_detail_url],
            [self.NOTE_EDIT_URL, self.login_next_edit_url],
            [self.NOTE_DELETE_URL, self.login_next_delete_url],
        ]
        for url, expected_redirect in test_list:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertRedirects(response, expected_redirect)
