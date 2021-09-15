import json
import pytest

from rasa_sdk.executor import CollectingDispatcher, Tracker
from rasa_sdk.events import SlotSet, ActionExecuted, SessionStarted, FollowupAction, AllSlotsReset

#from tests.conftest import EMPTY_TRACKER
from actions import actions

from pathlib import Path
from .conftest import get_tracker



# test tutorial switch
def test_tutorial_switch(tracker,dispatcher, domain):
    tracker_state_dictionary = json.load(open(Path(__file__).parent.resolve() / "./data/empty_tracker.json"))
    tracker_state_dictionary['slots']['controller_type'] = "avr"
    tracker_state_dictionary['slots']['tutorial_next_step'] = 3
    tracker_state_dictionary['slots']['current_tutorial'] = "led_tutorial"

    tracker = get_tracker(tracker_state = tracker_state_dictionary)

    action = actions.ActionHandleSetupTutorial()
    events = action.run(dispatcher, tracker, domain)
    expected_events = [
        SlotSet("current_tutorial", "setup_tutorial"),
        SlotSet("tutorial_next_step", 1),
        FollowupAction("controller_form")
    ]
    assert events == expected_events


# test setup tutorial handler
def test_run_handle_setup_tutorial(tracker, dispatcher, domain):
    action = actions.ActionHandleSetupTutorial()
    events = action.run(dispatcher, tracker, domain)
    expected_events = [
        SlotSet("current_tutorial", "setup_tutorial"),
        SlotSet("tutorial_next_step", 1),
        FollowupAction("controller_form")
    ]
    assert events == expected_events


def test_run_handle_setup_tutorial_avr_all_steps(tracker, dispatcher, domain):
    tracker_state_dictionary = json.load(open(Path(__file__).parent.resolve() / "./data/empty_tracker.json"))
    tracker_state_dictionary['slots']['controller_type'] = "avr"

    upper_bound = actions.ActionHandleSetupTutorial.total_number_of_steps_avr + 1
    for i in range(1, upper_bound):

        tracker_state_dictionary['slots']['tutorial_next_step'] = i
        tracker_state_dictionary['slots']['current_tutorial'] = "setup_tutorial"
        tracker = get_tracker(tracker_state = tracker_state_dictionary)

        action = actions.ActionHandleSetupTutorial()
        events = action.run(dispatcher, tracker, domain)
        expected_events = [
            SlotSet("current_tutorial", "setup_tutorial"),
            SlotSet("tutorial_next_step", i+1),
            FollowupAction("action_listen")
        ]

        assert events == expected_events
        expected_response = f"utter_setup_avr_step_{i}"
        assert dispatcher.messages[i-1]["response"] == expected_response

def test_run_handle_setup_tutorial_stm_all_steps(tracker, dispatcher, domain):
    tracker_state_dictionary = json.load(open(Path(__file__).parent.resolve() / "./data/empty_tracker.json"))
    tracker_state_dictionary['slots']['controller_type'] = "stm"

    upper_bound = actions.ActionHandleSetupTutorial.total_number_of_steps_avr + 1
    for i in range(1, upper_bound):

        tracker_state_dictionary['slots']['tutorial_next_step'] = i
        tracker_state_dictionary['slots']['current_tutorial'] = "setup_tutorial"
        tracker = get_tracker(tracker_state = tracker_state_dictionary)

        action = actions.ActionHandleSetupTutorial()
        events = action.run(dispatcher, tracker, domain)
        expected_events = [
            SlotSet("current_tutorial", "setup_tutorial"),
            SlotSet("tutorial_next_step", i+1),
            FollowupAction("action_listen")
        ]

        assert events == expected_events
        expected_response = f"utter_setup_stm_step_{i}"
        assert dispatcher.messages[i-1]["response"] == expected_response

def test_run_handle_setup_tutorial_xmc_all_steps(tracker, dispatcher, domain):
    tracker_state_dictionary = json.load(open(Path(__file__).parent.resolve() / "./data/empty_tracker.json"))
    tracker_state_dictionary['slots']['controller_type'] = "xmc"

    upper_bound = actions.ActionHandleSetupTutorial.total_number_of_steps_avr + 1
    for i in range(1, upper_bound):

        tracker_state_dictionary['slots']['tutorial_next_step'] = i
        tracker_state_dictionary['slots']['current_tutorial'] = "setup_tutorial"
        tracker = get_tracker(tracker_state = tracker_state_dictionary)

        action = actions.ActionHandleSetupTutorial()
        events = action.run(dispatcher, tracker, domain)
        expected_events = [
            SlotSet("current_tutorial", "setup_tutorial"),
            SlotSet("tutorial_next_step", i+1),
            FollowupAction("action_listen")
        ]

        assert events == expected_events
        expected_response = f"utter_setup_xmc_step_{i}"
        assert dispatcher.messages[i-1]["response"] == expected_response

