import pytest
from accounts.tests.fixtures import *
from django.shortcuts import reverse

from ..views import (
    NewsListView,
    NewsDetailView
)


@pytest.mark.django_db
def test_news_list_view(
        api_factory
):
    view = NewsListView.as_view()
    request = api_factory.get(reverse('api:news:list'))
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_news_detail_view(
        api_factory, create_news
):
    news = create_news()
    view = NewsDetailView.as_view()
    request = api_factory.get(reverse('api:news:detail', kwargs={'pk': news.pk}))
    response = view(request, pk=news.pk)

    assert response.status_code == 200


@pytest.mark.django_db
def test_news_list_renders(
        api_client, create_news
):
    news = create_news(
        title='News 1',
        content='News content'
    )

    response = api_client.get(reverse('api:news:list'))

    assert response.status_code == 200
    assert response.data['results'][0]['title'] == news.title
    assert response.data['results'][0]['content'] == news.content


@pytest.mark.django_db
def test_news_detail_renders(
        api_client, create_news
):
    news = create_news(
        title='News 1',
        content='News content'
    )

    response = api_client.get(reverse('api:news:detail', kwargs={'pk': news.pk}))

    assert response.status_code == 200
    assert response.data['title'] == news.title
    assert response.data['content'] == news.content
