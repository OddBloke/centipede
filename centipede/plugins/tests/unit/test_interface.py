from nose.tools import assert_raises

from centipede.plugins import PluginInterface


def test_get():
    assert_raises(NotImplementedError, PluginInterface().get, 'id')
