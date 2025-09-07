"""Module providing a function printing python version."""

# Standard library imports
import os
import re
import sqlite3
from datetime import datetime, timedelta

# Third-party imports
from flask import Flask, render_template, request, url_for, flash, redirect, session
from werkzeug.exceptions import abort  # pyright: ignore[reportMissingImports]
from flask_wtf import CSRFProtect  # <-- Added CSRFProtect for STRIDE

# First-party / local imports
from flask_session import Session  # pyright: ignore[reportMissingImports]


# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'nosecret')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
csrf = CSRFProtect(app)  # <-- Added CSRFProtect (STRIDE)
Session(app)

# Added security headers to mitigate vulnerabilities (STRIDE)
@app.after_request
def set_security_headers(response):
    """ Adds common security-related HTTP headers """

    # Prevent clickjacking
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'

    # Prevent XSS attacks in some browsers
    response.headers['X-XSS-Protection'] = '1; mode=block'

    # Content Security Policy (CSP) to control resources loaded
    csp_policy = [
        "default-src 'self'; "
        "script-src 'self' https://code.jquery.com https://cdnjs.cloudflare.com,"
        " https://stackpath.bootstrapcdn.com https://cdn.jsdelivr.net; "
        "style-src 'self' 'unsafe-inline' https://stackpath.bootstrapcdn.com,"
        " https://cdn.jsdelivr.net; "
        "font-src 'self' https://cdn.jsdelivr.net; "  # For Bootstrap Icons font files
        "img-src 'self' data:; "  # 'data:' allows inline images
    ]
    response.headers['Content-Security-Policy'] = csp_policy

    return response

def get_db_connection():
    """Create and return a new SQLite database connection with row factory set to sqlite3.Row."""
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


# Template filter to strip HTML tags from strings
@app.template_filter('strip_html')
def strip_html(text):
    """Remove HTML tags from a string for safe display."""
    if not text:
        return ''
    text = str(text)  # Ensure input is a string
    return re.sub(r'<[^>]*?>', '', text)


@app.route('/')
def index():
    """Display all posts on the homepage."""
    conn = get_db_connection()
    posts = conn.execute(
        'SELECT id, title, content, created, author FROM posts'
    ).fetchall()
    conn.close()

    return render_template('index.html', posts=posts)


def get_post(post_id):
    """Retrieve a single post by ID. Abort with 404 if not found."""
    conn = get_db_connection()
    post_data = conn.execute(
        'SELECT * FROM posts WHERE id = ?',
        (post_id,)
    ).fetchone()
    conn.close()

    if post_data is None:
        abort(404)

    return post_data


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    """Edit a post if the user is logged in."""
    if 'username' not in session:
        return redirect(url_for('login'))

    post_data = get_post(post_id)  # Raises 404 if post not found

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title:
            flash('Title is needed!')
        else:
            edit_post(post_id, title, content)
            flash('Post updated successfully')
            return redirect(url_for('post', post_id=post_id))

    return render_template('edit.html', post=post_data)


def delete_post(post_id):
    """Delete a post by its ID."""
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()


@app.route('/<int:post_id>')
def post(post_id):
    """Display a single post and its comments."""
    post_data = get_post(post_id)  # Make sure this raises 404 if post not found

    conn = get_db_connection()
    comments = conn.execute(
        'SELECT * FROM comments WHERE post_id = ?',
        (post_id,)
    ).fetchall()
    conn.close()

    return render_template('post.html', post=post_data, comments=comments)


@app.route('/create', methods=['GET', 'POST'])
def create():
    """Create a new post if the user is logged in."""
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()

        if not title:
            flash('Title is needed!')
        else:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO posts (title, content, author) VALUES (?, ?, ?)',
                (title, content, session['name'])
            )
            conn.commit()
            conn.close()
            flash('Post created successfully')
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id, title=None, content=None):
    """Update the title and content of a post."""
    title = title or request.form.get('title', '').strip()
    content = content or request.form.get('content', '').strip()

    conn = get_db_connection()
    conn.execute(
        'UPDATE posts SET title = ?, content = ? WHERE id = ?',
        (title, content, post_id)
    )
    conn.commit()
    conn.close()
    return redirect(url_for('post', post_id=post_id))


