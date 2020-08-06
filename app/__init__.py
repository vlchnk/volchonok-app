from flask import Flask, render_template, url_for, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import uuid
from config import Config


# app.logger.info(username) - log

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


# if __name__ == '__main__':
#     app.run() #host='0.0.0.0'

from app import route, models, api