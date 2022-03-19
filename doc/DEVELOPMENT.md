# Development

You can continue the development by forking https://github.com/Effo483/ES-Tutorial-Chatbot.

There is a github workflow automatically creating a docker image of the action server after each change to the actions file.
After forking, the docker registry should be replaced with your own dockerhub repository.

After the action server image was updated, the new image tag needs to be specified on the server in:
```/etc/rasa/docker-compose.override.yml```
This step can probably be automated be using the appropriate tag (using :latest didn't work for some reason)

# Start Chat

To use custom actions defined in actiony.py you can start the action server with the following command: ```rasa run actions```

In a second terminal you can start the conversation with ```rasa shell```

# Train the model

Whenever the nlu.yml or rules.yml has been updated you can retrain your model by using ```rasa train```

# Test custom actions

Tests defined in **tests/test_actions.py** can be run with ```pipenv run pytest tests```


