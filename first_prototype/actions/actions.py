# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import AllSlotsReset, FollowupAction, ActiveLoop, SlotSet
from rasa_sdk.forms import FormAction


class ActionResetAllSlots(Action):

    def name(self):
        return "reset_all_slots"

    def run(self, dispatcher, tracker, domain):
        return [AllSlotsReset()]

class ValidateLedForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_led_form"

    def validate_start_led_form(
                self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        intent_name = tracker.latest_message['intent'].get('name')
        if intent_name == 'affirm':
            return {'start_led_form': True}
        if intent_name == 'deny':
            dispatcher.utter_message(response = "utter_cancel")
            # this deactivates the form
            return { "requested_slot": None}


        return {"start_led_form": None}


    def validate_controller_type(
                self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        if slot_value == 'xmc':
            dispatcher.utter_message(response= "utter_youtube_blinky_xmc")
            return {"controller_type": slot_value}
        if slot_value == 'stm':
            dispatcher.utter_message(response= "utter_youtube_blinky_stm")
            return {"controller_type": slot_value}
        if slot_value == 'avr':
            dispatcher.utter_message(response= "utter_youtube_blinky_avr")
            return {"controller_type": slot_value}

        return {"controller_type": None}


    # def validate_confirm_setup(
    #             self,
    #     slot_value: Any,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,
    # ) -> Dict[Text, Any]:
    #     """Validate cuisine value."""
    #     intent_name = tracker.latest_message['intent'].get('name')

    #     if slot_value == False:
    #         return {"confirm_setup": None}
    #     if slot_value == True:
    #         return {"confirm_setup": True}

    #     return {"confirm_setup": None}


    def validate_setup(
                self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        intent_name = tracker.latest_message['intent'].get('name')
        controller = tracker.get_slot('controller_type')
        if intent_name == 'affirm':
            if controller == "xmc":
                dispatcher.utter_message(response = "utter_youtube_setup_xmc")
                dispatcher.utter_message(response = "utter_setup_stm_xmc")
                return {"setup": True}
            if controller == 'avr':
                dispatcher.utter_message(response = "utter_youtube_setup_avr")
                dispatcher.utter_message(response = "utter_setup_avr")
                return {"setup": True}
            if controller == 'stm':
                dispatcher.utter_message(response = "utter_youtube_setup_stm")
                dispatcher.utter_message(response = "utter_setup_stm")                    
                return {"setup": True}

        if intent_name == 'deny':
            return {"setup": False}

        return {"setup": None}


    # def submit(self, dispatcher, tracker, domain):

    #     dispatcher.utter_message(response="utter_add_led")
    #     return []


    # async def required_slots(
    #         self,
    #         slots_mapped_in_domain: List[Text],
    #         dispatcher: "CollectingDispatcher",
    #         tracker: "Tracker",
    #         domain: "DomainDict",
    #     ) -> Optional[List[Text]]:

    #         # fix rasa x slot order bug
    #         slots_mapped_in_domain_ordered = ['start_led_form', 'controller_type', 'setup']

    #         return slots_mapped_in_domain_ordered

class ValidateFunctionKeyForm(FormValidationAction):

    def name(self) -> Text:
        return "validate_button_form"


    def validate_start_button_form(
                self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        intent_name = tracker.latest_message['intent'].get('name')
        if intent_name == 'affirm':
            return {'start_button_form': True}
        if intent_name == 'deny':
            dispatcher.utter_message(response = "utter_cancel")
            # this deactivates the form
            return { "requested_slot": None}

        return {"start_button_form": None}
        
    def validate_controller_type(
                self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""

        #todo add button youtube links
        if slot_value == 'xmc':
            dispatcher.utter_message(response= "utter_youtube_blinky_xmc")
            return {"controller_type": slot_value}
        if slot_value == 'stm':
            dispatcher.utter_message(response= "utter_youtube_blinky_stm")
            return {"controller_type": slot_value}
        if slot_value == 'avr':
            dispatcher.utter_message(response= "utter_youtube_blinky_avr")
            return {"controller_type": slot_value}

        return {"controller_type": None}

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
        ) -> Optional[List[Text]]:

            # fix rasa x slot order bug
            slots_mapped_in_domain_ordered = ['start_button_form', 'controller_type',]

            return slots_mapped_in_domain_ordered

class ActionHandleBlinkyTutorial(Action):

    def name(self):
        return "handĺe_led_tutorial"

    def run(self, dispatcher, tracker, domain):
        
        total_number_of_steps = 6

        current_step = tracker.get_slot("led_tutorial_next_step")    
        next_response = f'utter_led_step_{current_step}'
        next_step = current_step+1

        print(current_step)
        if current_step == 0:
            return [SlotSet("current_tutorial", "led_tutorial"), SlotSet("led_tutorial_next_step", next_step), FollowupAction("led_form") ]

        print(current_step, next_response)
        if current_step <= total_number_of_steps:
            try:
                dispatcher.utter_message(response = next_response)
            except:
                #todo: implement useful error handling
                print("no response found")
            return [SlotSet("current_tutorial", "led_tutorial"), SlotSet("led_tutorial_next_step", next_step), FollowupAction("action_listen")]

        else:
            dispatcher.utter_message(response = "utter_congratulations")
            return [SlotSet("current_tutorial", None), SlotSet("led_tutorial_next_step", 0), FollowupAction("action_listen")]

        return []

class ActionDispatchTutorial(Action):

    def name(self):
        return "dispatch_tutorials"

    def run(self, dispatcher, tracker, domain):

        current_tutorial = tracker.get_slot("current_tutorial")
        print("current_tutorial is:")
        print(current_tutorial)
        if current_tutorial == None:
            dispatcher.utter_message(response = "no_active_tutorial")
        elif current_tutorial == "led_tutorial":
            print("dispatch to LED tutorial")
            return [FollowupAction("handĺe_led_tutorial")]
        elif current_tutorial == "button_tutorial":
            print("dispatch to button tutorial")
            return [FollowupAction("handle_button_tutorial")]
        else:
            print("current_tutorial could not be found")
            return []

        return []

class ActionHandelButtonTurial(Action):

    def name(self):
        return "handle_button_tutorial"

    def run(self, dispatcher, tracker, domain):

        total_number_of_steps = 6

        current_step = tracker.get_slot("button_tutorial_next_step")
        next_response = f'utter_button_step_{current_step}'
        next_step = current_step + 1

        if current_step == 0:
            return [SlotSet("current_tutorial", "button_tutorial"), SlotSet("button_tutorial_next_step", next_step), FollowupAction("button_form")]

        if current_step <= total_number_of_steps:
            try:
                dispatcher.utter_message(response = next_response)
            except:
                #todo add error handling
                print("no response found")
            return [SlotSet("current_tutorial", "button_tutorial"), SlotSet("button_tutorial_next_step", next_step), FollowupAction("action_listen")]

        else:
            dispatcher.utter_message(response = "utter_congratulations")
            return [SlotSet("current_tutorial", None), SlotSet("button_tutorial_next_step", 0), FollowupAction("action_listen")]

        return []

class Test(Action):

    def name(self):
        return "test"


    def run(self, dispatcher, tracker, domain):

        dispatcher.utter_message("utter_greet")

        return [FollowupAction("action_listen")]