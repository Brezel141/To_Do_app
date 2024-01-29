# Import necessary modules from Flask and Flask-SQLAlchemy
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# Initialize a Flask app
app = Flask(__name__)

# Configure the app to use a SQLite database named 'todos.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'

# Disable the Flask-SQLAlchemy event system
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy object with the Flask app
db = SQLAlchemy(app)

migrate = Migrate(app, db)

# Define a Todo model to structure the database table
class Todo(db.Model):
    __tablename__ = 'tasks'  # Define the table name 'tasks'
    id = db.Column(db.Integer, primary_key=True)  # An integer column to serve as the primary key
    content = db.Column(db.String(200), nullable=False)  # A string column for the to-do item content
    completed = db.Column(db.Boolean, default=False)  # A boolean column to indicate if a task is completed
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Todo %r>' % self.id  # Representation of the Todo object

# Define the index route to show all to-do items
@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.id.desc()).all()  # Retrieve all Todo items from the database
    
    return render_template('index.html', todos=todos) # Render the 'index.html' template with the todos

# Define the route to add a new to-do item
@app.route('/add', methods=['POST'])
def add_todo():
    todo = request.form.get('todo')  # Get the 'todo' data from the form
    new_todo = Todo(content=todo)  # Create a new Todo object
    db.session.add(new_todo)  # Add the new object to the database session
    db.session.commit()  # Commit the session to save the changes
    return redirect('/')  # Redirect to the index page

# Check if the script is run directly and not imported
if __name__ == '__main__':
    app.run(debug=True)  # Run the app in debug mode

# Define the route to mark a to-do item as completed
@app.route('/complete/<int:id>')
def complete_todo(id):
    todo = Todo.query.get_or_404(id)  # Get the Todo item by id or return a 404 error
    todo.completed = True  # Set the 'completed' attribute of the Todo to True
    db.session.commit()  # Commit the session to save the changes
    return redirect('/')  # Redirect to the index page

# Define the route to delete a to-do item
@app.route('/delete/<int:id>')
def delete_todo(id):
    todo = Todo.query.get_or_404(id)  # Get the Todo item by id or return a 404 error
    db.session.delete(todo)  # Delete the Todo item from the database
    db.session.commit()  # Commit the session to save the changes
    return redirect('/')  # Redirect to the index page

