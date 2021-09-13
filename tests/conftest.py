import os
from pathlib import Path
import pytest
import json
import sqlalchemy as sa
from rasa.shared.core.domain import Domain

from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker

here = Path(__file__).parent.resolve()

# EMPTY_TRACKER = Tracker.from_dict(json.load(open(here / "./data/empty_tracker.json")))

# PAY_CC_NOT_CONFIRMED = Tracker.from_dict(
#     json.load(open(here / "./data/pay_cc_not_confirmed.json"))
# )
# PAY_CC_CONFIRMED = Tracker.from_dict(
#     json.load(open(here / "./data/pay_cc_confirmed.json"))
# )
# DATABASE_URL = os.environ.setdefault("DATABASE_URL", "postgresql:///postgres")

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
        tracker= Tracker.from_dict(tracker_state)
    return tracker