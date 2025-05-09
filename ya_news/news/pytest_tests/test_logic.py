import pytest
from pytest_django.asserts import assertRedirects
from news.forms import BAD_WORDS, WARNING
from news.models import Comment

from http import HTTPStatus

FORM_DATA = {'text': 'Текст'}

BAD_WORDS_FORM_DATA = {'text': 'Какой-то текст, {bad_word}, еще текст'}


def get_bad_words_data(bad_word):
    return {
        'text': BAD_WORDS_FORM_DATA['text'].format(bad_word=bad_word)
    }


def test_anonymous_user_cant_create_comment(client, detail_url):
    client.post(detail_url, data=FORM_DATA)
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_user_can_create_comment(author_client, author, news, detail_url):
    author_client.post(detail_url, data=FORM_DATA)
    comments_count = Comment.objects.count()
    assert comments_count == 1
    comment = Comment.objects.get()
    assert comment.news == news
    assert comment.author == author
    assert comment.text == FORM_DATA['text']


@pytest.mark.parametrize('bad_word', BAD_WORDS)
def test_user_cant_use_bad_words(author_client, detail_url, bad_word):
    response = author_client.post(
        detail_url,
        data=get_bad_words_data(bad_word)
    )
    assert 'form' in response.context
    form = response.context['form']
    assert WARNING in form.errors['text']
    comments_count = Comment.objects.count()
    assert comments_count == 0


def test_author_can_delete_comment(author_client, delete_url):
    author_client.delete(delete_url, FORM_DATA)
    assert Comment.objects.count() == 0


def test_author_can_edit_comment(author_client, comment, edit_url, detail_url):
    response = author_client.post(edit_url, FORM_DATA)
    assertRedirects(response, f"{detail_url}#comments")
    comment_updated = Comment.objects.get()
    assert comment_updated.text == FORM_DATA['text']
    assert comment_updated.author == comment.author
    assert comment_updated.news == comment.news


def test_user_cant_edit_comment_of_another_user(
        not_author_client, comment, edit_url):
    current_text = comment.text
    response = not_author_client.post(edit_url, FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    note_from_db = Comment.objects.get(id=comment.id)
    assert note_from_db.text == current_text
    assert note_from_db.author == comment.author
    assert note_from_db.news == comment.news


def test_user_cant_delete_comment_of_another_user(
        not_author_client, comment, delete_url):
    comment_count = Comment.objects.count()
    response = not_author_client.delete(delete_url, FORM_DATA)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert comment_count == 1
