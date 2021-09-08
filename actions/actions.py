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

    async def required_slots(
            self,
            slots_mapped_in_domain: List[Text],
            dispatcher: "CollectingDispatcher",
            tracker: "Tracker",
            domain: "DomainDict",
        ) -> Optional[List[Text]]:

            # fix rasa x slot order bug
            slots_mapped_in_domain_ordered = ['start_led_form', 'setup', 'controller_type', ]

            return slots_mapped_in_domain_ordered

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

class TutorialHandlerClass(Action):

    def __init__(self):
        self.tutorial_name = self.name()[7:]
        self.slot_counter_name = self.tutorial_name + "_next_step"
    
    def name(self) -> Text:
        return "handle_name_tutorial"

    def run(self, dispatcher, tracker, domain):
        current_step = self.current_step(tracker)   
        next_response = self.next_response(current_step)
        next_step = current_step + 1

        # if tutorial has been switched, reset counter
        if self.current_tutorial(tracker) != self.tutorial_name:
            current_step = 0
            next_step = current_step + 1
        # if counter is 0, start form
        if current_step == 0:
            return [SlotSet("current_tutorial", self.tutorial_name), SlotSet(self.slot_counter_name, next_step), FollowupAction(self.form_name()) ]
        # if counter > 0, choose message according to step counter
        elif current_step <= self.total_number_of_steps:
            try:
                dispatcher.utter_message(response = next_response)
            except ValueError as err:
                dispatcher.utter_message("Sorry, no response found for this tutorial step.")
                print(err.args)
            return [SlotSet("current_tutorial", self.tutorial_name), SlotSet(self.slot_counter_name, next_step), FollowupAction("action_listen")]
        # if counter is 1 bigger than max steps, tutorial is finished.
        elif current_step == self.total_number_of_steps + 1:
            dispatcher.utter_message(response = "utter_congratulations")
            return [SlotSet("current_tutorial", None), SlotSet(self.slot_counter_name, 0), FollowupAction("action_listen")]
        # something went wrong
        else:
            raise ValueError('The step counter raised higher than it should.')

    def current_step(self, tracker):
        return tracker.get_slot(self.slot_counter_name) 

    def next_step(self):
        return self.current_step() + 1

    def next_response(self, current_step):
        # the name of the next response based on the tutorial step
        tutorial_prefix = self.tutorial_name[:-9]
        return  f'utter_{tutorial_prefix}_step_{current_step}'

    def current_tutorial(self, tracker):
        return tracker.get_slot("current_tutorial")

    def form_name(self):
        return self.tutorial_name + "_form"

class ActionHandleLedTutorial(TutorialHandlerClass):

    total_number_of_steps = 6

    def __init__(self):
        self.tutorial_name = self.name()[7:]
        self.slot_counter_name = self.tutorial_name + "_next_step"

    def name(self):
        return "handĺe_led_tutorial"

class ActionHandelButtonTurial(TutorialHandlerClass):

    total_number_of_steps = 6

    def __init__(self):
        self.tutorial_name = self.name()[7:]
        self.slot_counter_name = self.tutorial_name + "_next_step"

    def name(self):
        return "handle_button_tutorial"

class ActionDispatchTutorial(Action):

    def name(self):
        return "dispatch_tutorials"

    def run(self, dispatcher, tracker, domain):

        current_tutorial = tracker.get_slot("current_tutorial")
        current_intent = tracker.latest_message['intent'].get('name')
        if current_tutorial == None:
            dispatcher.utter_message(response = "no_active_tutorial")
            return [FollowupAction("action_listen")]
        elif current_intent == "next" and tracker.active_loop.get('name'):
            return [FollowupAction(tracker.active_loop.get('name'))]
            # if form is running, a "next" intent should not skip the form 
        elif current_tutorial == "led_tutorial":
            return [FollowupAction("handĺe_led_tutorial")]
        elif current_tutorial == "button_tutorial":
            return [FollowupAction("handle_button_tutorial")]
        else:
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
