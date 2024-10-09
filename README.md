# RBAC App: Role-Based Access Control System

This is a simple implementation of Role-Based Access Control (RBAC) using Flask. It allows administrators to assign roles (Admin, Editor, Viewer) to users, and restricts access to certain endpoints based on the user's role.

## Features

- **Admin**: Full access to manage users and assign roles.
- **Editor**: Can create, update, and delete content but cannot manage users.
- **Viewer**: Can view content but cannot modify or delete anything.
- **Role-Based Middleware**: Ensures only users with the correct role can access certain routes.

## Project Structure
```bash
rbac_app/
│
├── app.py          # Main Flask application
├── models.py       # Database models (Users, Roles, UserRoles)
├── db.sqlite3      # SQLite database
└── requirements.txt  # Dependencies
```


## Requirements

To run this project, you'll need to have Python and the following packages installed:

- Flask
- SQLAlchemy

Install dependencies by running:

```bash
pip install -r requirements.txt
```

## Getting Started
1. Clone the Repository
```bash
git clone https://github.com/your-repo/rbac-app.git
cd rbac-app
```
2. Set Up the Database
To set up the SQLite database and create roles, run the following Python script:
```bash
python -c 'from app import app; from models import create_tables, create_roles; create_tables(app); create_roles();'
```
This will create an SQLite database (db.sqlite3) and add the roles Admin, Editor, and Viewer to the database.

3. Run the Application
Start the Flask development server:

```bash
python app.py
```
The application will be available at http://127.0.0.1:5000.

Usage
1. Assign Role to a User
Admins can assign roles to users by making a POST request to /assign_role:

```bash
curl -X POST http://127.0.0.1:5000/assign_role -H "Content-Type: application/json" -d '{"username": "john", "role_name": "Editor"}'
```

2. Access Admin-Only Functionality
Admins can manage users by making a GET request to /manage_users:

```bash
curl -H "username: admin" http://127.0.0.1:5000/manage_users
```

3. Access Editor-Only Functionality
Editors can manage content by making a POST request to /manage_content:

```bash
curl -X POST -H "username: john" http://127.0.0.1:5000/manage_content
```

4. Access Viewer-Only Functionality
Viewers can view content by making a GET request to /view_content:

```bash
curl -H "username: jane" http://127.0.0.1:5000/view_content
```

5. Example Users
You can simulate users by passing the username header in your requests.

- Admin: Full access to manage users and assign roles.
- Editor: Can create, update, and delete content.
- Viewer: Can only view content.

## Project Details
- Database: SQLite is used for managing users and their roles.
- Role-Based Access: Implemented using Flask decorators to protect routes based on user roles.
- Token-Based Authentication: You can extend this project to include token-based authentication (JWT).

## Extending the Project
Add Authentication: Integrate JWT for secure authentication.
- UI Implementation: Add a frontend to manage users and content via a user-friendly interface.
- Role Customization: Implement more granular role definitions and permissions.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.


### Steps to Follow After Adding the `README.md`:

1. **Dependencies**: 
   - Ensure the `requirements.txt` contains the necessary libraries:
     ```bash
     Flask
     Flask-SQLAlchemy
     ```

2. **Database Initialization**: Follow the `Set Up the Database` section of the `README.md` to create the roles and the database before running the app.
