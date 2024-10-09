from flask import Flask, jsonify, request
from models import db, User, Role

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db.init_app(app)

# Create roles in the system
def create_roles():
    admin_role = Role(name='Admin')
    editor_role = Role(name='Editor')
    viewer_role = Role(name='Viewer')
    
    db.session.add_all([admin_role, editor_role, viewer_role])
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

if __name__ == '__main__':
    app.run(debug=True)
