from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decimal import Decimal
import json

db = SQLAlchemy()

class Student(db.Model):
    """
    Student model for storing student information.
    
    Attributes:
        id (int): Primary key - Auto-generated unique identifier
        student_id (str): Unique student identification number
        name (str): Full name of the student
        age (int): Age of the student
        email (str): Email address of the student (unique)
        marks (list): List of marks/scores in different subjects
        average (float): Average marks calculated from marks
        grade (str): Letter grade based on average marks
        created_at (datetime): Timestamp when record was created
        updated_at (datetime): Timestamp when record was last updated
    """
    
    __tablename__ = 'students'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Student Identification
    student_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # Personal Information
    name = db.Column(db.String(150), nullable=False, index=True)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    
    # Academic Information
    marks = db.Column(db.JSON, nullable=False, default=list)  # Stores list of marks
    average = db.Column(db.Float, nullable=False, default=0.0)
    grade = db.Column(db.String(2), nullable=False, default='F')
    
    # Timestamps
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """String representation of Student object"""
        return f'<Student {self.student_id}: {self.name} (Grade: {self.grade})>'
    
    # ==================== CALCULATION METHODS ====================
    
    def calculate_average(self):
        """
        Calculate average marks from the marks list.
        
        Returns:
            float: Average marks rounded to 2 decimal places
        """
        if not self.marks or len(self.marks) == 0:
            return 0.0
        
        try:
            total_marks = sum(float(mark) for mark in self.marks if mark is not None)
            average = total_marks / len(self.marks)
            return round(average, 2)
        except (TypeError, ValueError):
            return 0.0
    
    def calculate_grade(self, average=None):
        """
        Calculate letter grade based on average marks.
        
        Grading Scale:
        - A: >= 90
        - B: >= 80
        - C: >= 70
        - D: >= 60
        - F: < 60
        
        Args:
            average (float, optional): Average marks to calculate grade from.
                                      If None, uses self.average
        
        Returns:
            str: Letter grade (A, B, C, D, F)
        """
        avg = average if average is not None else self.average
        
        if avg >= 90:
            return 'A'
        elif avg >= 80:
            return 'B'
        elif avg >= 70:
            return 'C'
        elif avg >= 60:
            return 'D'
        else:
            return 'F'
    
    def calculate_percentage(self):
        """
        Calculate percentage of marks.
        
        Returns:
            float: Percentage rounded to 2 decimal places
        """
        if not self.marks or len(self.marks) == 0:
            return 0.0
        
        return round((self.average / 100) * 100, 2)
    
    def get_gpa(self, scale=4.0):
        """
        Convert average marks to GPA (Grade Point Average).
        
        Args:
            scale (float): GPA scale (default: 4.0)
        
        Returns:
            float: GPA rounded to 2 decimal places
        """
        # Convert percentage to GPA on 4.0 scale
        gpa = (self.average / 100) * scale
        return round(gpa, 2)
    
    def is_passed(self, passing_percentage=40):
        """
        Check if student passed based on passing percentage.
        
        Args:
            passing_percentage (int): Passing percentage threshold (default: 40)
        
        Returns:
            bool: True if passed, False otherwise
        """
        return self.average >= passing_percentage
    
    def add_marks(self, mark):
        """
        Add a new mark to the marks list.
        
        Args:
            mark (float): Mark to add
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            mark_value = float(mark)
            if 0 <= mark_value <= 100:
                if not isinstance(self.marks, list):
                    self.marks = []
                self.marks.append(mark_value)
                self.average = self.calculate_average()
                self.grade = self.calculate_grade()
                return True
            return False
        except (TypeError, ValueError):
            return False
    
    def update_marks(self, marks_list):
        """
        Update all marks at once.
        
        Args:
            marks_list (list): List of marks to set
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            validated_marks = [float(mark) for mark in marks_list if 0 <= float(mark) <= 100]
            if len(validated_marks) == len(marks_list):
                self.marks = validated_marks
                self.average = self.calculate_average()
                self.grade = self.calculate_grade()
                return True
            return False
        except (TypeError, ValueError):
            return False
    
    # ==================== SERIALIZATION METHODS ====================
    
    def to_dict(self, include_timestamps=True):
        """
        Convert Student object to dictionary for API responses.
        
        Args:
            include_timestamps (bool): Include created_at and updated_at fields
        
        Returns:
            dict: Dictionary representation of the student
        """
        student_dict = {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'marks': self.marks if isinstance(self.marks, list) else [],
            'average': self.average,
            'grade': self.grade,
            'gpa': self.get_gpa(),
            'percentage': self.calculate_percentage(),
            'is_passed': self.is_passed(),
            'status': 'Passed' if self.is_passed() else 'Failed'
        }
        
        if include_timestamps:
            student_dict['created_at'] = self.created_at.isoformat() if self.created_at else None
            student_dict['updated_at'] = self.updated_at.isoformat() if self.updated_at else None
        
        return student_dict
    
    def to_json(self, include_timestamps=True):
        """
        Convert Student object to JSON string.
        
        Args:
            include_timestamps (bool): Include timestamp fields
        
        Returns:
            str: JSON string representation of the student
        """
        return json.dumps(self.to_dict(include_timestamps=include_timestamps), indent=2)
    
    def to_detailed_dict(self):
        """
        Convert Student object to a detailed dictionary with additional information.
        
        Returns:
            dict: Detailed dictionary representation including statistics
        """
        marks_count = len(self.marks) if isinstance(self.marks, list) else 0
        highest_mark = max(self.marks) if marks_count > 0 else 0
        lowest_mark = min(self.marks) if marks_count > 0 else 0
        
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'age': self.age,
            'email': self.email,
            'marks': {
                'list': self.marks if isinstance(self.marks, list) else [],
                'count': marks_count,
                'average': self.average,
                'highest': highest_mark,
                'lowest': lowest_mark,
                'total': sum(self.marks) if marks_count > 0 else 0
            },
            'grade': {
                'letter_grade': self.grade,
                'percentage': self.calculate_percentage(),
                'gpa': self.get_gpa(),
                'status': 'Passed' if self.is_passed() else 'Failed'
            },
            'metadata': {
                'created_at': self.created_at.isoformat() if self.created_at else None,
                'updated_at': self.updated_at.isoformat() if self.updated_at else None,
                'age_group': self._get_age_group(),
                'grade_category': self._get_grade_category()
            }
        }
    
    def to_csv_row(self):
        """
        Convert Student object to CSV row format.
        
        Returns:
            str: Comma-separated values for CSV export
        """
        marks_str = '|'.join(str(mark) for mark in (self.marks if isinstance(self.marks, list) else []))
        return f"{self.id},{self.student_id},{self.name},{self.age},{self.email},{marks_str},{self.average},{self.grade}"
    
    def to_list(self):
        """
        Convert Student object to list format for tabular display.
        
        Returns:
            list: List of student attributes in order
        """
        return [
            self.id,
            self.student_id,
            self.name,
            self.age,
            self.email,
            str(self.marks),
            self.average,
            self.grade,
            self.get_gpa(),
            'Passed' if self.is_passed() else 'Failed'
        ]
    
    def to_summary(self):
        """
        Get a brief summary of the student.
        
        Returns:
            dict: Summary dictionary with key information
        """
        return {
            'student_id': self.student_id,
            'name': self.name,
            'grade': self.grade,
            'average': self.average,
            'status': 'Passed' if self.is_passed() else 'Failed'
        }
    
    # ==================== DESERIALIZATION METHODS ====================
    
    @classmethod
    def from_dict(cls, data):
        """
        Create a Student object from a dictionary.
        
        Args:
            data (dict): Dictionary containing student data
        
        Returns:
            Student: Student object or None if invalid
        """
        try:
            student = cls(
                student_id=data.get('student_id'),
                name=data.get('name'),
                age=int(data.get('age', 0)),
                email=data.get('email'),
                marks=data.get('marks', [])
            )
            student.average = student.calculate_average()
            student.grade = student.calculate_grade()
            return student
        except (KeyError, TypeError, ValueError):
            return None
    
    @classmethod
    def from_json(cls, json_string):
        """
        Create a Student object from a JSON string.
        
        Args:
            json_string (str): JSON string containing student data
        
        Returns:
            Student: Student object or None if invalid
        """
        try:
            data = json.loads(json_string)
            return cls.from_dict(data)
        except (json.JSONDecodeError, ValueError):
            return None
    
    # ==================== UTILITY METHODS ====================
    
    def _get_age_group(self):
        """
        Get age group category.
        
        Returns:
            str: Age group classification
        """
        if self.age < 18:
            return 'Minor'
        elif self.age < 25:
            return 'Young Adult'
        elif self.age < 35:
            return 'Adult'
        else:
            return 'Senior'
    
    def _get_grade_category(self):
        """
        Get grade category description.
        
        Returns:
            str: Grade category
        """
        if self.grade == 'A':
            return 'Outstanding'
        elif self.grade == 'B':
            return 'Good'
        elif self.grade == 'C':
            return 'Satisfactory'
        elif self.grade == 'D':
            return 'Needs Improvement'
        else:
            return 'Failed'
    
    def get_marks_distribution(self):
        """
        Get distribution of marks for analysis.
        
        Returns:
            dict: Distribution statistics
        """
        if not self.marks or len(self.marks) == 0:
            return {'distribution': {}, 'total_subjects': 0}
        
        marks_count = len(self.marks)
        above_80 = len([m for m in self.marks if m >= 80])
        between_60_80 = len([m for m in self.marks if 60 <= m < 80])
        below_60 = len([m for m in self.marks if m < 60])
        
        return {
            'total_subjects': marks_count,
            'above_80': above_80,
            'between_60_80': between_60_80,
            'below_60': below_60,
            'distribution': {
                'above_80_percentage': round((above_80 / marks_count) * 100, 2),
                'between_60_80_percentage': round((between_60_80 / marks_count) * 100, 2),
                'below_60_percentage': round((below_60 / marks_count) * 100, 2)
            }
        }
    
    def update_from_dict(self, data):
        """
        Update student attributes from a dictionary.
        
        Args:
            data (dict): Dictionary with fields to update
        
        Returns:
            bool: True if update successful, False otherwise
        """
        try:
            if 'name' in data:
                self.name = data['name']
            if 'age' in data:
                self.age = int(data['age'])
            if 'email' in data:
                self.email = data['email']
            if 'marks' in data:
                if not self.update_marks(data['marks']):
                    return False
            
            self.updated_at = datetime.utcnow()
            return True
        except (TypeError, ValueError, KeyError):
            return False
    
    def validate(self):
        """
        Validate student data.
        
        Returns:
            tuple: (bool: is_valid, list: error_messages)
        """
        errors = []
        
        if not self.student_id or len(self.student_id) == 0:
            errors.append('Student ID is required')
        
        if not self.name or len(self.name) < 2:
            errors.append('Name must be at least 2 characters')
        
        if self.age < 5 or self.age > 120:
            errors.append('Age must be between 5 and 120')
        
        if not self.email or '@' not in self.email:
            errors.append('Valid email is required')
        
        if not isinstance(self.marks, list):
            errors.append('Marks must be a list')
        
        for mark in (self.marks if isinstance(self.marks, list) else []):
            try:
                mark_val = float(mark)
                if mark_val < 0 or mark_val > 100:
                    errors.append(f'Mark {mark} is out of range (0-100)')
            except (TypeError, ValueError):
                errors.append(f'Invalid mark value: {mark}')
        
        return (len(errors) == 0, errors)
    
    def __eq__(self, other):
        """Check equality based on student_id"""
        if not isinstance(other, Student):
            return False
        return self.student_id == other.student_id
    
    def __hash__(self):
        """Make Student hashable"""
        return hash(self.student_id)
    
    def __lt__(self, other):
        """Compare students by average marks"""
        return self.average < other.average
    
    def __le__(self, other):
        """Compare students by average marks"""
        return self.average <= other.average
    
    def __gt__(self, other):
        """Compare students by average marks"""
        return self.average > other.average
    
    def __ge__(self, other):
        """Compare students by average marks"""
        return self.average >= other.average
