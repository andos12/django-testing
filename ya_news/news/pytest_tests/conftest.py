from datetime import datetime, timedelta

import pytest
from django.test.client import Client
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from news.models import News, Comment


@pytest.fixture
def news():
    news = News.objects.create(
        title='Заголовок',
        text='Просто текст.',
    )
    return news


@pytest.fixture
def author(django_user_model):
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):
    client = Client()
    client.force_login(author)
    return client


@pytest.fixture
def not_author_client(not_author):
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def comment(author, news):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text='Просто текст.'
    )
    return comment


@pytest.fixture
def news_selection():
    today = datetime.today()
    News.objects.bulk_create(
        News(
            title='Заголовок',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    )


@pytest.fixture
def comment_selection(news, author):
    comments = []
    for index in range(10):
        comment = Comment.objects.create(
            news=news,
            author=author,
            text='Просто комментарий'
        )
    comment.created = timezone.now() + timedelta(days=index)
    comment.save()
    comments.append(comment)
    return comments


@pytest.fixture
def home_url():
    return reverse('news:home')


@pytest.fixture
def detail_url(news):
    return reverse('news:detail', args=(news.pk,))


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    pass


@pytest.fixture
def edit_url(comment):
    return reverse('news:edit', args=(comment.pk,))


@pytest.fixture
def delete_url(comment):
    return reverse('news:delete', args=(comment.pk,))


@pytest.fixture
def login_url():
    return reverse('users:login')


@pytest.fixture
def signup_url():
    return reverse('users:signup')


@pytest.fixture
def logout_url():
    return reverse('users:logout')


@pytest.fixture
def edit_url_redirect(edit_url, login_url):
    return f'{login_url}?next={edit_url}'


@pytest.fixture
def delete_url_redirect(delete_url, login_url):
    return f'{login_url}?next={delete_url}'


@pytest.fixture
def detail_url_comment(detail_url):
    return f'{detail_url}#comments'
