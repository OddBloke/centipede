from nose.tools import assert_raises, assert_true

from centipede.tracker import load_tracker, TrackerInterface

def test_import_tracker():
    tracker = load_tracker('centipede.plugins.rally.Rally')
    assert_true(isinstance(tracker, TrackerInterface))

def test_get_ticket():
    assert_raises(NotImplementedError, TrackerInterface().get_ticket, 'id')

def test_list_root():
    assert_raises(NotImplementedError, TrackerInterface().list_root)

def test_list_children():
    assert_raises(NotImplementedError, TrackerInterface().list_children, 'id')
