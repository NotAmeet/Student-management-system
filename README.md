# Flask Student Management System

A simple yet comprehensive web application for managing student records using Flask and SQLite. This system allows you to create, read, update, and delete student information with a clean and intuitive user interface.

## Features

- ✅ **Dashboard** - View statistics and recent students
- ✅ **Student Management** - Add, edit, view, and delete students
- ✅ **Search Functionality** - Search students by name, email, or enrollment number
- ✅ **Responsive Design** - Works on desktop, tablet, and mobile devices
- ✅ **Form Validation** - Client and server-side validation
- ✅ **Error Handling** - Custom error pages and error messages
- ✅ **RESTful API** - JSON API endpoints for integration
- ✅ **Database** - SQLite with SQLAlchemy ORM
- ✅ **Modern UI** - Bootstrap 5 with custom styling

## Technologies Used

- **Backend**: Flask 2.3.3
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **JavaScript**: Vanilla JavaScript for interactivity
- **Python**: 3.8+

## Project Structure

```
Student-management-system/
├── app.py                      # Main Flask application
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navbar
│   ├── index.html             # Home page/dashboard
│   ├── students/
│   │   ├── list.html          # List all students
│   │   ├── form.html          # Add/Edit student form
│   │   └── view.html          # View student details
│   └── errors/
│       ├── 404.html           # 404 error page
│       └── 500.html           # 500 error page
└── static/                     # Static files
    ├── css/
    │   └── style.css          # Custom CSS styles
    └── js/
        └── script.js          # Custom JavaScript
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/NotAmeet/Student-management-system.git
   cd Student-management-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your web browser and navigate to `http://localhost:5000`

## Usage

### Dashboard
- View total number of students
- See recent students added to the system
- Quick navigation to all sections

### Adding a Student
1. Click on "Students" in the navigation bar
2. Click "Add New Student" button
3. Fill in the student details:
   - First Name (required)
   - Last Name (required)
   - Email (required, must be unique)
   - Enrollment Number (required, must be unique)
   - Phone (required)
   - Date of Birth (optional)
   - Address (optional)
   - GPA (optional)
4. Click "Save" to add the student

### Viewing Students
1. Navigate to the "Students" page
2. View the list of all students with pagination
3. Use the search bar to find students by name, email, or enrollment number
4. Click on a student's name to view detailed information

### Editing a Student
1. Go to the student's detail page
2. Click the "Edit" button
3. Modify the student information
4. Click "Update" to save changes

### Deleting a Student
1. Go to the student's detail page
2. Click the "Delete" button
3. Confirm the deletion

## Database Schema

### Student Table

| Column | Type | Constraints |
|--------|------|-------------|
| id | Integer | Primary Key |
| first_name | String(100) | Not Null |
| last_name | String(100) | Not Null |
| email | String(120) | Unique, Not Null, Indexed |
| enrollment_number | String(50) | Unique, Not Null, Indexed |
| phone | String(20) | Not Null |
| date_of_birth | Date | Nullable |
| address | Text | Nullable |
| gpa | Float | Default: 0.0 |
| created_at | DateTime | Default: Current Time |
| updated_at | DateTime | Default: Current Time |

## API Endpoints

### GET Endpoints

- `GET /` - Dashboard page
- `GET /students` - List all students (with pagination)
- `GET /students/add` - Add student form
- `GET /students/<id>` - View student details
- `GET /students/<id>/edit` - Edit student form
- `GET /api/students` - Get all students as JSON
- `GET /api/students/<id>` - Get specific student as JSON

### POST Endpoints

- `POST /students/add` - Create new student
- `POST /students/<id>/edit` - Update student
- `POST /students/<id>/delete` - Delete student

## Features in Detail

### Search Functionality
- Search by first name, last name, email, or enrollment number
- Real-time filtering
- Case-insensitive search

### Form Validation
- **Client-side**: HTML5 validation
- **Server-side**: 
  - Required field validation
  - Unique constraint validation (email, enrollment number)
  - Email format validation
  - Data type validation

### Error Handling
- Custom error pages for 404 and 500 errors
- User-friendly error messages
- Database transaction rollback on errors
- Logging of errors

### Responsive Design
- Mobile-first approach
- Bootstrap 5 grid system
- Flexible layouts
- Touch-friendly buttons and forms

## Grade Level Classification

Based on GPA:
- **Excellent**: GPA >= 3.5
- **Very Good**: GPA >= 3.0
- **Good**: GPA >= 2.5
- **Average**: GPA >= 2.0
- **Below Average**: GPA < 2.0

## Configuration

Edit `app.py` to modify:
- Database URI
- Debug mode
- Secret key
- Port number

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_management.db'
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.run(debug=True, port=5000)
```

## Troubleshooting

### Database Issues
- If the database is corrupted, delete `student_management.db` and restart the app
- Database will be automatically recreated

### Port Already in Use
- Change the port in `app.py`: `app.run(port=5001)`
- Or kill the process using port 5000

### Import Errors
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

## Security Considerations

1. **Change Secret Key**: Update `app.config['SECRET_KEY']` in production
2. **Database**: Use SQLite for development only; use PostgreSQL for production
3. **HTTPS**: Enable HTTPS in production
4. **Input Validation**: All inputs are validated on server-side
5. **CSRF Protection**: Can be added with Flask-WTF

## Future Enhancements

- [ ] User authentication and authorization
- [ ] Student grades and courses management
- [ ] Export to PDF/Excel
- [ ] Email notifications
- [ ] Advanced analytics and reports
- [ ] Multi-user support
- [ ] API documentation (Swagger)
- [ ] Unit tests
- [ ] Docker support
- [ ] Deployment to cloud

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, email support@example.com or open an issue on GitHub.

## Author

**NotAmeet** - Initial work

## Acknowledgments

- Flask documentation
- Bootstrap documentation
- SQLAlchemy documentation
- Community feedback and suggestions

---

**Last Updated**: July 2024
**Version**: 1.0.0
