from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://your_username:your_password@localhost/your_database'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String(10))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    disposition = db.Column(db.String(50))
    image_url = db.Column(db.String(255))

@app.route('/admin')
def admin_portal():
    # Retrieve and display all users from the database
    users = User.query.all()
    return render_template('admin_portal.html', users=users)

@app.route('/admin/create_user', methods=['POST'])
def create_user():
    # Handle form submission to create a new user
    prefix = request.form['prefix']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    disposition = request.form['disposition']
    image_url = request.form['image_url']

    new_user = User(prefix=prefix, first_name=first_name, last_name=last_name, disposition=disposition, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('admin_portal'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
