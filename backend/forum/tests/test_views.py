import pytest
from django.urls import reverse
from accounts.tests.fixtures import *

from ..views import (
    CategoryListView,
    CategoryDetailView,
    ThreadListView,
    ThreadDetailView,
    ThreadReactionsListView,
    ThreadSetBestAnswerView,
    ThreadUnSetBestAnswerView,
    PostListView,
    PostDetailView,
    StatsView,
    ReactionListView
)


@pytest.mark.django_db
def test_category_list_view(
        api_factory
):
    view = CategoryListView.as_view()
    request = api_factory.get(reverse('api:forum:category-list'))
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_category_detail_view(
        api_factory, create_category
):
    category = create_category()

    view = CategoryDetailView.as_view()
    request = api_factory.get(reverse('api:forum:category-detail', kwargs={'pk': category.pk}))
    response = view(request, pk=category.pk)

    assert response.status_code == 200


@pytest.mark.django_db
def test_thread_list_view(
        api_factory
):
    view = ThreadListView.as_view()
    request = api_factory.get(reverse('api:forum:thread-list'))
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_thread_detail_view(
        api_factory, create_thread
):
    thread = create_thread()

    view = ThreadDetailView.as_view()
    request = api_factory.get(reverse('api:forum:thread-detail', kwargs={'pk': thread.pk}))
    response = view(request, pk=thread.pk)

    assert response.status_code == 200


@pytest.mark.django_db
def test_thread_create_view_without_authenticate(
        api_factory
):
    view = ThreadListView.as_view()
    request = api_factory.post(reverse('api:forum:thread-list'))
    response = view(request)

    assert response.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize(
    'title, content, category_name, status_code', [
        pytest.param(
            'Testowy temat', 'Testowa tresc', 'Testowa kategoria', 201
        )
    ]
)
def test_thread_create_view_with_authenticate(
        title, content, category_name, status_code, api_factory, create_category, create_user, get_token_for_user
):
    category = create_category(name=category_name)
    user = create_user()

    data = {
        'title': title,
        'content': content,
        'category': category.pk
    }

    view = ThreadListView.as_view()
    request = api_factory.post(reverse('api:forum:thread-list'), data=data)
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request)

    assert response.status_code == status_code


@pytest.mark.django_db
def test_thread_reaction_add_view_without_authenticate(
        api_factory
):
    view = ThreadReactionsListView.as_view()
    request = api_factory.post(reverse('api:forum:thread-reactions-list', kwargs={'thread_pk': 1}))
    response = view(request, thread_pk=1)

    assert response.status_code == 401


@pytest.mark.django_db
def test_thread_reaction_add_view(
        api_factory, create_thread, create_user, get_token_for_user, create_reactionitem,
):
    thread = create_thread()
    user = create_user()
    reaction_item = create_reactionitem(
        name='Sad',
        tag='sad'
    )

    data = {
        'reaction_item': reaction_item.pk
    }

    view = ThreadReactionsListView.as_view()
    request = api_factory.post(reverse('api:forum:thread-reactions-list', kwargs={'thread_pk': thread.pk}), data=data)
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request, thread_pk=thread.pk)

    assert response.status_code == 201


@pytest.mark.django_db
def test_thread_reaction_list_view(
        api_factory, create_thread, create_user, create_reactionitem
):
    thread = create_thread()
    user = create_user()
    reaction_item = create_reactionitem(
        name='Sad',
        tag='sad'
    )

    view = ThreadReactionsListView.as_view()
    request = api_factory.get(reverse('api:forum:thread-reactions-list', kwargs={'thread_pk': thread.pk}))
    response = view(request, thread_pk=thread.pk)

    assert response.status_code == 200


@pytest.mark.django_db
def test_post_list_view(
        api_factory
):
    view = PostListView.as_view()
    request = api_factory.get(reverse('api:forum:post-list'))
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_post_detail_view(
        api_factory, create_post
):
    post = create_post()

    view = PostDetailView.as_view()
    request = api_factory.get(reverse('api:forum:post-detail', kwargs={'pk': post.pk}))
    response = view(request, pk=post.pk)

    assert response.status_code == 200


