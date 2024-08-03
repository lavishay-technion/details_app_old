import os
import logging
from flask import Flask, render_template, request, redirect, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from wtforms import StringField, SubmitField, validators
from flask_wtf import FlaskForm

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Fetch environment variables
dbuser = os.getenv("POSTGRES_USER")
dbpass = os.getenv("POSTGRES_PASSWORD")
dbhost = os.getenv('DBHOST')
dbname = os.getenv('DBNAME')
skey = os.getenv('SECRET_KEY')

app = Flask(__name__)
app.config['SECRET_KEY'] = skey
app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger.debug(f'Database URI: {app.config["SQLALCHEMY_DATABASE_URI"]}')

db = SQLAlchemy(app)

class Contacts(db.Model):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Contact {self.email}>'

class ConnectionForm(FlaskForm):
    name = StringField('Name', validators=[validators.DataRequired()])
    email = StringField('Email', validators=[validators.DataRequired()])
    submit = SubmitField('Submit')

# Create the table (this will not overwrite the existing table)
with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    form = ConnectionForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        new_contact = Contacts(name=name, email=email)
        try:
            db.session.add(new_contact)
            db.session.commit()
            logger.debug(f'Successfully added contact: {new_contact}')
            return redirect('/')
        except Exception as e:
            db.session.rollback()
            logger.error(f'Error adding contact: {e}', exc_info=True)
            flash('Failed to add contact. Please try again.', 'error')
    return render_template('index.html', form=form)

@app.route('/contacts', methods=['GET'])
def get_contacts():
    try:
        contacts = Contacts.query.with_entities(Contacts.id, Contacts.name, Contacts.email).all()
        logger.debug(f'Raw query result: {contacts}')
        result = [{'id': c.id, 'name': c.name, 'email': c.email} for c in contacts]
        logger.debug(f'Contacts fetched: {result}')
        return jsonify(result), 200
    except Exception as e:
        logger.error(f'Error fetching contacts: {e}', exc_info=True)
        return jsonify({"error": "Failed to fetch contacts"}), 500

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8000)


