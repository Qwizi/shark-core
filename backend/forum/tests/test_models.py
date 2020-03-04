import pytest
from accounts.tests.fixtures import *


@pytest.mark.django_db
@pytest.mark.parametrize(
    'name', [
        pytest.param(
            'Testowa kategoria'
        )
    ]
)
def test_category_create(
        name, create_category
):
    category = create_category()

    assert category.name == name


@pytest.mark.django_db
@pytest.mark.parametrize(
    'category_name, thread_title, thread_content, author_username', [
        pytest.param(
            'Testowa kategoria', 'Testowy temat', 'Testowa tresc', 'Qwizi'
        )
    ]
)
def test_thread_create(
        category_name, thread_title, thread_content, author_username, create_thread
):
    thread = create_thread(title='Testowy temat', content='Testowa tresc')

    assert thread.category.name == category_name
    assert thread.title == thread_title
    assert thread.content == thread_content
    assert thread.author.username == author_username


@pytest.mark.django_db
@pytest.mark.parametrize(
    'pinned', [
        pytest.param(
            True
        )
    ]
)
def test_thread_pin(
        pinned, create_thread
):
    thread = create_thread()

    thread.pin()

    assert thread.pinned == pinned


@pytest.mark.django_db
@pytest.mark.parametrize(
    'pinned', [
        pytest.param(
            False
        )
    ]
)
def test_thread_unpin(
        pinned, create_thread
):
    thread = create_thread()

    thread.unpin()

    assert thread.pinned == pinned


@pytest.mark.django_db
@pytest.mark.parametrize(
    'status', [
        pytest.param(
            Thread.ThreadStatusChoices.OPENED
        )
    ]
)
def test_thread_open(
        status, create_thread
):
    thread = create_thread()

    thread.open()

    assert thread.status == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'status', [
        pytest.param(
            Thread.ThreadStatusChoices.CLOSED
        )
    ]
)
def test_thread_close(
        status, create_thread
):
    thread = create_thread()

    thread.close()

    assert thread.status == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'status', [
        pytest.param(
            Thread.ThreadStatusChoices.HIDDEN
        )
    ]
)
def test_thread_hide(
        status, create_thread
):
    thread = create_thread()

    thread.hide()

    assert thread.status == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'content, thread_title', [
        pytest.param(
            'Testowa tresc', 'Testowy temat'
        )
    ]
)
def test_post_create(
        content, thread_title, create_post
):
    post = create_post(content='Testowa tresc')

    assert post.content == content
    assert post.thread.title == thread_title


@pytest.mark.django_db
@pytest.mark.parametrize(
    'status', [
        pytest.param(
            Post.PostStatusChoices.VISIBLE
        )
    ]
)
def test_post_visible(
        status, create_post
):
    post = create_post()

    post.visible()

    assert post.status == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'status', [
        pytest.param(
            Post.PostStatusChoices.HIDDEN
        )
    ]
)
def test_post_hide(
        status, create_post
):
    post = create_post()

    post.hide()

    assert post.status == status


@pytest.mark.django_db
@pytest.mark.parametrize(
    'last_poster_username', [
        pytest.param(
            'Qwizi'
        )
    ]
)
def test_post_update_thread_last_poster(
        last_poster_username, create_thread, create_post
):
    thread = create_thread()

    post = create_post(thread=thread)

    post.update_thread_last_poster()

    assert post.thread.last_poster.username == last_poster_username


@pytest.mark.django_db
@pytest.mark.parametrize(
    'count, name, tag, image', [
        pytest.param(
            1, 'Sad', 'sad', 'https://www.cdn.pecetowicz.pl/reactions/sad.png'
        )
    ]
)
def test_reactionitem_create(
        count, name, tag, image, create_reactionitem
):
    reactionitem = create_reactionitem(
        name="Sad",
        tag='sad',
        image=File('https://www.cdn.pecetowicz.pl/reactions/sad.png')
    )

    assert ReactionItem.objects.all().count() == count
    assert reactionitem.name == name
    assert reactionitem.tag == tag
    assert reactionitem.image == File(image)


@pytest.mark.django_db
@pytest.mark.parametrize(
    'count, name, tag, image, username', [
        pytest.param(
            1, 'Sad', 'sad', 'https://www.cdn.pecetowicz.pl/reactions/sad.png', 'Qwizi'
        )
    ]
)
def test_reaction_create(
        count, name, tag, image, username, create_reactionitem, create_user, create_reaction
):
    item = create_reactionitem(
        name='Sad',
        tag='sad',
        image=File('https://www.cdn.pecetowicz.pl/reactions/sad.png')
    )
    user = create_user()
    reaction = create_reaction(
        item=item,
        user=user
    )
    assert Reaction.objects.all().count() == count
    assert reaction.item.name == name
    assert reaction.item.tag == tag
    assert reaction.item.image == File(image)
    assert reaction.user.username == username
