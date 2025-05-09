from django.conf import settings

from news.forms import CommentForm


def test_news_count(client, home_url, news_create):
    response = client.get(home_url)
    news_on_page = response.context['object_list']
    news_create = len(news_on_page)
    assert news_create == settings.NEWS_COUNT_ON_HOME_PAGE


def test_news_order(client, home_url):
    response = client.get(home_url)
    news_on_page = response.context['object_list']
    all_dates = [news.date for news in news_on_page]
    sorted_dates = sorted(all_dates, reverse=True)
    assert sorted_dates == all_dates


def test_comments_order(client, detail_url, comment_create):
    news = comment_create
    response = client.get(detail_url)
    assert 'news' in response.context
    news = response.context['news']
    all_comments = news.comment_set.all()
    all_timestamps = [comment.created for comment in all_comments]
    sorted_timestamps = sorted(all_timestamps)
    assert sorted_timestamps == all_timestamps


def test_anonymous_client_has_no_form(client, detail_url):
    response = client.get(detail_url)
    assert 'form' not in response.context


def test_authorized_client_has_form(author_client, detail_url):
    response = author_client.get(detail_url)
    assert 'form' in response.context
    assert isinstance(response.context['form'], CommentForm)
