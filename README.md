# Flask-App---Task-Management

Task Management API

The Task Management API is a simple Flask-based web application that allows you to manage tasks with various properties like title, description, completion status and due date.

Before running the Task Management API, ensure you have the following installed on your system:

Python (3.6 or higher)
PostgreSQL database (PostgreSQL 9.4 or higher)

Installation
Clone the repository:
git clone https://github.com/christineelia/Flask-App---Task-Management.git

Create and activate a virtual environment (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'

Set the appropriate value for the SQLALCHEMY_DATABASE_URI variable to point to your PostgreSQL database. For example:

SQLALCHEMY_DATABASE_URI = 'postgresql://your-username:your-password@localhost/your-database'
Adjust other configurations (if necessary) such as DEBUG, SQLALCHEMY_TRACK_MODIFICATIONS, etc.
Initialize the database:

Run the following command to create the necessary tables in the database:

python manage.py db init
python manage.py db migrate
python manage.py db upgrade

Note: Ensure your PostgreSQL server is running and the database specified in the SQLALCHEMY_DATABASE_URI exists.

Running the Application

To run the Task Management API, use the following command:
python app.py

By default, the application will be accessible at http://127.0.0.1:5000/.

Endpoints
The Task Management API provides the following endpoints:

GET /tasks: Retrieve a list of all tasks.
GET /tasks/<int:task_id>: Retrieve a specific task by its ID.
POST /tasks: Create a new task.
PUT /tasks/<int:task_id>: Update an existing task by its ID.
DELETE /tasks/<int:task_id>: Delete a task by its ID.

Usage Examples
Creating a New Task
To create a new task, send a POST request to /tasks with the following JSON payload:

{
  "title": "Buy groceries",
  "description": "Buy milk, eggs, and bread.",
  "completed": false,
  "due_date": "2023-08-15"
}
Updating an Existing Task
To update an existing task, send a PUT request to /tasks/<task_id> with the JSON payload containing the fields you want to update:

{
  "title": "Buy groceries",
  "completed": true
}
Deleting a Task
To delete a task, send a DELETE request to /tasks/<task_id>.

