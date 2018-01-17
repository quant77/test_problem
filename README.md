How to setup the environment and run an app:
$ mkdir folder
$ cd folder
$ virtualenv .venv
$ source .venv/bin/activate
$ pip3 install falcon
Open new terminal and do:
$ source .venv/bin/activate
$ pip3 install gunicorn
copy a file t.py into the directory and run
$ gunicorn t:app
then open a new terminal tab and run a following command for posting a json:
$curl -X POST -d @your_file.json http://localhost:8000/things
$
