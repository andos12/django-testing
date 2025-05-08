import pytest

from http import HTTPStatus

from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'url_fixture, parametrized_client, expected_status, method',
    (
        (pytest.lazy_fixture('home_url'),
            pytest.lazy_fixture('anonymous'), HTTPStatus.OK, 'get'),
        (pytest.lazy_fixture('detail_url'),
            pytest.lazy_fixture('anonymous'), HTTPStatus.OK, 'get'),
        (pytest.lazy_fixture('login_url'),
            pytest.lazy_fixture('anonymous'), HTTPStatus.OK, 'get'),
        (pytest.lazy_fixture('signup_url'),
            pytest.lazy_fixture('anonymous'), HTTPStatus.OK, 'get'),
        (pytest.lazy_fixture('logout_url'),
            pytest.lazy_fixture('anonymous'), HTTPStatus.OK, 'post'),
        (pytest.lazy_fixture('edit_url'),
            pytest.lazy_fixture('author_client'), HTTPStatus.OK, 'get'),
        (pytest.lazy_fixture('delete_url'),
            pytest.lazy_fixture('author_client'), HTTPStatus.OK, 'get'),
        (pytest.lazy_fixture('edit_url'),
            pytest.lazy_fixture('not_author_client'),
            HTTPStatus.NOT_FOUND, 'get'),
        (pytest.lazy_fixture('delete_url'),
            pytest.lazy_fixture('not_author_client'),
            HTTPStatus.NOT_FOUND, 'get'),

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
    'url_fixture, expected_url, parametrized_client',
    (
        (pytest.lazy_fixture('edit_url'), pytest.lazy_fixture('login_url'),
            pytest.lazy_fixture('anonymous')),
        (pytest.lazy_fixture('delete_url'), pytest.lazy_fixture('login_url'),
            pytest.lazy_fixture('anonymous')),
    )
)
def test_redirect(url_fixture, parametrized_client, login_url, expected_url):
    expected_url = f'{login_url}?next={url_fixture}'
    response = parametrized_client.get(url_fixture)
    assertRedirects(response, expected_url)
