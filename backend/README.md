# llama.cpp playground Backend🦙

A backend for handle paralell server.cpp instances executions for playground UI. Is experimental and only for personal use purposes given the nature of the project.


### How to run
#### Put your model and setup into main.py from backend
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