# Start Chat

To use custom actions defined in actiony.py you can start the action server with the following command: ```rasa run actions```

In a second terminal you can start the conversation with ```rasa shell```


# Train the model

Whenever the nlu.yml or rules.yml has been updated you can retrain your model by using ```rasa train```

# Tests custom actions

Tests defined in **tests/test_actions.py** can be run with ```pipenv run pytest tests```