@pytest.mark.django_db
def test_post_create_view_without_authenticate(
        api_factory
):
    view = PostListView.as_view()
    request = api_factory.post(reverse('api:forum:post-list'))
    response = view(request)

    assert response.status_code == 401


@pytest.mark.django_db
@pytest.mark.parametrize(
    'content, status_code', [
        pytest.param(
            'Testowy post', 201
        )
    ]
)
def test_post_create_view_with_authenticate(
        content, status_code, api_factory, create_thread, create_user, get_token_for_user
):
    user = create_user()
    thread = create_thread(author=user)

    data = {
        'content': content,
        'thread': thread.pk
    }

    view = PostListView.as_view()
    request = api_factory.post(reverse('api:forum:post-list'), data=data)
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request)

    assert response.status_code == status_code


@pytest.mark.django_db
def test_stats_view(
        api_factory
):
    view = StatsView.as_view()
    request = api_factory.get(reverse('api:forum:stats-list'))
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, count, status_code', [
        pytest.param(
            'Testowa kategoria', 1, 200
        )
    ]
)
def test_category_list_renders(
        name, count, status_code, api_client, create_category
):
    create_category()

    response = api_client.get(reverse('api:forum:category-list'))

    assert response.status_code == status_code
    assert response.data['count'] == count
    assert response.data['results'][0]['name'] == name


@pytest.mark.django_db
def test_reaction_list_view(
        api_factory, create_reactionitem
):
    reaction_item = create_reactionitem(
        tag='thx',
        name='Thanks',
        image='http://localhost:8000/static/reactions/thx.png'
    )

    view = ReactionListView.as_view()
    request = api_factory.get(reverse('api:forum:reactions-list'))
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_thread_set_best_answer_without_authenticate_view(
        api_factory
):
    view = ThreadSetBestAnswerView.as_view()
    request = api_factory.put(reverse('api:forum:thread-set-best-answer', kwargs={'pk': 9999}))
    response = view(request, pk=999)

    assert response.status_code == 401


@pytest.mark.django_db
def test_thread_set_best_answer_view(
        api_factory, create_user, get_token_for_user, create_thread, create_post
):
    user = create_user()
    thread = create_thread(author=user)
    post = create_post(thread=thread, author=user)

    data = {
        'post': post.pk
    }

    view = ThreadSetBestAnswerView.as_view()
    request = api_factory.put(reverse('api:forum:thread-set-best-answer', kwargs={'pk': thread.pk}), data=data)
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request, pk=thread.pk)

    assert response.status_code == 200


@pytest.mark.django
def test_thread_unset_best_answer_without_authenticate_view(
        api_factory
):
    view = ThreadUnSetBestAnswerView.as_view()
    request = api_factory.put(reverse('api:forum:thread-unset-best-answer', kwargs={'pk': 999}))
    response = view(request, pk=999)

    assert response.status_code == 401


@pytest.mark.django_db
def test_thread_unset_best_answer_view(
        api_factory, create_user, get_token_for_user, create_thread, create_post
):
    user = create_user()
    thread = create_thread(author=user)
    post = create_post(thread=thread, author=user)

    data = {
        'post': post.pk
    }

    view = ThreadUnSetBestAnswerView.as_view()
    request = api_factory.put(reverse('api:forum:thread-unset-best-answer', kwargs={'pk': thread.pk}), data=data)
    force_authenticate(request, user=user, token=get_token_for_user(user=user))
    response = view(request, pk=thread.pk)

    assert response.status_code == 200


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name, status_code', [
        pytest.param(
            'Testowa kategoria', 200
        )
    ]
)
def test_category_detail_renders(
        name, status_code, api_client, create_category
):
    category = create_category()

    response = api_client.get(reverse('api:forum:category-detail', kwargs={'pk': category.pk}))

    assert response.status_code == status_code
    assert response.data['name'] == name


