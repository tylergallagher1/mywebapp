from flask import Flask, session, request, render_template, render_template_string, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

class UserForm(FlaskForm):
    name = StringField(label=('Name:'), validators=[DataRequired(), Length(min=3)])
    email = StringField(label=('Email:'), validators=[DataRequired(), Length(min=8), Email()])
    submit = SubmitField(label=('Submit'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        session['username'] = form.name.data
        session['email'] = form.email.data
        return redirect(url_for('home'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('home'))

items = []

@app.route('/list')
def list():
    return render_template('items.html', items=items)

@app.route('/submit', methods=['POST'])
def submit():
    item = request.form['item']
    if item.strip():
        items.append(item)
        return render_template('items.html', items=items, message="Item Added")
    else:
        return render_template('items.html', items=items, message="Please enter a valid item")

if __name__ == '__main__':
    app.run(debug=True)