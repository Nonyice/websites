from flask import Flask, render_template, request, redirect, url_for, jsonify

import psycopg2
import keyring


app = Flask(__name__, static_url_path='/static')


# Configure database connection details

db_host = "127.0.0.1"
db_name = "meal-treat"
db_user = "postgres"
db_password = keyring.get_password('meal-treat', 'postgres')

#Define the route for the homepage
@app.route('/')
def home():
    return render_template('index.html')
    

# Define the route for the contact form
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Connect to the database
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cur = conn.cursor()

        # Insert form data into the database
        cur.execute("INSERT INTO contact_form (name, email, message) VALUES (%s, %s, %s)",
                    (name, email, message))
        #Commit the database insertions
        conn.commit()

        # Close the database connection
        cur.close()
        conn.close()

        return 'Form submitted successfully!'
    
    return render_template('contact.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/submit_review', methods=['GET', 'POST'])
def leave_a_review():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        review = request.form['review']
        image_data = request.files['image_data']

        #Read image files as binary
        image_bytes = image_data.read()

        # Connect to the database
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cur = conn.cursor()
  
        # Insert form data into the database
        cur.execute("INSERT INTO customer_review (name, review, image_data) VALUES (%s, %s, %s)",
                    (name, review, psycopg2.Binary(image_bytes)))
        #Commit the database insertions
        conn.commit()

        # Close the database connection
        cur.close()
        conn.close()

        return 'Review submitted successfully!'
    
    return render_template('submit_review.html')

@app.route('/add_reviews')
def new_review():

    try:
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cur = conn.cursor()

        cursor.execute('SELECT name, review, image_data FROM customer_review')
        customer_review = [{'name': name, 'review': review, 'image': image_data} for name, review, image_data in cursor.fetchall()]
        
        cursor.close()
        conn.close()

    except Exception as e:
        return str(e)


    


if __name__ == '__main__':
    app.run(debug=True)