@pytest.mark.django_db
@pytest.mark.parametrize(
    'count, thread_title, category_id, pinned, status_code', [
        # Tematy bez filtrow
        pytest.param(
            3, 'Testowy temat', None, None, 200
        ),
        # Tematy filtrowane po kategorii Pierwsza kategoria, nie przypiete
        pytest.param(
            2, 'Testowy temat', 1, None, 200
        ),
        # Tematy filtrowane po kategorii Druga testowa kategoria, nie przypiete
        pytest.param(
            1, 'Drugi testowy temat', 2, None, 200
        ),
        # Tematy nie filtrowane, przypiete
        pytest.param(
            1, 'Przypiety temat', None, True, 200
        ),
    ]
)
def test_thread_list_renders(
        count, thread_title, category_id, pinned, status_code, api_client, create_thread, create_category
):
    first_category = create_category(pk=1, name='Pierwsza kategoria')
    second_category = create_category(pk=2, name='Druga testowa kategoria')

    first_thread = create_thread(title='Testowy temat', category=first_category)
    second_thread = create_thread(title='Drugi testowy temat', category=second_category)

    pinned_thread = create_thread(title='Przypiety temat', category=first_category, pinned=True)

    url = reverse('api:forum:thread-list')
    if category_id:
        if pinned:
            url_full = '{}?category={}&?pinned={}'.format(url, category_id, pinned)
        else:
            url_full = '{}?category={}'.format(url, category_id)
    else:
        if pinned:
            url_full = '{}?pinned={}'.format(url, pinned)
        else:
            url_full = url

    response = api_client.get(url_full)

    assert response.status_code == status_code
    assert response.data['count'] == count
    if count:
        assert response.data['results'][0]['title'] == thread_title


@pytest.mark.django_db
@pytest.mark.parametrize(
    'title, author_username, status_code', [
        pytest.param(
            'Testowy temat', 'Qwizi', 200
        )
    ]
)
def test_thread_detail_renders(
        title, author_username, status_code, api_client, create_thread
):
    thread = create_thread(title='Testowy temat')

    response = api_client.get(reverse('api:forum:thread-detail', kwargs={'pk': thread.pk}))

    assert response.status_code == status_code
    assert response.data['title'] == title
    assert response.data['author']['username'] == author_username


@pytest.mark.django_db
@pytest.mark.parametrize(
    'title, content, status_code', [
        pytest.param(
            'Testowy temat', 'Testowa kategoria', 200
        )
    ]
)
def test_thread_create_renders(
        title, content, status_code, api_client_with_credentials, create_category
):
    category = create_category(name='Testowa kategoria')
    data = {
        'title': title,
        'content': content,
        'category': category.pk
    }
    response = api_client_with_credentials.post(reverse('api:forum:thread-list'), data=data)

    assert response.status_code == 201
    assert response.data['title'] == title
    assert response.data['content'] == content


@pytest.mark.django_db
@pytest.mark.parametrize(
    'updated_content, updated_title, status_code', [
        pytest.param(
            'Zaaktualizowana tresc', 'Zaaktualizowy tytul', 200
        )
    ]
)
def test_thread_update_renders(
        updated_content, updated_title, status_code, api_client_with_credentials, create_thread, create_user
):
    user = create_user()
    thread = create_thread(title='Normalny tytul', content='Normanla tresc', author=user)

    data = {
        'title': 'Zaaktualizowy tytul',
        'content': 'Zaaktualizowana tresc'
    }

    response = api_client_with_credentials.put(reverse('api:forum:thread-detail', kwargs={'pk': thread.pk}), data=data)

    assert response.status_code == status_code
    assert response.data['title'] == updated_title
    assert response.data['content'] == updated_content


