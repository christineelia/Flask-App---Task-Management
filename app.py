from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from datetime import datetime
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["DEBUG"] = True

db      = SQLAlchemy(app)
migrate = Migrate(app, db)

class Task(db.Model):
    id          = Column(Integer, primary_key=True)
    title       = Column(String)
    description = Column(String)
    completed   = Column(Boolean)
    due_date = Column(DateTime)

@app.route('/')
def home():
    return "Welcome to the Task Management API!"
    
# Returns list of all tasks    
@app.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        # Get the query parameters from the URL
        page = int(request.args.get('page', 1))  # Default to page 1 if not provided
        per_page = int(request.args.get('per_page', 10))  # Default to 10 items per page if not provided

        # Calculate the starting index and ending index for the pagination
        start_index = (page - 1) * per_page
        end_index = start_index + per_page

        # Query the database for tasks within the pagination range
        tasks = Task.query.slice(start_index, end_index).all()

        # Get the total number of tasks in the database
        total_tasks = Task.query.count()

        task_list = []
        for task in tasks:
            task_data = {
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'completed': task.completed,
            }
            if task.due_date is not None:
                task_data['due_date'] = task.due_date.strftime('%Y-%m-%d')
            else:
                task_data['due_date'] = None
            task_list.append(task_data)

        # Create the response dictionary
        response = {
            'tasks': task_list,
            'total_items': total_tasks,
            'page': page,
            'per_page': per_page
        }

        return jsonify(response), 200
    except SQLAlchemyError as e:
        error_msg = str(e)
        return jsonify({'error': error_msg}), 500

# Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    try:
        data = request.get_json()
        task = Task(
            title=data['title'],
            description=data['description'],
            completed=data['completed']
        )
        db.session.add(task)
        db.session.commit()

        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed,
            'due_date': task.due_date,
        }

        return jsonify(task_data), 201
    except KeyError:
        return jsonify({'error': 'Invalid request data'}), 400
    except SQLAlchemyError as e:
        error_msg = str(e)
        return jsonify({'error': error_msg}), 500

# Get Task by ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = Task.query.get(task_id)
        if task is None:
            return jsonify({'error': 'Task not found'}), 404

        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed,
        }

        if task.due_date is not None:
                task_data['due_date'] = task.due_date.strftime('%Y-%m-%d')
        else:
                task_data['due_date'] = None

        return jsonify(task_data), 200
    except SQLAlchemyError as e:
        error_msg = str(e)
        return jsonify({'error': error_msg}), 500

# Update existing task by ID
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        task = Task.query.get(task_id)
        if task is None:
            return jsonify({'error': 'Task not found'}), 404
        data = request.get_json()
        task.title = data['title']
        task.description = data['description']
        task.completed = data['completed']
        # due_date is optional
        # Format is DD/MM/YYYY , raise error if wrong
        try:
                # Attempt to parse the provided date string to a datetime object
                task.due_date = datetime.strptime(data['due_date'], '%d/%m/%Y')
        except ValueError:
                return jsonify({'error': 'Invalid date format. Date should be in DD/MM/YYYY format.'}), 400
        db.session.commit()

        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'completed': task.completed,
            'due_date' : task.due_date.strftime('%Y-%m-%d')
        }

        return jsonify(task_data), 200
    except KeyError:
        return jsonify({'error': 'Invalid request data'}), 400
    except SQLAlchemyError as e:
        error_msg = str(e)
        return jsonify({'error': error_msg}), 500

# Delete Task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        if task is None:
            return jsonify({'error': 'Task not found'}), 404
        db.session.delete(task)
        db.session.commit()

        return jsonify({'success': 'Task Deleted Successfully'}), 200
    except SQLAlchemyError as e:
        error_msg = str(e)
        return jsonify({'error': error_msg}), 500


if __name__ == '__main__':
    app.run()
