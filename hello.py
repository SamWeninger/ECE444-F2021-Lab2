from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from wtforms.fields.html5 import EmailField

from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    email = EmailField('What is your UofT Email address?', validators=[DataRequired(), Email()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route("/user/<name>")
def user(name):
    return render_template('user.html', name=name)

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    #session['name'] = "Stranger"
    #session['email'] = None
    #email = None
    #name = None
    if form.validate_on_submit():
        old_email = session.get('email')
        #email = form.email.data
        #form.email.data = ''
        #name = form.name.data
        #form.name.data = ''
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('You changed your name!')
        if old_email is not None and old_email != form.email.data:
            flash('You changed your email!')
        session['name'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), email=session.get('email'))

if __name__ == "__main__":
    app.run()
