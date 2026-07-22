from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app import db
from app.models import Student, Course, Grade
from app.forms import StudentForm, CourseForm, GradeForm, SearchForm
from app.utils import commit_to_db, flash_errors, calculate_letter_grade, get_or_404
from sqlalchemy import or_

# Create blueprints
main_bp = Blueprint('main', __name__)
students_bp = Blueprint('students', __name__)
courses_bp = Blueprint('courses', __name__)
grades_bp = Blueprint('grades', __name__)

# ==================== MAIN ROUTES ====================

@main_bp.route('/')
def index():
    """Dashboard"""
    total_students = Student.query.count()
    total_courses = Course.query.count()
    total_grades = Grade.query.count()
    
    recent_students = Student.query.order_by(Student.created_at.desc()).limit(5).all()
    
    stats = {
        'total_students': total_students,
        'total_courses': total_courses,
        'total_grades': total_grades,
    }
    
    return render_template('index.html', stats=stats, recent_students=recent_students)

# ==================== STUDENT ROUTES ====================

@students_bp.route('/', methods=['GET', 'POST'])
def list_students():
    """List all students with search functionality"""
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '', type=str)
    
    query = Student.query
    
    if search_query:
        query = query.filter(
            or_(
                Student.first_name.ilike(f'%{search_query}%'),
                Student.last_name.ilike(f'%{search_query}%'),
                Student.email.ilike(f'%{search_query}%'),
                Student.enrollment_number.ilike(f'%{search_query}%')
            )
        )
    
    students = query.order_by(Student.created_at.desc()).paginate(page=page, per_page=10)
    
    return render_template('students/index.html', students=students, search_query=search_query)