def test_run_handle_setup_tutorial_finished(tracker, dispatcher, domain):
    total_number_of_steps_dict = {'avr': 5, 'xmc': 6, 'stm':7}
    tracker_state_dictionary = json.load(open(Path(__file__).parent.resolve() / "./data/empty_tracker.json"))
    tracker_state_dictionary['slots']['current_tutorial'] = "setup_tutorial"

    for controller_type in ('avr', 'xmc', 'stm'):
        tracker_state_dictionary['slots']['controller_type'] = controller_type
        tracker_state_dictionary['slots']['tutorial_next_step'] = total_number_of_steps_dict[controller_type] + 1
        tracker = get_tracker(tracker_state = tracker_state_dictionary)
        action = actions.ActionHandleSetupTutorial()
        events = action.run(dispatcher, tracker, domain)
        expected_events = [
            SlotSet("current_tutorial", None),
            SlotSet("tutorial_next_step", 0),
            FollowupAction('action_listen')
        ]
        assert events == expected_events
        expected_response_1 = "utter_congratulations"
        expected_response_2 = "utter_successor_setup_tutorial"
        assert dispatcher.messages[0]["response"] == expected_response_1
        assert dispatcher.messages[1]["response"] == expected_response_2

# test led tutorial handler
def test_run_handle_led_tutorial(tracker, dispatcher, domain):
    action = actions.ActionHandleLedTutorial()
    events = action.run(dispatcher, tracker, domain)
    expected_events = [
        SlotSet("current_tutorial", "led_tutorial"),
        SlotSet("tutorial_next_step", 1),
        FollowupAction("controller_form")
    ]
    assert events == expected_events


def test_run_handle_led_tutorial_all_steps(tracker, dispatcher, domain):
    tracker_state_dictionary = json.load(open(Path(__file__).parent.resolve() / "./data/empty_tracker.json"))

    upper_bound = actions.ActionHandleLedTutorial.total_number_of_steps + 1

    for i in range(1, upper_bound):

        tracker_state_dictionary['slots']['tutorial_next_step'] = i
        tracker_state_dictionary['slots']['current_tutorial'] = "led_tutorial"
        tracker = get_tracker(tracker_state = tracker_state_dictionary)

        action = actions.ActionHandleLedTutorial()
        events = action.run(dispatcher, tracker, domain)
        expected_events = [
            SlotSet("current_tutorial", "led_tutorial"),
            SlotSet("tutorial_next_step", i+1),
            FollowupAction("action_listen")
        ]

        assert events == expected_events
        expected_response = f"utter_led_step_{i}"
        assert dispatcher.messages[i-1]["response"] == expected_response

def test_run_handle_led_tutorial_finished(tracker, dispatcher, domain):
    tracker_state_dictionary = json.load(open(Path(__file__).parent.resolve() / "./data/empty_tracker.json"))
    tracker_state_dictionary['slots']['tutorial_next_step'] = actions.ActionHandleLedTutorial.total_number_of_steps + 1
    tracker_state_dictionary['slots']['current_tutorial'] = "led_tutorial"
    tracker = get_tracker(tracker_state = tracker_state_dictionary)

    action = actions.ActionHandleLedTutorial()
    events = action.run(dispatcher, tracker, domain)
    expected_events = [
        SlotSet("current_tutorial", None),
        SlotSet("tutorial_next_step", 0),
        FollowupAction('action_listen')
    ]
    assert events == expected_events

    expected_response_1 = "utter_congratulations"
    expected_response_2 = "utter_successor_led_tutorial"
    assert dispatcher.messages[0]["response"] == expected_response_1
    assert dispatcher.messages[1]["response"] == expected_response_2


