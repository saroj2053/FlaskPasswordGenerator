from flask import Flask, render_template, url_for, session, redirect
import os
from forms import ContactForm
import random
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

###########################################



class Customer(db.Model):

    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    queries = db.Column(db.Text)

    def __init__(self, username, email, queries):
        self.username = username
        self.email = email
        self.queries = queries

    def __repr__(self):
        return f"Customer is {self.username} and query is {self.queries}"

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

class InfoForm(FlaskForm):
    nr_letters = StringField("How many letters would you like in your password?",
                            validators=[DataRequired()])
    nr_symbols = StringField("How many symbols would you like in your password?",
                            validators=[DataRequired()])
    nr_numbers = StringField("How many numbers would you like in your password?",
                            validators=[DataRequired()])
    submit = SubmitField('Generate Password')

@app.route("/", methods=['GET','POST'])
def index():
    form = InfoForm()
    if form.validate_on_submit():
        session['nr_letters'] = form.nr_letters.data
        session['nr_symbols'] = form.nr_symbols.data
        session['nr_numbers'] = form.nr_numbers.data

        return redirect(url_for('password'))
    return render_template('main.html', form = form)

@app.route('/password')
def password():
    num_letter = int(session['nr_letters'])
    num_symbol = int(session['nr_symbols'])
    num_number = int(session['nr_numbers'])

    password_list = []
    pyPassword = ""
    for char in range(1, num_letter + 1):
        password_list.append(random.choice(letters))

    for symbol in range(1, num_symbol + 1):
        password_list.append(random.choice(symbols))

    for number in range(1, num_number + 1):
        password_list.append(random.choice(numbers))

    print(password_list)

    random.shuffle(password_list)
    print(password_list)

    for characters in password_list:
        pyPassword += characters

    return render_template('password.html',pyPassword = pyPassword)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():

        username = form.name.data
        email = form.email.data
        queries = form.queries.data

        new_user = Customer(username, email, queries)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('thankyou'))

    return render_template('contact.html', form = form)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')
    
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == "__main__":
    app.run(debug=True)
