# Student Management System

A comprehensive web-based Student Management System built with Flask, SQLite, and Bootstrap. This application allows administrators and educators to manage student records, track academic progress, and maintain student information efficiently.

## Features

- **Student Management**: Add, update, view, and delete student records
- **Course Management**: Manage courses and their details
- **Grade Management**: Track and manage student grades
- **Search Functionality**: Search students by name, ID, or email
- **Responsive Design**: Bootstrap-based responsive UI
- **Data Validation**: Input validation and error handling
- **Database**: SQLite with SQLAlchemy ORM
- **User-friendly Interface**: Clean and intuitive Jinja2 templates

## Technologies Used

- **Backend**: Flask 2.3.3
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5
- **Templating**: Jinja2
- **Python Version**: 3.8+

## Project Structure

```
Student-management-system/
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── utils.py
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   └── script.js
│   │   └── images/
│   └── templates/
│       ├── base.html
│       ├── index.html
│       ├── students/
│       │   ├── index.html
│       │   ├── add.html
│       │   ├── edit.html
│       │   └── view.html
│       ├── courses/
│       │   ├── index.html
│       │   ├── add.html
│       │   └── edit.html
│       ├── grades/
│       │   ├── index.html
│       │   ├── add.html
│       │   └── edit.html
│       └── errors/
│           ├── 404.html
│           └── 500.html
├── config.py
├── run.py
├── requirements.txt
└── README.md
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

5. **Initialize the database**
   ```bash
   python
   >>> from app import create_app, db
   >>> app = create_app()
   >>> with app.app_context():
   ...     db.create_all()
   >>> exit()
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

7. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## Usage

### Adding a Student
1. Navigate to the Students section
2. Click on "Add New Student"
3. Fill in the student details (name, email, enrollment number, etc.)
4. Click "Save" to add the student

### Managing Grades
1. Go to the Grades section
2. Select a student and course
3. Enter the grade
4. Save the grade

### Searching Students
1. Use the search bar on the Students page
2. Search by student name, email, or enrollment number

## Error Handling

The application includes comprehensive error handling:
- Form validation on both client and server side
- Database error handling
- 404 error pages for missing resources
- 500 error pages for server errors
- User-friendly error messages

## Database Models

### Student
- ID (Primary Key)
- First Name
- Last Name
- Email (Unique)
- Enrollment Number (Unique)
- Phone Number
- Date of Birth
- Address
- Created At
- Updated At

### Course
- ID (Primary Key)
- Course Code (Unique)
- Course Name
- Description
- Credits
- Created At
- Updated At

### Grade
- ID (Primary Key)
- Student ID (Foreign Key)
- Course ID (Foreign Key)
- Grade (Letter Grade)
- Score (Numerical Score)
- Semester
- Created At
- Updated At

## API Endpoints

### Students
- `GET /` - Dashboard
- `GET /students` - List all students
- `GET /students/add` - Add student form
- `POST /students/add` - Create new student
- `GET /students/<id>` - View student details
- `GET /students/<id>/edit` - Edit student form
- `POST /students/<id>/edit` - Update student
- `POST /students/<id>/delete` - Delete student

### Courses
- `GET /courses` - List all courses
- `GET /courses/add` - Add course form
- `POST /courses/add` - Create new course
- `GET /courses/<id>/edit` - Edit course form
- `POST /courses/<id>/edit` - Update course
- `POST /courses/<id>/delete` - Delete course

### Grades
- `GET /grades` - List all grades
- `GET /grades/add` - Add grade form
- `POST /grades/add` - Create new grade
- `GET /grades/<id>/edit` - Edit grade form
- `POST /grades/<id>/edit` - Update grade
- `POST /grades/<id>/delete` - Delete grade

## Configuration

Edit `config.py` to customize settings:
- Database configuration
- Flask settings
- Application debug mode

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions, please open an issue on the GitHub repository.

## Author

NotAmeet
