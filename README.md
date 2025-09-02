TheCyberForum

Version: 1.1.0

A simple blog application built with Flask that allows users to create, read, update, and delete blog posts.
Changelog
1.1.0 (2024-07-14)

    Blog main page updated to a more traditional look with a hero image at the top.
    Root / now redirects to /thecyberforum.
    Images now referenced using Flask's url_for('static', ...) for robust static file serving.
    Added comment functionality to post view page.
    Added search function with a search icon in the navbar.
    Edit and delete now work for posts; only the post creator can edit or delete their posts.
    Edit and delete available from both the post view and profile page.
    Create post supports image display.
    Post view page displays pasted images.
    Contact Us page is now connected and functional.
    Improved code documentation and clarity with comments in app.py.

1.0.0 (Initial Release)

    View all blog posts on the homepage
    Create, edit, and delete blog posts
    Responsive design using Bootstrap
    User authentication (login, logout, register)
    Profile page
    Contact us form

Features

    View all blog posts on the homepage
    Create new blog posts
    Edit existing blog posts (only by the post creator)
    Delete blog posts (only by the post creator)
    Add comments to posts
    Search posts by title or content
    Responsive design using Bootstrap
    User authentication (login, logout, register)
    Profile page with user's posts and quick actions
    Contact us form
    All routes under /thecyberforum for clear branding
    Robust static file/image handling

Prerequisites

    Python 3.8 or higher
    pip (Python package installer)

Installation

Clone the repository:

git clone https://github.com/AugustusNnamdi/flask_blog.git
cd flask-blog

Create and activate a virtual environment:

python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate

Install the required packages:

pip install -r requirements.txt

Initialize the database:

python init_db.py

Running the Application

Set the Flask environment variables:

# On Windows
set FLASK_APP=app.py
set FLASK_ENV=development
# On macOS/Linux
export FLASK_APP=app.py
export FLASK_ENV=development

Start the development server:

flask run

    Open your browser and navigate to http://127.0.0.1:5000/thecyberforum/


For other platforms, use the same commands:

    Build: pip install -r requirements.txt
    Start: gunicorn wsgi:app

Project Structure

flask_blog/
├── app.py                  # Main application file
├── requirements.txt        # Python dependencies
├── init_db.py              # Database initialization script
├── schema.sql              # SQL schema for the database
├── database.db             # SQLite database file
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   ├── img/
└── templates/              # HTML templates
    ├── base.html           # Base template with common elements
    ├── index.html          # Homepage template
    ├── create.html         # Create post template
    ├── edit.html           # Edit post template
    ├── post.html           # Single post template
    ├── profile.html        # User profile template
    ├── contactus.html      # Contact form template
    └── search.html         # Search results template

Development

    Set FLASK_ENV=development to enable debug mode
    The server will automatically reload when you make changes to the code

Resources

    Flask Documentation
    SQLite Documentation
    Bootstrap Documentation

License
This project is licensed under the MIT License - see the LICENSE file for details.