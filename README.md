How to setup the environment and run an app: <br />
$ mkdir folder <br />
$ cd folder <br />
$ virtualenv .venv <br />
$ source .venv/bin/activate <br />
$ pip3 install falcon   <br />
Open new terminal and do: <br />
$ source .venv/bin/activate <br />
$ pip3 install gunicorn <br />
copy a file t.py into the directory and run <br />
$ gunicorn t:app <br />
then open a new terminal tab and run a following command for posting a json: <br />
$curl -X POST -d @your_file.json http://localhost:8000/things <br />
then for GET in the same tab: <br />
$ http GET  http://localhost:8000/reputee/nr1
