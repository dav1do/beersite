from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models


@app.before_first_request
def setup():
    pass


@app.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()

# todo implement bootstrap formatting
# todo make combined reviews format nicely
# todo metacritc v pitchfork:
#   top 10 per year for each
#   which metacritic are biggest user vs critic difference
#   which albums do metacritic and pitchfork agree/disagree on
# todo deploy it
# http://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xvii-deployment-on-linux-even-on-the-raspberry-pi
