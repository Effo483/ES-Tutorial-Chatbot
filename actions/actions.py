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

        if tracker.get_slot("current_tutorial") != 'led_tutorial':
            print("tutorial switch detected")
            current_step = 0
            next_step = current_step + 1

        if current_step == 0:
            return [SlotSet("current_tutorial", "led_tutorial"), SlotSet("led_tutorial_next_step", next_step), FollowupAction("led_tutorial_form") ]

        if current_step <= total_number_of_steps:
            try:
                dispatcher.utter_message(response = next_response)
            except:
                dispatcher.utter_message("No response found for this tutorial step.")
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
        current_intent = tracker.latest_message['intent'].get('name')
        if current_tutorial == None:
            dispatcher.utter_message(response = "no_active_tutorial")
        elif current_intent == "next" and tracker.active_loop.get('name'):
            return [FollowupAction(tracker.active_loop.get('name'))]
            # if form is running, a "next" intent should not skip the form 
        elif current_tutorial == "led_tutorial":
            return [FollowupAction("handĺe_led_tutorial")]
        elif current_tutorial == "button_tutorial":
            return [FollowupAction("handle_button_tutorial")]
        else:
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


        if tracker.get_slot("current_tutorial") != 'button_tutorial':
            print("tutorial switch detected")
            current_step = 0
            next_step = current_step + 1

        if current_step == 0:
            return [SlotSet("current_tutorial", "button_tutorial"), SlotSet("button_tutorial_next_step", next_step), FollowupAction("button_tutorial_form")]

        if current_step <= total_number_of_steps:
            try:
                dispatcher.utter_message(response = next_response)
            except:
                dispatcher.utter_message("No response found for this tutorial step.")
            return [SlotSet("current_tutorial", "button_tutorial"), SlotSet("button_tutorial_next_step", next_step), FollowupAction("action_listen")]

        else:
            dispatcher.utter_message(response = "utter_congratulations")
            return [SlotSet("current_tutorial", None), SlotSet("button_tutorial_next_step", 0), FollowupAction("action_listen")]

        return []


class ActionAnswerScope(Action):

    def name(self):
        return "answer_scope"

    def run(self, dispatcher, tracker, domain):

        #constnruct list of tutorials
        tutorials = [key for key in domain['forms'] if key.endswith('tutorial_form')]

        for i, tutorial in enumerate(tutorials):
            new_tutorial = tutorial[:-14]
            new_tutorial = '- ' + new_tutorial.capitalize() + ' tutorial'
            tutorials[i] = new_tutorial

        # construct list of faqs
        faqs = [key for key in domain['responses'] if key.startswith('utter_faq')]
        for i, faq in enumerate(faqs):
            new_faq = faq[10:]
            new_faq = new_faq.replace("_", " ")
            new_faq = '- ' + new_faq.capitalize() + "?"
            faqs[i] = new_faq

        message = "Here are the things I can do. I can assist you with tutorials and I can answer a list of FAQs.\n" + "List of tutorials:\n" + "\n".join(tutorials) + 2*"\n" + "List of FAQs:\n" + "\n".join(faqs)
        dispatcher.utter_message(message)

        return []


class ActionRestartTutorial(Action):

    def name(self):
        return "restart_tutorial"

    def run(self, dispatcher, tracker, domain):

        current_tutorial = tracker.get_slot("current_tutorial")
        step_counter_name = current_tutorial + "_next_step"

        return [SlotSet(step_counter_name, 0)]
