# Student Management System - Setup Guide

## Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- SQLite3 (comes with Python)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Initialize Database
```bash
# Create database tables
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Seed sample data (optional)
flask seed-db
```

### Step 3: Run Application
```bash
python app.py
```

The application will be available at `http://localhost:5000`

---

## Features

### 1. Homepage (`/`)
- Welcome page with system overview
- Quick statistics (total students, active students, classes)
- Navigation links to all features

### 2. Full Student Registration (`/add_student`)
- Comprehensive form with all student details
- Fields: Personal info, academic info, and address
- Form validation with error messages
- Database storage of complete student profiles

### 3. Quick Student Registration (`/register`)
- **New feature with 4 essential fields:**
  - **Student ID** (Auto-generated)
  - **Full Name** (Validation: 3-100 characters, letters only)
  - **Age** (Validation: 5-100 years)
  - **Email** (Validation: Valid email format, unique)
- Real-time field validation
- Progress bar showing form completion
- Bootstrap styling for responsive design
- Character counter for name field
- Success confirmation screen

### 4. View Students (`/view_students`)
- Display all registered students in a table
- Search functionality (name, email, student ID)
- Pagination support
- Edit/Delete/View actions
- Statistics dashboard
- Responsive table design

---

## API Endpoints

### Student Management APIs

#### Get All Students
```
GET /api/students
Query Parameters:
  - page (int): Page number (default: 1)
  - per_page (int): Items per page (default: 10)
  - search (string): Search term
  - class (string): Filter by class
  - sort_by (string): Sort by 'name', 'email', 'class', 'created_at'
  - order (string): 'asc' or 'desc'

Response:
{
  "success": true,
  "data": [...],
  "pagination": {...},
  "stats": {...}
}
```

#### Get Single Student
```
GET /api/students/<id>
Response: {
  "success": true,
  "data": {student_object}
}
```

#### Add Student (Full Form)
```
POST /add_student
Content-Type: application/json
Body: {
  "firstName": "string",
  "lastName": "string",
  "email": "string",
  "phone": "string",
  "studentId": "string",
  "class": "string",
  "rollNumber": "number",
  "address": "string",
  "city": "string",
  "state": "string",
  "postalCode": "string"
}
```

#### Quick Registration
```
POST /api/register
Content-Type: application/json
Body: {
  "firstName": "string",
  "lastName": "string",
  "email": "string",
  "age": "number",
  "studentId": "string"
}
```

#### Update Student
```
PUT /api/students/<id>
Content-Type: application/json
Body: {field_name: value, ...}
```

#### Delete Student
```
DELETE /api/students/<id>
```

#### Get Statistics
```
GET /api/statistics
Response: {
  "success": true,
  "data": {
    "total_students": number,
    "total_classes": number,
    "class_distribution": [...]
  }
}
```

---

## Validation Rules

### Full Name (Registration Form)
- ✓ Required field
- ✓ Minimum 3 characters
- ✓ Maximum 100 characters
- ✓ Only letters, spaces, hyphens, and apostrophes

### Age (Registration Form)
- ✓ Required field
- ✓ Numeric value
- ✓ Minimum: 5 years
- ✓ Maximum: 100 years

### Email (All Forms)
- ✓ Required field
- ✓ Valid email format (user@domain.com)
- ✓ Must be unique in database
- ✓ Converted to lowercase

### Student ID (All Forms)
- ✓ Required field
- ✓ Must be unique
- ✓ Auto-generated format: STU{timestamp}

### Phone Number (Full Form)
- ✓ Required field
- ✓ Minimum 10 digits

---

## Database Schema

### Students Table
```sql
CREATE TABLE students (
  id INTEGER PRIMARY KEY,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  email VARCHAR(120) UNIQUE NOT NULL,
  phone VARCHAR(20),
  student_id VARCHAR(50) UNIQUE NOT NULL,
  class_name VARCHAR(50),
  roll_number INTEGER,
  address TEXT,
  city VARCHAR(100),
  state VARCHAR(100),
  postal_code VARCHAR(20),
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  is_active BOOLEAN DEFAULT TRUE
)
```

---

## File Structure

```
student-management-system/
├── app.py                          # Main Flask application
├── registration_routes.py          # Registration API routes
├── requirements.txt                # Python dependencies
├── student_management.db           # SQLite database
├── templates/
│   ├── index.html                 # Homepage
│   ├── add_student.html           # Full registration form
│   ├── register.html              # Quick registration form
│   └── view_students.html         # View all students
├── static/
│   ├── styles.css                 # Global CSS styling
│   └── script.js                  # JavaScript utilities
└── README.md                       # This file
```

---

## Key Features

### Frontend
- **Responsive Bootstrap Design** - Works on desktop, tablet, mobile
- **Real-time Form Validation** - Instant feedback on input
- **Progress Bars** - Visual indication of form completion
- **Success Animations** - Engaging user experience
- **Character Counters** - Input length monitoring
- **Search Functionality** - Quick student lookup
- **Pagination** - Efficient data display
- **Error Alerts** - Clear error messaging

### Backend
- **SQLAlchemy ORM** - Type-safe database operations
- **Flask-Migrate** - Database versioning
- **Comprehensive Logging** - Error tracking and debugging
- **Input Validation** - Data integrity
- **Soft Deletes** - Student records marked inactive
- **API Documentation** - Clear endpoint specifications

---

## Customization

### Change Database
In `app.py`, modify the `SQLALCHEMY_DATABASE_URI`:
```python
# For PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/student_db'

# For MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/student_db'
```

### Modify Styling
Edit `static/styles.css` to customize colors, fonts, and layouts.

### Add Fields to Registration
1. Add field to `register.html` form
2. Add validation in JavaScript
3. Add field to API payload
4. Add field to database model

---

## Troubleshooting

### Database Errors
```bash
# Reset database (WARNING: Deletes all data)
rm student_management.db
flask db init
flask db upgrade
```

### Port Already in Use
```bash
# Use different port
python app.py --port 5001
```

### Module Not Found
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## Security Notes

⚠️ **Development Mode:**
- Change `SECRET_KEY` in production
- Set `debug=False` in production
- Use environment variables for sensitive data
- Implement authentication/authorization
- Add CSRF protection
- Validate all user inputs

---

## Support

For issues or questions, please check:
1. Application logs for errors
2. Browser console for frontend errors
3. Database integrity
4. API request/response payloads

---

**Last Updated:** 2024
**Version:** 1.0.0
