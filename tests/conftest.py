"""
Contains shared fixtures for all tests.
"""
from pathlib import Path
import pytest
import json
from rasa.shared.core.domain import Domain

from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker

here = Path(__file__).parent.resolve()


@pytest.fixture
def tracker():
    tracker_state_dictionary = json.load(open(here / "./data/empty_tracker.json"))
    tracker = Tracker.from_dict(tracker_state_dictionary)
    return tracker


@pytest.fixture
def dispatcher():
    return CollectingDispatcher()


@pytest.fixture
def domain():
    return Domain.load(here / "../domain.yml")


def get_tracker(tracker_state="default"):
    if tracker_state == "default":
        tracker = Tracker.from_dict(json.load(open(here / "./data/empty_tracker.json")))
    else:
        tracker = Tracker.from_dict(tracker_state)
    return tracker