@app.route('/<int:post_id>/delete', methods=['POST'])
def delete(post_id):
    """Delete a post if the user is logged in."""
    if 'username' not in session:
        return redirect(url_for('login'))

    post_to_delete = get_post(post_id)  # Make sure get_post raises 404 if post not found
    delete_post(post_id)
    flash(f'"{post_to_delete["title"]}" was successfully deleted!')
    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login by verifying username and password."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username:
            flash('Username is needed!')
        elif not password:
            flash('Password is needed!')
        else:
            conn = get_db_connection()
            user = conn.execute(
                'SELECT * FROM users WHERE username = ?',
                (username,)
            ).fetchone()
            conn.close()

            if user is None:
                flash('Username does not exist!')
            elif user['password'] != password:  # Ideally use hashed password check
                flash('Password is incorrect!')
            else:
                session['username'] = user['username']
                session['name'] = user['name']
                session['email'] = user['email']
                session['member_since'] = user['member_since']
                return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Log the user out by clearing the session and redirect to homepage."""
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Allow admin to register new users."""
    # Only admin can access registration
    if request.method == 'GET':
        if session.get('username') != 'admin':
            flash('Only admin can register new users')
            return redirect(url_for('contactus'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')

        if not username:
            flash('Username is needed!')
        elif not name:
            flash('Name is needed!')
        elif not email:
            flash('Email is needed!')
        elif not password:
            flash('Password is needed!')
        elif password != confirm:
            flash('Passwords do not match!')
        else:
            conn = get_db_connection()
            conn.execute(
                'INSERT INTO users (username, name, email, password) VALUES (?, ?, ?, ?)',
                (username, name, email, password)
            )
            conn.commit()
            conn.close()
            flash('Registration successful')
            return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/profile')
def profile():
    """Display the logged-in user's profile and their posts."""
    if 'username' not in session:
        return redirect(url_for('login'))

    author = session['username']  # use consistent session key
    conn = get_db_connection()
    posts = conn.execute(
        'SELECT * FROM posts WHERE author = ?',
        (author,)
    ).fetchall()
    conn.close()

    return render_template('profile.html', posts=posts)


@app.route('/contactus', methods=['GET', 'POST'])
def contactus():
    """Handle the Contact Us form submission and display the form."""
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        issue = request.form['issue']
        subject = request.form['subject']
        message = request.form['message']
        #Process or store the contact message


        if not name:
            flash('Name is needed!')
        elif not email:
            flash('Email is needed!')
        elif not issue:
            flash('Issue is needed!')
        elif not subject:
            flash('Subject is needed!')
        elif not message:
            flash('Message is needed!')
        else:
            flash('Message sent!')
            return redirect(url_for('contactus'))

    return render_template('contactus.html')

@app.route('/add_comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    """Add a comment to a specific post. User must be logged in."""
    if 'username' not in session:
        return redirect(url_for('login'))

    comment = request.form.get('comment', '').strip()
    if not comment:
        flash('Comment cannot be empty')
        return redirect(url_for('post', post_id=post_id))

    author = session['username']  # ensure consistent session key
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO comments (post_id, author, content) VALUES (?, ?, ?)',
        (post_id, author, comment)
    )
    conn.commit()
    conn.close()

    flash('Comment added successfully')
    return redirect(url_for('post', post_id=post_id))


@app.route('/subscribe', methods=['POST'])
def subscribe():
    """Handle newsletter subscription by email."""
    email = request.form.get('email', '').strip()

    if email:
        #Save the email to the database or mailing list here
        flash('Subscription successful')
    else:
        flash('Please enter a valid email')

    return redirect(url_for('index'))


@app.route('/search', methods=['GET'])
def search():
    """Search posts by title or content based on query string 'q'."""
    query = request.args.get('q', '').strip()  # default to empty string if not provided

    if not query:
        posts = []
    else:
        conn = get_db_connection()
        posts = conn.execute(
            'SELECT * FROM posts WHERE title LIKE ? OR content LIKE ?',
            ('%' + query + '%', '%' + query + '%')
        ).fetchall()
        conn.close()

    return render_template('search.html', posts=posts, query=query)

@app.template_filter('iso_to_pretty')
def iso_to_pretty(value, fmt='%B %-d, %Y'):
    """Convert an ISO 8601 datetime string to a human-readable format."""
    return datetime.fromisoformat(value.replace('Z', '+00:00')).strftime(fmt)

if __name__ == '__main__':
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    port = int(os.getenv("APP_PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "yes")

    app.run(host=host, port=port, debug=debug)
