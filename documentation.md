

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

<!-- ## make ssh connection

ssh friotte@project2.informatik.uni-osnabrueck.de

cd /local/friotte -->

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

ssh -i .ssh/id_rsa_ba root@chatbot.informatik.uni-osnabrueck.de

pw: u...7..6..

  While you're waiting please add the following line to your terminal configuration  (depending on your operating system this is the '~/.bashrc' or '~/.zshrc' file).  This is needed so that you can access the embedded cluster using the 'kubectl' command  line interface.

          export KUBECONFIG=/etc/rancher/k3s/k3s.yaml

  Rasa X will be installed into the following Kubernetes namespace: rasa

  Please save the following access credentials for later use:

  Your Rasa X password is WXFOOZI1Ij6alYXxRsXd

  The passwords for the other services in the deployment are:

  Database password (PostgreSQL): aQHWUdSIUYqNxuPeGQxd
  Event Broker password (RabbitMQ): Ll74Y6uIBI3I5meAg8n0
  Lock Store password (Redis): IVzQu5ebwhjr2cvHmEpg

  Deploying Rasa X ...

problem: install script got stuck



--> new approach

# docker compose

https://rasa.com/docs/rasa-x/installation-and-setup/install/docker-compose/#docker-compose-install-script

sudo python3 rasa_x_commands.py create --update admin me PASSWORD


Server IP address: 131.173.23.119

!model upload does not work!
--> it does now (conflicting rasa x version)

?transfer model via scp?

scp -i .ssh/id_rsa_ba /home/f/Projects/bachelor_thesis/first_prototype/models/20210823-120923.tar.gz root@chatbot.informatik.uni-osnabrueck.de:/etc/rasa/models/


pipenv install -U rasa-x --extra-index-url https://pypi.rasa.com/simple

next steps:

- [x] create github repository
- [x] dockerhub account
- [x] add DockerHub login and pw to github repository secrets
- [x] create workflows/actions_server.yml
- [x] push docker image to dockerhub
- [x] create docker-compose.override.yml inside your /etc/rasa https://rasa.com/docs/rasa-x/installation-and-setup/customize#connecting-a-custom-action-server
- [x] start rasa x again

build action server image https://rasa.com/docs/rasa/how-to-deploy/#building-an-action-server-image

docker login --username frogg28 --password o36PezYGoPc0
docker push frogg28/rasa_action_server:tagname

git-deploy-key
PASSWORD

curl -k -F "model=@my_model.tar.gz" "http://131.173.23.119/projects/default/models?api_token=eca3c2205588b6dc6b0e900996a1325fb3e0b80d"

curl --request POST \
     --url http://131.173.23.119/api/projects/default/git_repositories?api_token=eca3c2205588b6dc6b0e900996a1325fb3e0b80d" \
     --header 'Content-Type: application/json' \
     --data-binary @repository.json

## github key

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

## update docker image

nano /etc/rasa/docker-compose.override.yml
--> replace image tag

sudo docker-compose down
sudo docker-compose up -d

## debug

switch between tutorials does not work

- do tutorials work independently correct?
- what exactly happens when you switch?
[x] done (problem was created by giving next intent during form, solved by cycling back to form if intent is "next")

## next features

### [x] restart
  - [x] add restart intent
  - [x] add restart rule
  - [x] add restart action

  -> there is a hidden rule that calls action_restart!
  -> rename intent to restart_tutorial instead
### [x] implement retrieval intent

  - add retrieval rule
  - ?

### [x] Inform about usage with hello intent


### add another tutorial

### check for best practices

- fallback?
- no scope?


### [x] consolidate forms
One form should be enough to cover all tutorials. Otherwise the ovearhead of adding additional tutorials is too big. 
  - [x] always call the same form from each tutorial handler
  - [x] test new form
  - [x] get rid of rules and instead use submit method or sth
  - [x] move first message from utter_ask_start.. to utter_introduction


### [x] create unit tests

### basic chitchat?

### slot values reset after form is finished

### write tests
  - [x] figure out how to test custom actions
  - [x] test restart
  - [x] test increment
  - [x] test switch

### abstract class or interface for handler actions?

### update server
  
  - push to git
  - update docker id?

### test if rasa x bug happens on server too

### add imgur picturs

which link?

--> https://i.imgur.com/8f5Xi3Q.jpg


### problems

- pipenv lock does not work (numpy)
- apparently pipfile has not been created before?
- in local repo there was a different tensorflow version (2.6 instead of 2.3.4)
  --> doing downgrade now
  

!forms need to be consolidated! One form should be enough to handle all tutorials.
This will get rid of the tutorial specific start_tutorial slot. This can probably be replaced by an fstring that uses the current tutorial slot. 


connect to server:

ssh -i .ssh/id_rsa_ba root@chatbot.informatik.uni-osnabrueck.de
u..7....6
Server IP address: 131.173.23.119
P......D

### push to git

username: Effo483
pw: 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

### restart rasa

ssh -i .ssh/id_rsa_ba root@chatbot.informatik.uni-osnabrueck.de
cd /etc/rasa
sudo docker-compose down
sudo docker-compose up -d
go to 131.173.23.119


which ip?