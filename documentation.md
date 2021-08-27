

# forms

1. register form and all required slots in domain.yml
2. Add utter_ask_<slotname> texts to domain
3. Add rules for form activation and deactivation
4. Add stories to help with detecting deviations

if the value of a behaviour should influence the conversation -> influence_conversation = True

## form validation

1. creat custom action validate_<form_name> and inherit from FormValidationAction
2. for each slot you want to add validation, overwrite validate_<slot_name>
3. add validation logic

## custom actions

### dynamic form behaviour
!!! did not work yet !!! probably have to add a story
what i tried:
overwrite required_slots
add utter_ask_slot
add slot



problem: bot does not ask the added slot within the form!

### added reset action
this actions is added as a rule after form deactivation

### added provide_uml action
this action evaluates the defined slots and provides a fitting predefined UML diagram

!!! todo: provide methods to overwrite
!!! build link / filename


## slot types

There are a couple of slot types which have specific use cases
When use from_text and when from_slot?

# enquire

Allow the user to gain further information on how to answer the current question without interrupting the form.

This is done by:
1. Adding further information as response to domain.yml
2. Implement an enquire intent and add it to the domain
3. Add a new rule that whenever the user enquires at a current stage of the form, a specific response is given.


rasa run actions
rasa shell
rasa shell --debug
rasa interactive

action_endpoint:
  url: "http://localhost:5055/webhook


# current bugs
- does not ask for frequency after accuracy???


todos:

- what can you do? (fallback)
- [x] add more microcontrollers
- [x] validation for other slots
- [x] How to learn c++?
- [x] How to overwrite function?
- [x] two stage fallback policy https://rasa.com/docs/rasa/fallback-handoff/#two-stage-fallback
-  provide image
- [x] faq questions (sth with retrieval)
- [x] chitchat
- [x] local deployment https://rasa.com/docs/rasa-x/installation-and-setup/install/local-mode/
- entity typos https://stackoverflow.com/questions/63719843/how-to-handle-spelling-mistaketypos-in-entity-extraction-in-rasa-nlu



implemented features:

- form with slots (structured information retrieval)
- slot validation:
  - choose from predefined list of choices
  - optional use of buttons for predefined choices
  - provide list of methods to overwrite reading from csv
  - validation logic for pins reading from json
- fill slots from entities
- provide uml
- enquire intent informs user dependent on which slot is active
- refresh slots after form is finished



# validation logic for tutorial steps

action: give some info and ask if succsessful
if yes: continue
if no: ask what's wrong

problem: When bot asks "Whats wrong?" the user will answer and the bot will try to solve the problem. But on top of that the bot is still waiting for the slot to be filled and will repeat it's question. 
A solution could be that the bot has a unicue problem solves slot. But then it would have to use this slot after every possible step.

solution proposal:
a more elegant way is if we give the advice after validating the last slot. This way it is not repeated each time.
When will this fail? When we have dynamic slots maybe? NO, because the logic that starts the dynamic slot can still be used to handle the response logic.
--> this is better but still the question "Did you succed" will be repeated and will overlap with "plaese describe your problem"
maybe try to not call the dispatcher but define a response as next action?
--> research response as next actions
--> not successfull
---> asking in rasa Form
[ ] waiting for resposne
[ ] --> proposal: use stories and rules


alternative:
Just tell the user he can answer with yes or describe the problem!
--> shortens validation logic


What if we just return [] instead of slot:None? 
--> This does not work, the slot_value will just be set.
[x]

problem: User is asked if he needs help with the setup. Bot will either answer with a link or not. 
Now we want to know if setup was successfull?
---> add confirm_setup slot
[x] 

by the way: slot_value already takes the extracted intent! 

even better solution?
--> custom query where utter_ask_slot is only repeated if last intent was affirm

# deployment
quick guide on https://rasa.com/docs/rasa-x/installation-and-setup/install/quick-install-script

## make ssh connection

ssh friotte@project2.informatik.uni-osnabrueck.de

cd /local/friotte

## install 

#problem

switch between forms
what I tried:
stories -> correct action is memorized but not used (probably overruled by rule policy?)
rule -> what happens?
[ ] try with featurized slots

# share rasa locally

https://rasa.com/docs/rasa-x/installation-and-setup/install/local-mode/
rasa x
ngrok http 5002

http://localhost:5002/guest/conversations/production/58182c1c43fd49448e9aa6eaca9e89ac

http://2a4d2f64ed39.ngrok.io/guest/conversations/production/58182c1c43fd49448e9aa6eaca9e89ac

[ ] fix order becaus of freakign rasa x
[ ] confrim setup as dynamic slot




## new idea for step by step realisation

- custom action for form

- custom action for "next" dispatcher

- slots for counter and current tutorial





# todos


-{'start_led_form': True} vs. SlotSet() ???
- create stories data

# bug fixing

problem: tutorial dispatcher does not work as intended

- it starts the correct tutorial when requestes
- with "next intent" the correct tutorial is dispatched
- but with LED nothing happens and with button tut only 1 step increment is possible

why?

Trying to run unknown follow-up action 'handle_led_tutorial'  HOW?? It is registered.

Why is default message added?
because bot does not know next actions and has no stories to learn from.
--> action_listen as followUP

Suddenly next step counting also works and I do not know why...


# server deployment

https://rasa.com/docs/rasa-x/installation-and-setup/install/quick-install-script

quick install --> url to rasa x

curl -s get-rasa-x.rasa.com | sudo bash


connect to new server:

ssh  -i .ssh/id_rsa_ba root@chatbot.informatik.uni-osnabrueck.de

  While you're waiting please add the following line to your terminal configuration  (depending on your operating system this is the '~/.bashrc' or '~/.zshrc' file).  This is needed so that you can access the embedded cluster using the 'kubectl' command  line interface.

          export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

  Rasa X will be installed into the following Kubernetes namespace: rasa

  Please save the following access credentials for later use:

  Your Rasa X password is WXFOOZI1Ij6alYXxRsXd

  The passwords for the other services in the deployment are:

  Database password (PostgreSQL): aQHWUdSIUYqNxuPeGQxd
  Event Broker password (RabbitMQ): Ll74Y6uIBI3I5meAg8n0
  Lock Store password (Redis): IVzQu5ebwhjr2cvHmEpg