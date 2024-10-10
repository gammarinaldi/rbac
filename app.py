import functools
from flask import Flask, jsonify, request
from models import db, User, Role
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)

def create_tables():
    print("Current working directory:", os.getcwd())
    print("Attempting to create tables...")
    try:
        with app.app_context():
            db.create_all()
        print("Tables created successfully.")
    except Exception as e:
        print("Error creating tables:", str(e))

def create_roles():
    with app.app_context():
        roles = ['Admin', 'Editor', 'Viewer']
        for role_name in roles:
            existing_role = Role.query.filter_by(name=role_name).first()
            if not existing_role:
                new_role = Role(name=role_name)
                db.session.add(new_role)
        db.session.commit()

# Assign a role to a user (Admin functionality)
@app.route('/assign_role', methods=['POST'])
def assign_role():
    data = request.json
    username = data.get('username')
    role_name = data.get('role_name')
    
    user = User.query.filter_by(username=username).first()
    role = Role.query.filter_by(name=role_name).first()
    
    if user and role:
        user.role_id = role.id
        db.session.commit()
        return jsonify({'message': 'Role assigned successfully'}), 200
    return jsonify({'error': 'User or role not found'}), 404

# Decorator to restrict access based on roles
def role_required(required_role):
    def decorator(f):
        @functools.wraps(f)  # This line preserves the function's name and prevents overwriting
        def wrapper(*args, **kwargs):
            username = request.headers.get('username')  # Simulating user login
            user = User.query.filter_by(username=username).first()
            
            if user and user.role.name == required_role:
                return f(*args, **kwargs)
            else:
                return jsonify({'error': 'Forbidden: Insufficient role'}), 403
        return wrapper
    return decorator

# Admin-only endpoint to manage users
@app.route('/manage_users', methods=['GET'])
@role_required('Admin')
def manage_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'role': u.role.name} for u in users])

# Editor-only endpoint to manage content
@app.route('/manage_content', methods=['POST'])
@role_required('Editor')
def manage_content():
    # Content creation logic
    return jsonify({'message': 'Content created/updated/deleted'}), 200

# Viewer-only endpoint to view content
@app.route('/view_content', methods=['GET'])
@role_required('Viewer')
def view_content():
    # Logic to display content
    return jsonify({'content': 'Here is some viewable content'}), 200

# Add this function to your app.py
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    username = data.get('username')
    role_name = data.get('role_name')
    
    if not username or not role_name:
        return jsonify({'error': 'Both username and role_name are required'}), 400

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400
    
    role = Role.query.filter_by(name=role_name).first()
    if not role:
        return jsonify({'error': 'Specified role does not exist'}), 400
    
    new_user = User(username=username, role=role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User added successfully'}), 201

# Add this function to check roles
@app.route('/check_roles', methods=['GET'])
def check_roles():
    roles = Role.query.all()
    return jsonify([{'id': role.id, 'name': role.name} for role in roles])

if __name__ == '__main__':
    create_tables()
    create_roles()
    app.run(debug=True)
