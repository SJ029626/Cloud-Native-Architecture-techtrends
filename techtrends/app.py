'''
maintainer: Sanyam Jain
Version: V1.0
'''
import sqlite3

from flask import Flask, jsonify, json, render_template, request, url_for, redirect, flash
from werkzeug.exceptions import abort
import logging # For enabling Logging
import sys

count_of_connection = 0
# Function to get a database connection.
# This function connects to database with the name `database.db`
app = Flask(__name__)

def get_db_connection():
    connection = sqlite3.connect('database.db')
    connection.row_factory = sqlite3.Row
    global count_of_connection
    count_of_connection += 1
    return connection

# Function to get a post using its ID
def get_post(post_id):
    connection = get_db_connection()
    post = connection.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    connection.close()
    return post

# Define the Flask application
app.config['SECRET_KEY'] = 'your secret key'

# Define the main route of the web application 
@app.route('/')
def index():
    connection = get_db_connection()
    posts = connection.execute('SELECT * FROM posts').fetchall()
    connection.close()
    return render_template('index.html', posts=posts)

# Define how each individual article is rendered 
# If the post ID is not found a 404 page is shown
@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    if post is None:
      app.logger.error('Article with id {0} does not exist!'.format(post_id))
      return render_template('404.html'), 404
    else:
      app.logger.info('Existing Article {title} retrieved!'.format(title=post['title']))
      return render_template('post.html', post=post)

# Define the About Us page
@app.route('/about')
def about():
    app.logger.info("About US Page is Retrieved")
    return render_template('about.html')

# Define the post creation functionality 
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            connection.commit()
            app.logger.info('The Following Article {0} has been created'.format(title))
            connection.close()

            return redirect(url_for('index'))

    return render_template('create.html')

# Step 1: Best Practices for application deployment
# Part 1: /healthz endpoint
@app.route('/healthz', methods=['GET'])
def healthz():
    try:
        # If the endpoint is accessible
        result = {'result': 'OK - healthy'}
        result.update({'status_code': 200})
        status_code = 200
        connect = get_db_connection()
        cursor = connect.cursor()
        cursor.execute('SELECT * FROM posts')
        connect.close()
    except Exception as e:
        result = {'result': 'ERROR - unhealthy',
                  'status_code': 500}
        result.update({'error': str(e)})
        # Internal Server Error
        status_code = 500
    response = app.response_class(
        response=json.dumps(result),
        status=status_code,
        mimetype='application/json')
    return response


# Part 2: /metrics
@app.route('/metrics', methods=['GET'])
def metrics():
    try:
        status_code = 200
        connect = get_db_connection()
        cursor = connect.cursor()
        # Understood from index function
        count = len(cursor.execute('SELECT * FROM posts').fetchall())
        result = {'db_connection_count': count_of_connection,
                  'post_count': count,
                  'status': 200}
        connect.close()
    except Exception as e:
        result = {'result': 'ERROR - unhealthy',
                  'status_code': 500}
        result.update({'error': str(e)})
        # Internal Server Error
        status_code = 500
    response = app.response_class(
        response=json.dumps(result),
        status=status_code,
        mimetype='application/json')
    return response


# start the application on port 3111
if __name__ == "__main__":
    formatter = logging.Formatter(
        '%(levelname)s:%(name)s:%(asctime)s, %(message)s',
        '%d/%m/%Y, %H:%M:%S')

    app.logger.setLevel(logging.DEBUG)

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setFormatter(formatter)
    app.logger.addHandler(stdout_handler)

    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    app.logger.addHandler(stderr_handler)

    app.run(host='0.0.0.0', port='3111')