import pytest

from http import HTTPStatus

from pytest_django.asserts import assertRedirects

CLIENT = pytest.lazy_fixture('client')
AUTHOR_CLIENT = pytest.lazy_fixture('author_client')
NOT_AUTHOR_CLIENT = pytest.lazy_fixture('not_author_client')
HOME_URL = pytest.lazy_fixture('home_url')
DETAIL_URL = pytest.lazy_fixture('detail_url')
LOGIN_URL = pytest.lazy_fixture('login_url')
SIGNUP_URL = pytest.lazy_fixture('signup_url')
LOGOUT_URL = pytest.lazy_fixture('logout_url')
EDIT_URL = pytest.lazy_fixture('edit_url')
DELETE_URL = pytest.lazy_fixture('delete_url')
EDIT_URL_REDIRECT = pytest.lazy_fixture('edit_url_redirect')
DELETE_URL_REDIRECT = pytest.lazy_fixture('delete_url_redirect')


@pytest.mark.parametrize(
    'url_fixture, parametrized_client, expected_status, method',
    (
        (HOME_URL, CLIENT, HTTPStatus.OK, 'get'),
        (DETAIL_URL, CLIENT, HTTPStatus.OK, 'get'),
        (LOGIN_URL, CLIENT, HTTPStatus.OK, 'get'),
        (SIGNUP_URL, CLIENT, HTTPStatus.OK, 'get'),
        (LOGOUT_URL, CLIENT, HTTPStatus.OK, 'post'),
        (EDIT_URL, AUTHOR_CLIENT, HTTPStatus.OK, 'get'),
        (DELETE_URL, AUTHOR_CLIENT, HTTPStatus.OK, 'get'),
        (EDIT_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND, 'get'),
        (DELETE_URL, NOT_AUTHOR_CLIENT, HTTPStatus.NOT_FOUND, 'get'),
        (EDIT_URL, CLIENT, HTTPStatus.FOUND, 'get'),
        (DELETE_URL, CLIENT, HTTPStatus.FOUND, 'get'),
    )
)
def test_status_code(
        url_fixture,
        parametrized_client,
        expected_status,
        method
):
    if method == 'post':
        response = parametrized_client.post(url_fixture)
    else:
        response = parametrized_client.get(url_fixture)
    assert response.status_code == expected_status


@pytest.mark.parametrize(
    'expected_url, url_fixture, parametrized_client',
    (
        (EDIT_URL_REDIRECT, EDIT_URL, CLIENT),
        (DELETE_URL_REDIRECT, DELETE_URL, CLIENT),
    )
)
def test_redirect(url_fixture, parametrized_client, expected_url):
    response = parametrized_client.get(url_fixture)
    assertRedirects(response, expected_url)
