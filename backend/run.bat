@echo off
flask --app main.py run --host=0.0.0.0 --port=8080 --with-threads  --debug
pause