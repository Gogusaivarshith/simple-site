from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Define a Contact model
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    message = db.Column(db.Text)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    message = request.form['message']

    # Save to database
    contact = Contact(name=name, message=message)
    db.session.add(contact)
    db.session.commit()

    return render_template('success.html', name=name)

@app.route('/messages')
def view_messages():
    all_contacts = Contact.query.all()
    return render_template('messages.html', contacts=all_contacts)


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
