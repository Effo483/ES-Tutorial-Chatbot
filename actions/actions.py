from abc import ABC, abstractmethod
from typing import Any, Text, Dict

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import FollowupAction, SlotSet


class ValidateControllerForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_controller_form"

    def validate_start_tutorial(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        intent_name = tracker.latest_message["intent"].get("name")
        if intent_name == "affirm":
            return {"start_tutorial": True}
        if intent_name == "deny":
            dispatcher.utter_message(response="utter_cancel")
            # this deactivates the form
            return {"requested_slot": None}

        return {"start_tutorial": None}

    def validate_controller_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:

        if slot_value == "xmc":
            return {"controller_type": slot_value}
        if slot_value == "stm":
            return {"controller_type": slot_value}
        if slot_value == "avr":
            return {"controller_type": slot_value}

        return {"controller_type": None}


class SubmitForm(Action):
    def name(self) -> Text:
        return "submit_form"

    def run(self, dispatcher, tracker, domain) -> Dict[Text, Any]:
        return [FollowupAction("dispatch_tutorials")]


class TutorialHandlerClass(ABC, Action):

    total_number_of_steps = -1
    total_number_of_steps_avr = -1
    total_number_of_steps_stm = -1
    total_number_of_steps_xmc = -1
    predecessor = None

    controller_type_is_relevant = False

    def __init__(self):
        self.tutorial_name = self.name()[7:]
        self.slot_counter_name = "tutorial_next_step"
        self.form_name = "controller_form"
        self.current_step = None
        self.next_response = None
        self.next_step = None
        self.tracker = None

    @abstractmethod
    def name(self) -> Text:
        return "handle_name_tutorial"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> Dict[Text, Any]:

        self.tracker = tracker
        self.current_step = self.get_current_step()
        self.next_step = self.current_step + 1

        # update max tutorial steps depending on context
        if self.controller_type_is_relevant:
            self.set_total_number_of_steps_depending_on_slots()

        # reset step counter if tutorial switch happened
        if self.get_current_tutorial() != self.tutorial_name:
            self.current_step = 0
            self.next_step = self.current_step + 1

        # if counter is 0, start form
        if self.current_step == 0:
            if self.predecessor:
                dispatcher.utter_message(
                    f'This is the {self.tutorial_name.capitalize().replace("_", " ")}. This assumes you have already done the {self.predecessor}. You can switch to that by typing "{self.predecessor}"'
                )
            return [
                SlotSet("current_tutorial", self.tutorial_name),
                SlotSet(self.slot_counter_name, self.next_step),
                FollowupAction(self.form_name),
            ]

        # if counter > 0, choose message according to step counter
        elif self.current_step <= self.total_number_of_steps:
            try:
                dispatcher.utter_message(response=self.get_next_response())
            except ValueError as err:
                dispatcher.utter_message(
                    "Sorry, no response found for this tutorial step."
                )
                print(err.args)
            return [
                SlotSet("current_tutorial", self.tutorial_name),
                SlotSet(self.slot_counter_name, self.next_step),
                FollowupAction("action_listen"),
            ]

        # if counter is 1 bigger than max steps, tutorial is finished.
        elif self.current_step == self.total_number_of_steps + 1:
            dispatcher.utter_message(response="utter_congratulations")
            if self.get_successor_name():
                dispatcher.utter_message(response=self.get_successor_name())
            else:
                dispatcher.utter_message("It seems like you completed everything. There is no successor for this tutorial.")
            return [
                SlotSet("current_tutorial", None),
                SlotSet(self.slot_counter_name, 0),
                FollowupAction("action_listen"),
            ]

        else:
            raise ValueError("The step counter raised higher than it should.")

    def get_current_step(self):
        return self.tracker.get_slot(self.slot_counter_name)

    def get_next_response(self) -> str:
        tutorial_prefix = self.tutorial_name[:-9]
        # the name of the next response based on the tutorial step
        if self.controller_type_is_relevant:
            controller_type = self.get_controller_type()
            return f"utter_{tutorial_prefix}_{controller_type}_step_{self.current_step}"
        else:
            return f"utter_{tutorial_prefix}_step_{self.current_step}"

    def get_current_tutorial(self):
        return self.tracker.get_slot("current_tutorial")

    def get_successor_name(self):
        return f"utter_successor_{self.tutorial_name}"

    def get_controller_type(self):
        return self.tracker.get_slot("controller_type")

    def set_total_number_of_steps_depending_on_slots(self):
        controller_type = self.get_controller_type()
        if controller_type == "avr":
            self.total_number_of_steps = self.total_number_of_steps_avr
        elif controller_type == "stm":
            self.total_number_of_steps = self.total_number_of_steps_stm
        elif controller_type == "xmc":
            self.total_number_of_steps = self.total_number_of_steps_xmc


class ActionHandleSetupTutorial(TutorialHandlerClass):

    controller_type_is_relevant = True
    total_number_of_steps_avr = 5
    total_number_of_steps_stm = 7
    total_number_of_steps_xmc = 6

    def name(self) -> Text:
        return "handle_setup_tutorial"


class ActionHandleLedTutorial(TutorialHandlerClass):

    total_number_of_steps = 6
    predecessor = "Setup Tutorial"

    def name(self):
        return "handle_led_tutorial"


class ActionHandleButtonTutorial(TutorialHandlerClass):

    total_number_of_steps = 6
    predecessor = "LED Tutorial"

    def name(self):
        return "handle_button_tutorial"


class ActionDispatchTutorial(Action):
    def name(self):
        return "dispatch_tutorials"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> Dict[Text, Any]:

        current_tutorial = tracker.get_slot("current_tutorial")
        current_intent = tracker.latest_message["intent"].get("name")

        # construct list of tutorials by searching the intents
        # warning: this is only a provisional solution because every intent whose name ends with "tutorial" will be treated as such
        tutorials = [
            list(dictionary)[0][8:]
            for dictionary in domain["intents"]
            if list(dictionary)[0].endswith("tutorial")
        ]

        if current_tutorial is None:
            # if no tutorial is active, 'next' intent has no function
            dispatcher.utter_message(response="no_active_tutorial")
            return [FollowupAction("action_listen")]
        if current_intent == "next" and tracker.active_loop.get("name"):
            # if form is running, a "next" intent would otherwise skip the form
            return [FollowupAction(tracker.active_loop.get("name"))]
        if current_tutorial in tutorials:
            # dispatch to the handler of the running tutorial
            handler_name = f"handle_{current_tutorial}"
            return [FollowupAction(handler_name)]
        # should not happen
        raise ValueError("Dispatcher was not able to dissolve the current state")


class ActionAnswerScope(Action):
    def name(self):
        return "answer_scope"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict
    ) -> Dict[Text, Any]:

        # construct list of tutorials by filtering intents
        tutorials = [
            list(dictionary)[0]
            for dictionary in domain["intents"]
            if list(dictionary)[0].endswith("tutorial")
        ]

        for i, tutorial in enumerate(tutorials):
            new_tutorial = tutorial[8:-9]
            new_tutorial = "- " + new_tutorial.capitalize() + " tutorial"
            tutorials[i] = new_tutorial

        # construct list of faqs
        faqs = [key for key in domain["responses"] if key.startswith("utter_faq")]
        for i, faq in enumerate(faqs):
            new_faq = faq[10:]
            new_faq = new_faq.replace("_", " ")
            new_faq = "- " + new_faq.capitalize() + "?"
            faqs[i] = new_faq

        message = (
            "Here are the things I can do. I can assist you with tutorials and I can answer a list of FAQs.\n"
            + "List of tutorials:\n"
            + "\n".join(tutorials)
            + 2 * "\n"
            + "List of FAQs:\n"
            + "\n".join(faqs)
        )
        dispatcher.utter_message(message)

        return []
