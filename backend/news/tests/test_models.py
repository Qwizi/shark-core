import pytest
from accounts.tests.fixtures import *


@pytest.mark.django_db
def test_news_create(
        create_news
):
    news = create_news(
        title='News title',
        content='News content'
    )

    assert News.objects.all().count() == 1
    assert news.title == 'News title'
    assert news.content == 'News content'
