# llama.cpp playground Backend🦙

A backend for handle paralell server.cpp instances executions for playground UI. Is experimental and only for personal use purposes given the nature of the project. It is not explicit necessary because the fronted works too with standalone server execution.

More information about server.cpp: https://github.com/ggerganov/llama.cpp/tree/master/examples/server

### How to run
```
Put your model into 'model' folder and the llama server executable into the same path at main.py.
Configure the config.yml for set the model or configure the server parameters.
```
#### Install dependences
```
pip install -r requirements.txt
```

#### Launch server
```
flask --app main.py run --host=0.0.0.0 --port=5000 --with-threads
```

#### Lauch in debug mode
```
flask --app main.py run --host=0.0.0.0 --port=5000 --with-threads --debug
```