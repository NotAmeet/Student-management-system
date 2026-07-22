from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    """Student model for storing student information"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    enrollment_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    address = db.Column(db.Text, nullable=True)
    gpa = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'
    
    def get_full_name(self):
        """Return full name of student"""
        return f'{self.first_name} {self.last_name}'
    
    def get_grade_level(self):
        """Determine grade level based on GPA"""
        if self.gpa >= 3.5:
            return 'Excellent'
        elif self.gpa >= 3.0:
            return 'Very Good'
        elif self.gpa >= 2.5:
            return 'Good'
        elif self.gpa >= 2.0:
            return 'Average'
        else:
            return 'Below Average'
    
    def to_dict(self):
        """Convert student to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'email': self.email,
            'enrollment_number': self.enrollment_number,
            'phone': self.phone,
            'date_of_birth': self.date_of_birth.isoformat() if self.date_of_birth else None,
            'address': self.address,
            'gpa': self.gpa,
            'grade_level': self.get_grade_level(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