@pytest.mark.django_dbd
def test_thread_update_renders_when_user_is_not_author(
        api_client_with_credentials, create_user, create_thread
):
    author = create_user(steamid64="76561199027497412")
    thread = create_thread(title='Normalny tytul', content='Normanla tresc', author=author)

    response = api_client_with_credentials.put(reverse('api:forum:thread-detail', kwargs={'pk': thread.pk}))

    assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    'content, count, status_code', [
        pytest.param(
            'Testowa tresc', 1, 200
        )
    ]
)
def test_post_list_renders(
        content, count, status_code, api_client, create_post
):
    create_post(content='Testowa tresc')

    response = api_client.get(reverse('api:forum:post-list'))

    assert response.status_code == status_code
    assert response.data['count'] == count
    assert response.data['results'][0]['content'] == content


@pytest.mark.django_db
@pytest.mark.parametrize(
    'content, status_code', [
        pytest.param(
            'Testowa tresc', 200
        )
    ]
)
def test_post_detail_renders(
        content, status_code, api_client, create_post
):
    post = create_post(content='Testowa tresc')

    response = api_client.get(reverse('api:forum:post-detail', kwargs={'pk': post.pk}))

    assert response.status_code == status_code
    assert response.data['content'] == content


@pytest.mark.django_db
@pytest.mark.parametrize(
    'content, status_code', [
        pytest.param(
            'Testowa tresc', 201
        )
    ]
)
def test_post_create_renders(
        content, status_code, api_client_with_credentials, create_thread, create_user
):
    user = create_user()
    thread = create_thread(author=user)
    data = {
        'content': 'Testowa tresc',
        'thread': thread.pk
    }

    response = api_client_with_credentials.post(reverse('api:forum:post-list'), data=data)

    assert response.status_code == status_code
    assert response.data['content'] == content


@pytest.mark.django_db
def test_post_create_renders_in_closed_thread(
        api_client_with_credentials, create_thread, create_user
):
    user = create_user()
    thread = create_thread(author=user, status=Thread.ThreadStatusChoices.CLOSED)
    data = {
        'content': 'Testowa tress',
        'thread': thread.pk
    }

    response = api_client_with_credentials.post(reverse('api:forum:post-list'), data=data)

    assert response.status_code == 400
    assert 'Temat w którym próbujesz napisać post jest ukryty lub zamknięty' in response.data


@pytest.mark.django_db
@pytest.mark.parametrize(
    'updated_content, status_code', [
        pytest.param(
            'Zaaktualizowana tresc', 200
        )
    ]
)
def test_post_update_renders(
        updated_content, status_code, api_client_with_credentials, create_thread, create_post, create_user
):
    user = create_user()
    thread = create_thread(author=user, status=Thread.ThreadStatusChoices.CLOSED)
    post = create_post(content='Normalna tresc', thread=thread)

    data = {
        'content': 'Zaaktualizowana tresc',
        'thread': thread.pk
    }

    response = api_client_with_credentials.put(reverse('api:forum:post-detail', kwargs={'pk': post.pk}), data=data)

    assert response.status_code == status_code
    assert response.data['content'] == updated_content


@pytest.mark.django_dbd
def test_post_update_renders_when_user_is_not_author(
        api_client_with_credentials, create_user, create_thread, create_post
):
    author = create_user(steamid64="76561199027497412")
    thread = create_thread(title='Normalny tytul', content='Normanla tresc', author=author)
    post = create_post(thread=thread, author=author)

    response = api_client_with_credentials.put(reverse('api:forum:thread-detail', kwargs={'pk': thread.pk}))

    assert response.status_code == 403


@pytest.mark.django_db
@pytest.mark.parametrize(
    'threads, posts, status_code', [
        pytest.param(
            1, 1, 200
        )
    ]
)
def test_stats_renders(
        threads, posts, status_code, api_client, create_thread, create_post
):
    thread = create_thread()
    create_post(thread=thread)

    response = api_client.get(reverse('api:forum:stats-list'))

    assert response.status_code == status_code
    assert response.data['threads'] == threads
    assert response.data['posts'] == posts


