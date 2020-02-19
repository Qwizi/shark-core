import pytest
from accounts.tests.fixtures import *


@pytest.mark.django_db
def test_queue_create(
        create_user, create_queue
):
    user = create_user()
    queue = create_queue(
        account=user
    )

    assert queue.account == user