# test button tutorila handler
def test_run_handle_button_tutorial(tracker, dispatcher, domain):
    action = actions.ActionHandleButtonTutorial()
    events = action.run(dispatcher, tracker, domain)
    expected_events = [
        SlotSet("current_tutorial", "button_tutorial"),
        SlotSet("tutorial_next_step", 1),
        FollowupAction("controller_form")
    ]
    assert events == expected_events

def test_run_handle_button_tutorial_all_steps(tracker, dispatcher, domain):
    tracker_state_dictionary = json.load(open(Path(__file__).parent.resolve() / "./data/empty_tracker.json"))

    upper_bound = actions.ActionHandleButtonTutorial.total_number_of_steps + 1

    for i in range(1, upper_bound):

        tracker_state_dictionary['slots']['tutorial_next_step'] = i
        tracker_state_dictionary['slots']['current_tutorial'] = "button_tutorial"
        tracker = get_tracker(tracker_state = tracker_state_dictionary)

        action = actions.ActionHandleButtonTutorial()
        events = action.run(dispatcher, tracker, domain)
        expected_events = [
            SlotSet("current_tutorial", "button_tutorial"),
            SlotSet("tutorial_next_step", i+1),
            FollowupAction("action_listen")
        ]

        assert events == expected_events
        expected_response = f"utter_button_step_{i}"
        assert dispatcher.messages[i-1]["response"] == expected_response

def test_run_handle_button_tutorial_finished(tracker, dispatcher, domain):
    tracker_state_dictionary = json.load(open(Path(__file__).parent.resolve() / "./data/empty_tracker.json"))
    tracker_state_dictionary['slots']['tutorial_next_step'] = actions.ActionHandleLedTutorial.total_number_of_steps + 1
    tracker_state_dictionary['slots']['current_tutorial'] = "button_tutorial"
    tracker = get_tracker(tracker_state = tracker_state_dictionary)

    action = actions.ActionHandleButtonTutorial()
    events = action.run(dispatcher, tracker, domain)
    expected_events = [
        SlotSet("current_tutorial", None),
        SlotSet("tutorial_next_step", 0),
        FollowupAction('action_listen')
    ]
    assert events == expected_events

    expected_response_1 = "utter_congratulations"
    expected_response_2 = "utter_successor_button_tutorial"
    assert dispatcher.messages[0]["response"] == expected_response_1
    assert dispatcher.messages[1]["response"] == expected_response_2

# test tutorial dispatcher
def test_run_action_dispatcher_no_active_tutorial(tracker, dispatcher, domain):

    action = actions.ActionDispatchTutorial()
    events = action.run(dispatcher, tracker, domain)
    expected_events = [
        FollowupAction("action_listen"),
    ]
    assert events == expected_events

    expected_response = "no_active_tutorial"
    assert dispatcher.messages[0]["response"] == expected_response

def test_run_action_dispatcher_active_led_tutorial(tracker, dispatcher, domain):

    tracker_state_dictionary = json.load(open(Path(__file__).parent.resolve() / "./data/empty_tracker.json"))
    tracker_state_dictionary['slots']['current_tutorial'] = "led_tutorial"
    tracker = get_tracker(tracker_state = tracker_state_dictionary)

    action = actions.ActionDispatchTutorial()
    events = action.run(dispatcher, tracker, domain)
    expected_events = [
        FollowupAction("handle_led_tutorial")
    ]
    assert events == expected_events

def test_run_action_dispatcher_active_button_tutorial(tracker, dispatcher, domain):

    tracker_state_dictionary = json.load(open(Path(__file__).parent.resolve() / "./data/empty_tracker.json"))
    tracker_state_dictionary['slots']['current_tutorial'] = "button_tutorial"
    tracker = get_tracker(tracker_state = tracker_state_dictionary)

    action = actions.ActionDispatchTutorial()
    events = action.run(dispatcher, tracker, domain)
    expected_events = [
        FollowupAction("handle_button_tutorial")
    ]
    assert events == expected_events

def test_run_action_dispatcher_active_setup_tutorial(tracker, dispatcher, domain):

    tracker_state_dictionary = json.load(open(Path(__file__).parent.resolve() / "./data/empty_tracker.json"))
    tracker_state_dictionary['slots']['current_tutorial'] = "setup_tutorial"
    tracker = get_tracker(tracker_state = tracker_state_dictionary)

    action = actions.ActionDispatchTutorial()
    events = action.run(dispatcher, tracker, domain)
    expected_events = [
        FollowupAction("handle_setup_tutorial")
    ]
    assert events == expected_events