@pytest.mark.django_db
def test_thread_reaction_add_renders(
        api_client_with_credentials, create_thread, create_user, create_reactionitem
):
    thread = create_thread()
    user = create_user()
    reaction_item = create_reactionitem(
        name='Sad',
        tag='sad',
    )

    data = {
        'reaction_item': reaction_item.pk
    }

    response = api_client_with_credentials.post(
        reverse('api:forum:thread-reactions-list', kwargs={'thread_pk': thread.pk}), data=data)

    assert response.status_code == 201
    assert thread.reactions.all().count() == 1
    assert thread.reactions.all()[0].user == user
    assert thread.reactions.all()[0].item == reaction_item


@pytest.mark.django_db
def test_thread_reaction_invalid_reaction_tag_renders(
        api_client_with_credentials, create_thread
):
    thread = create_thread()

    data = {
        'reaction_item': 9999
    }

    response = api_client_with_credentials.post(
        reverse('api:forum:thread-reactions-list', kwargs={'thread_pk': thread.pk}), data=data)

    assert response.status_code == 400


@pytest.mark.django_db
def test_thread_reaction_user_already_give_reaction_renders(
        api_client_with_credentials, create_thread, create_reactionitem
):
    thread = create_thread()
    item = create_reactionitem(
        name='Sad',
        tag='sad'
    )

    data = {
        'reaction_item': item.pk
    }

    first_response = api_client_with_credentials.post(
        reverse('api:forum:thread-reactions-list', kwargs={'thread_pk': thread.pk}), data=data)
    second_response = api_client_with_credentials.post(
        reverse('api:forum:thread-reactions-list', kwargs={'thread_pk': thread.pk}), data=data)

    assert first_response.status_code == 201
    assert second_response.status_code == 400


@pytest.mark.django_db
def test_thread_reaction_list_renders(
        api_client_with_credentials, create_thread, create_reactionitem
):
    thread = create_thread()
    item = create_reactionitem(
        name='Sad',
        tag='sad',
    )

    data = {
        'reaction_item': item.pk
    }

    add_reaction_response = api_client_with_credentials.post(
        reverse('api:forum:thread-reactions-list', kwargs={'thread_pk': thread.pk}), data=data)

    response = api_client_with_credentials.get(
        reverse('api:forum:thread-reactions-list', kwargs={'thread_pk': thread.pk}))

    assert add_reaction_response.status_code == 201
    assert response.status_code == 200
    assert response.data['count'] == 1


@pytest.mark.django_db
def test_reaction_list_renders(
        api_client, create_reactionitem
):
    reaction_item = create_reactionitem(
        name='Thanks',
        tag='thx',
        image='http://localhost:3000/images/reactions/thx.png'
    )

    response = api_client.get(reverse('api:forum:reactions-list'))

    assert response.status_code == 200
    assert response.data['results'][0]['image'] == reaction_item.image


@pytest.mark.django_db
def test_thread_set_best_answer_renders(
        api_client_with_credentials, create_thread, create_post
):
    thread = create_thread()
    post = create_post(thread=thread)
    post2 = create_post(thread=thread)

    data = {
        'post': post.pk
    }

    response = api_client_with_credentials.put(reverse('api:forum:thread-set-best-answer', kwargs={'pk': thread.pk}),
                                               data=data)

    assert response.status_code == 200
    assert thread.post_set.get(pk=post.pk).best_answer is True
    assert thread.post_set.get(pk=post2.pk).best_answer is False


@pytest.mark.django_db
def test_thread_unset_best_answer_renders(
        api_client_with_credentials, create_thread, create_post
):
    thread = create_thread()
    post = create_post(thread=thread)
    post.set_best_answer()

    data = {
        'post': post.pk
    }

    response = api_client_with_credentials.put(reverse('api:forum:thread-unset-best-answer', kwargs={'pk': thread.pk}),
                                               data=data)
    assert response.status_code == 200
    assert thread.post_set.get(pk=post.pk).best_answer is False