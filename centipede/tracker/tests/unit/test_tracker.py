from nose.tools import assert_raises

from centipede.tracker import TrackerInterface


def test_get():
    assert_raises(NotImplementedError, TrackerInterface().get, 'id')