@students_bp.route('/add', methods=['GET', 'POST'])
def add_student():
    """Add a new student"""
    form = StudentForm()
    
    if form.validate_on_submit():
        try:
            student = Student(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                enrollment_number=form.enrollment_number.data,
                phone=form.phone.data,
                date_of_birth=form.date_of_birth.data,
                address=form.address.data
            )
            db.session.add(student)
            db.session.commit()
            flash(f'Student {student.get_full_name()} added successfully!', 'success')
            return redirect(url_for('students.list_students'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding student: {str(e)}', 'danger')
    else:
        flash_errors(form)
    
    return render_template('students/add.html', form=form)

@students_bp.route('/<int:student_id>')
def view_student(student_id):
    """View student details"""
    student = get_or_404(Student, student_id)
    grades = student.grades.all()
    return render_template('students/view.html', student=student, grades=grades)

@students_bp.route('/<int:student_id>/edit', methods=['GET', 'POST'])
def edit_student(student_id):
    """Edit student"""
    student = get_or_404(Student, student_id)
    form = StudentForm()
    
    if form.validate_on_submit():
        try:
            student.first_name = form.first_name.data
            student.last_name = form.last_name.data
            student.email = form.email.data
            student.enrollment_number = form.enrollment_number.data
            student.phone = form.phone.data
            student.date_of_birth = form.date_of_birth.data
            student.address = form.address.data
            db.session.commit()
            flash('Student updated successfully!', 'success')
            return redirect(url_for('students.view_student', student_id=student.id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating student: {str(e)}', 'danger')
    elif request.method == 'GET':
        form.first_name.data = student.first_name
        form.last_name.data = student.last_name
        form.email.data = student.email
        form.enrollment_number.data = student.enrollment_number
        form.phone.data = student.phone
        form.date_of_birth.data = student.date_of_birth
        form.address.data = student.address
    else:
        flash_errors(form)
    
    return render_template('students/edit.html', form=form, student=student)

@students_bp.route('/<int:student_id>/delete', methods=['POST'])
def delete_student(student_id):
    """Delete student"""
    student = get_or_404(Student, student_id)
    
    try:
        name = student.get_full_name()
        db.session.delete(student)
        db.session.commit()
        flash(f'Student {name} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting student: {str(e)}', 'danger')
    
    return redirect(url_for('students.list_students'))

# ==================== COURSE ROUTES ====================

@courses_bp.route('/', methods=['GET'])
def list_courses():
    """List all courses"""
    page = request.args.get('page', 1, type=int)
    courses = Course.query.order_by(Course.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('courses/index.html', courses=courses)

@courses_bp.route('/add', methods=['GET', 'POST'])
def add_course():
    """Add a new course"""
    form = CourseForm()
    
    if form.validate_on_submit():
        try:
            course = Course(
                course_code=form.course_code.data,
                course_name=form.course_name.data,
                description=form.description.data,
                credits=form.credits.data
            )
            db.session.add(course)
            db.session.commit()
            flash(f'Course {course.course_code} added successfully!', 'success')
            return redirect(url_for('courses.list_courses'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding course: {str(e)}', 'danger')
    else:
        flash_errors(form)
    
    return render_template('courses/add.html', form=form)

@courses_bp.route('/<int:course_id>/edit', methods=['GET', 'POST'])
def edit_course(course_id):
    """Edit course"""
    course = get_or_404(Course, course_id)
    form = CourseForm()
    
    if form.validate_on_submit():
        try:
            course.course_code = form.course_code.data
            course.course_name = form.course_name.data
            course.description = form.description.data
            course.credits = form.credits.data
            db.session.commit()
            flash('Course updated successfully!', 'success')
            return redirect(url_for('courses.list_courses'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating course: {str(e)}', 'danger')
    elif request.method == 'GET':
        form.course_code.data = course.course_code
        form.course_name.data = course.course_name
        form.description.data = course.description
        form.credits.data = course.credits
    else:
        flash_errors(form)
    
    return render_template('courses/edit.html', form=form, course=course)

@courses_bp.route('/<int:course_id>/delete', methods=['POST'])
def delete_course(course_id):
    """Delete course"""
    course = get_or_404(Course, course_id)
    
    try:
        code = course.course_code
        db.session.delete(course)
        db.session.commit()
        flash(f'Course {code} deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting course: {str(e)}', 'danger')
    
    return redirect(url_for('courses.list_courses'))

# ==================== GRADE ROUTES ====================

@grades_bp.route('/', methods=['GET'])
def list_grades():
    """List all grades"""
    page = request.args.get('page', 1, type=int)
    grades = Grade.query.order_by(Grade.created_at.desc()).paginate(page=page, per_page=10)
    return render_template('grades/index.html', grades=grades)

@grades_bp.route('/add', methods=['GET', 'POST'])
def add_grade():
    """Add a new grade"""
    form = GradeForm()
    
    if form.validate_on_submit():
        try:
            letter_grade = calculate_letter_grade(form.score.data)
            grade = Grade(
                student_id=form.student_id.data,
                course_id=form.course_id.data,
                score=form.score.data,
                grade=letter_grade,
                semester=form.semester.data,
                remarks=form.remarks.data
            )
            db.session.add(grade)
            db.session.commit()
            flash('Grade added successfully!', 'success')
            return redirect(url_for('grades.list_grades'))
        except Exception as e:
            db.session.rollback()
            if 'UNIQUE constraint failed' in str(e):
                flash('Grade for this student-course-semester combination already exists!', 'danger')
            else:
                flash(f'Error adding grade: {str(e)}', 'danger')
    else:
        flash_errors(form)
    
    return render_template('grades/add.html', form=form)

@grades_bp.route('/<int:grade_id>/edit', methods=['GET', 'POST'])
def edit_grade(grade_id):
    """Edit grade"""
    grade = get_or_404(Grade, grade_id)
    form = GradeForm()
    
    if form.validate_on_submit():
        try:
            letter_grade = calculate_letter_grade(form.score.data)
            grade.student_id = form.student_id.data
            grade.course_id = form.course_id.data
            grade.score = form.score.data
            grade.grade = letter_grade
            grade.semester = form.semester.data
            grade.remarks = form.remarks.data
            db.session.commit()
            flash('Grade updated successfully!', 'success')
            return redirect(url_for('grades.list_grades'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating grade: {str(e)}', 'danger')
    elif request.method == 'GET':
        form.student_id.data = grade.student_id
        form.course_id.data = grade.course_id
        form.score.data = grade.score
        form.semester.data = grade.semester
        form.remarks.data = grade.remarks
    else:
        flash_errors(form)
    
    return render_template('grades/edit.html', form=form, grade=grade)

@grades_bp.route('/<int:grade_id>/delete', methods=['POST'])
def delete_grade(grade_id):
    """Delete grade"""
    grade = get_or_404(Grade, grade_id)
    
    try:
        db.session.delete(grade)
        db.session.commit()
        flash('Grade deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting grade: {str(e)}', 'danger')
    
    return redirect(url_for('grades.list_grades'))
