from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField, SubmitField
from wtforms.fields import DateField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, ValidationError
from app.models import Student, Course

class StudentForm(FlaskForm):
    """Student form"""
    first_name = StringField('First Name', validators=[
        DataRequired(message='First name is required'),
        Length(min=2, max=100, message='First name must be between 2 and 100 characters')
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(message='Last name is required'),
        Length(min=2, max=100, message='Last name must be between 2 and 100 characters')
    ])
    email = StringField('Email', validators=[
        DataRequired(message='Email is required'),
        Email(message='Invalid email address')
    ])
    enrollment_number = StringField('Enrollment Number', validators=[
        DataRequired(message='Enrollment number is required'),
        Length(min=5, max=50, message='Enrollment number must be between 5 and 50 characters')
    ])
    phone = StringField('Phone Number', validators=[
        Optional(),
        Length(min=10, max=20, message='Phone number must be between 10 and 20 characters')
    ])
    date_of_birth = DateField('Date of Birth', validators=[Optional()])
    address = TextAreaField('Address', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Student')
    
    def validate_email(self, email):
        """Validate email uniqueness"""
        student = Student.query.filter_by(email=email.data).first()
        if student:
            raise ValidationError('Email already registered')
    
    def validate_enrollment_number(self, enrollment_number):
        """Validate enrollment number uniqueness"""
        student = Student.query.filter_by(enrollment_number=enrollment_number.data).first()
        if student:
            raise ValidationError('Enrollment number already exists')

class CourseForm(FlaskForm):
    """Course form"""
    course_code = StringField('Course Code', validators=[
        DataRequired(message='Course code is required'),
        Length(min=3, max=50, message='Course code must be between 3 and 50 characters')
    ])
    course_name = StringField('Course Name', validators=[
        DataRequired(message='Course name is required'),
        Length(min=3, max=150, message='Course name must be between 3 and 150 characters')
    ])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    credits = IntegerField('Credits', validators=[
        DataRequired(message='Credits is required'),
        NumberRange(min=1, max=10, message='Credits must be between 1 and 10')
    ])
    submit = SubmitField('Save Course')
    
    def validate_course_code(self, course_code):
        """Validate course code uniqueness"""
        course = Course.query.filter_by(course_code=course_code.data).first()
        if course:
            raise ValidationError('Course code already exists')

class GradeForm(FlaskForm):
    """Grade form"""
    student_id = SelectField('Student', coerce=int, validators=[DataRequired()])
    course_id = SelectField('Course', coerce=int, validators=[DataRequired()])
    score = FloatField('Score', validators=[
        DataRequired(message='Score is required'),
        NumberRange(min=0, max=100, message='Score must be between 0 and 100')
    ])
    semester = StringField('Semester', validators=[
        DataRequired(message='Semester is required'),
        Length(min=3, max=50, message='Semester must be between 3 and 50 characters')
    ])
    remarks = TextAreaField('Remarks', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Grade')
    
    def __init__(self, *args, **kwargs):
        super(GradeForm, self).__init__(*args, **kwargs)
        self.student_id.choices = [(s.id, s.get_full_name()) for s in Student.query.all()]
        self.course_id.choices = [(c.id, c.course_name) for c in Course.query.all()]

class SearchForm(FlaskForm):
    """Search form"""
    search_query = StringField('Search', validators=[
        Optional(),
        Length(max=100, message='Search query must not exceed 100 characters')
    ])
    submit = SubmitField('Search')
