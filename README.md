# old-people-API

#### A web implementation API using Flask.

## Local Setup:
 1. Ensure that Python, Flask, flask_cors, firebase_admin installed (either manually, or run `pip install -r requirements.txt`).
 2. Run *app.py* with `python app.py`.
 3. The demo will be live at [http://localhost:5000/](http://localhost:5000/)

## How do I deploy this to a web server?
If you do not have a dedicated server, I highly recommend using [PythonAnywhere](https://www.pythonanywhere.com/), [AWS](https://aws.amazon.com/getting-started/projects/deploy-python-application/) or [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#introduction) to host your application.

### Deploying on Heroku
If you are deploying on Heroku, you have `heroku` folder

... to use the Firebase adapter:

```
cred = credentials.Certificate('serviceAccountKey.json')

```
... where `serviceAccountKey.json` is the file config the database "Firebase" you wish to connect to ..

## License
This source is free to use.
