from . import util
from pyokc import User


@util.use_cassette('user_no_picture')
def test_handle_no_pictures():
    assert isinstance(User().username, str)


@util.use_cassette('user_get_threads')
def test_get_inbox():
    user = User()
    assert len(user.inbox.items) == 2

    for message_thread in user.inbox:
        for message in message_thread.messages:
            assert hasattr(message, 'sender')


@util.use_cassette('access_profile_from_message_thread')
def test_message_thread_to_profile():
    profile = User().inbox[0].correspondent_profile
    assert profile.age
    assert profile.age > 18
    assert isinstance(profile.rating, int)
