# Import necessary modules from Flask and Flask-SQLAlchemy
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# Initialize a Flask app
app = Flask(__name__)

# Configure the app to use a SQLite database named 'todos.db'
# SQLite is a database engine that allows you to create relational databases as simple disk files
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

# Disable the Flask-SQLAlchemy event system
# This is a system that signals the application every time a change is about to be made in the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object with the Flask app
# SQLAlchemy is a SQL toolkit and Object-Relational Mapping (ORM) system for Python, which provides a full suite of well known enterprise-level persistence patterns
db = SQLAlchemy(app)

# Initialize Flask-Migrate for handling database migrations
# Migrations are a way to make changes to your database schema (adding, removing, or modifying tables and fields) over time, while preserving existing data
migrate = Migrate(app, db)

# Define a Todo model to structure the database table
class Todo(db.Model):
    __tablename__ = 'tasks'  # Define the table name 'tasks'
    id = db.Column(db.Integer, primary_key=True)  # An integer column to serve as the primary key
    content = db.Column(db.String(200), nullable=False)  # A string column for the to-do item content
    completed = db.Column(db.Boolean, default=False)  # A boolean column to indicate if a task is completed
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # A datetime column for when the task was created

    def __repr__(self):
        return '<Todo %r>' % self.id  # Representation of the Todo object, useful for debugging

# Define a CompletedTask model to structure the database table
class CompletedTask(db.Model):
    __tablename__ = 'completed_tasks'  # Define the table name 'completed_tasks'
    id = db.Column(db.Integer, primary_key=True)  # An integer column to serve as the primary key
    content = db.Column(db.String(200), nullable=False)  # A string column for the task content
    date_completed = db.Column(db.DateTime, default=datetime.utcnow)  # A datetime column for when the task was completed

    def __repr__(self):
        return '<CompletedTask %r>' % self.id  # Representation of the CompletedTask object

# Define a DeletedTask model to structure the database table
class DeletedTask(db.Model):
    __tablename__ = 'deleted_tasks'  # Define the table name 'deleted_tasks'
    id = db.Column(db.Integer, primary_key=True)  # An integer column to serve as the primary key
    content = db.Column(db.String(200), nullable=False)  # A string column for the task content
    date_deleted = db.Column(db.DateTime, default=datetime.utcnow)  # A datetime column for when the task was deleted

    def __repr__(self):
        return '<DeletedTask %r>' % self.id  # Representation of the DeletedTask object

# Define the index route to show all to-do items
@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.id.desc()).all()  # Retrieve all Todo items from the database
    completed = CompletedTask.query.order_by(CompletedTask.date_completed.desc()).all()  # Retrieve all CompletedTask items from the database
    deleted = DeletedTask.query.order_by(DeletedTask.date_deleted.desc()).all()  # Retrieve all DeletedTask items from the database
    return render_template('index.html', todos=todos, completed=completed, deleted=deleted)  # Render the index template with the todos, completed, and deleted variables

# Define the route to add a new to-do item
@app.route('/add', methods=['POST'])
def add_todo():
    todo = request.form.get('todo')  # Get the 'todo' data from the form
    new_todo = Todo(content=todo)  # Create a new Todo object
    db.session.add(new_todo)  # Add the new object to the database session
    db.session.commit()  # Commit the session to save the changes
    return redirect('/')  # Redirect to the index page

# Define the route to mark a to-do item as completed
@app.route('/complete/<int:id>')
def complete_todo(id):
    todo = Todo.query.get_or_404(id)  # Get the Todo item or return a 404 error
    completed_task = CompletedTask(content=todo.content)  # Create a new CompletedTask object
    db.session.add(completed_task)  # Add the CompletedTask object to the database session
    db.session.delete(todo)  # Delete the Todo item from the database session
    db.session.commit()  # Commit the session to save the changes
    return redirect('/')  # Redirect to the index page

# Define the route to delete a to-do item
@app.route('/delete/<int:id>')
def delete_todo(id):
    todo = Todo.query.get_or_404(id)  # Get the Todo item or return a 404 error
    deleted_task = DeletedTask(content=todo.content)  # Create a new DeletedTask object
    db.session.add(deleted_task)  # Add the DeletedTask object to the database session
    db.session.delete(todo)  # Delete the Todo item from the database session
    db.session.commit()  # Commit the session to save the changes
    return redirect('/')  # Redirect to the index page

# Check if the script is run directly and not imported
if __name__ == '__main__':
    app.debug = True  # Enable debug mode
    app.run()  # Run the Flask application