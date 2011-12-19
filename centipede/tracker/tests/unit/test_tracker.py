from nose.tools import assert_raises, assert_true

from centipede.tracker import load_tracker, TrackerInterface

def test_import_tracker():
    tracker = load_tracker('centipede.plugins.rally.Rally')
    assert_true(isinstance(tracker, TrackerInterface))

def test_get():
    assert_raises(NotImplementedError, TrackerInterface().get, 'id')
