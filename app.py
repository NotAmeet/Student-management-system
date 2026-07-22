from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from models import db, Student
from datetime import datetime
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_management.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

db.init_app(app)

with app.app_context():
    db.create_all()

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Home page - Dashboard"""
    total_students = Student.query.count()
    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()
    return render_template('index.html', 
                         total_students=total_students,
                         recent_students=recent_students)

@app.route('/students')
def list_students():
    """List all students with pagination and search"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    
    query = Student.query
    
    if search:
        query = query.filter(
            (Student.first_name.ilike(f'%{search}%')) |
            (Student.last_name.ilike(f'%{search}%')) |
            (Student.email.ilike(f'%{search}%')) |
            (Student.enrollment_number.ilike(f'%{search}%'))
        )
    
    students = query.order_by(Student.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('students/list.html', students=students, search=search)

@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    """Add a new student"""
    if request.method == 'POST':
        try:
            # Check if enrollment number already exists
            if Student.query.filter_by(enrollment_number=request.form.get('enrollment_number')).first():
                flash('Enrollment number already exists!', 'danger')
                return redirect(url_for('add_student'))
            
            # Check if email already exists
            if Student.query.filter_by(email=request.form.get('email')).first():
                flash('Email already registered!', 'danger')
                return redirect(url_for('add_student'))
            
            # Validate required fields
            required_fields = ['first_name', 'last_name', 'email', 'enrollment_number', 'phone']
            for field in required_fields:
                if not request.form.get(field):
                    flash(f'{field.replace("_", " ").title()} is required!', 'danger')
                    return redirect(url_for('add_student'))
            
            student = Student(
                first_name=request.form.get('first_name'),
                last_name=request.form.get('last_name'),
                email=request.form.get('email'),
                enrollment_number=request.form.get('enrollment_number'),
                phone=request.form.get('phone'),
                date_of_birth=request.form.get('date_of_birth') or None,
                address=request.form.get('address'),
                gpa=float(request.form.get('gpa', 0.0)),
                created_at=datetime.utcnow()
            )
            
            db.session.add(student)
            db.session.commit()
            flash(f'Student {student.first_name} {student.last_name} added successfully!', 'success')
            return redirect(url_for('list_students'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding student: {str(e)}', 'danger')
            return redirect(url_for('add_student'))
    
    return render_template('students/form.html', action='Add')

@app.route('/students/<int:student_id>')
def view_student(student_id):
    """View student details"""
    student = Student.query.get_or_404(student_id)
    return render_template('students/view.html', student=student)

@app.route('/students/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    """Edit student details"""
    student = Student.query.get_or_404(student_id)
    
    if request.method == 'POST':
        try:
            # Check if new enrollment number already exists (and it's not the same student)
            enrollment_number = request.form.get('enrollment_number')
            if enrollment_number != student.enrollment_number:
                if Student.query.filter_by(enrollment_number=enrollment_number).first():
                    flash('Enrollment number already exists!', 'danger')
                    return redirect(url_for('edit_student', student_id=student_id))
            
            # Check if new email already exists (and it's not the same student)
            email = request.form.get('email')
            if email != student.email:
                if Student.query.filter_by(email=email).first():
                    flash('Email already registered!', 'danger')
                    return redirect(url_for('edit_student', student_id=student_id))
            
            student.first_name = request.form.get('first_name')
            student.last_name = request.form.get('last_name')
            student.email = email
            student.enrollment_number = enrollment_number
            student.phone = request.form.get('phone')
            student.date_of_birth = request.form.get('date_of_birth') or None
            student.address = request.form.get('address')
            student.gpa = float(request.form.get('gpa', 0.0))
            student.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('view_student', student_id=student_id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating student: {str(e)}', 'danger')
            return redirect(url_for('edit_student', student_id=student_id))
    
    return render_template('students/form.html', action='Edit', student=student)

@app.route('/students/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    """Delete a student"""
    student = Student.query.get_or_404(student_id)
    
    try:
        name = f"{student.first_name} {student.last_name}"
        db.session.delete(student)
        db.session.commit()
        flash(f'Student {name} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'danger')
    
    return redirect(url_for('list_students'))

# ==================== API ROUTES ====================

@app.route('/api/students', methods=['GET'])
def api_get_students():
    """API endpoint to get all students as JSON"""
    students = Student.query.all()
    return jsonify([
        {
            'id': s.id,
            'first_name': s.first_name,
            'last_name': s.last_name,
            'email': s.email,
            'enrollment_number': s.enrollment_number,
            'gpa': s.gpa
        }
        for s in students
    ])

@app.route('/api/students/<int:student_id>', methods=['GET'])
def api_get_student(student_id):
    """API endpoint to get a specific student as JSON"""
    student = Student.query.get_or_404(student_id)
    return jsonify({
        'id': student.id,
        'first_name': student.first_name,
        'last_name': student.last_name,
        'email': student.email,
        'enrollment_number': student.enrollment_number,
        'phone': student.phone,
        'date_of_birth': student.date_of_birth.isoformat() if student.date_of_birth else None,
        'address': student.address,
        'gpa': student.gpa,
        'created_at': student.created_at.isoformat()
    })

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    db.session.rollback()
    return render_template('errors/500.html'), 500

# ==================== CONTEXT PROCESSORS ====================

@app.context_processor
def inject_now():
    """Make datetime available in templates"""
    return {'now': datetime.utcnow()}

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
