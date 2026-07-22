"""
Database models for Student Management System
Defines all database schemas and relationships
"""

from app import db
from datetime import datetime

class Student(db.Model):
    """Student model for database storage"""
    __tablename__ = 'students'
    
    # Primary Key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Personal Information
    first_name = db.Column(db.String(100), nullable=False, index=True)
    last_name = db.Column(db.String(100), nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(20), nullable=True)
    
    # Academic Information
    student_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    class_name = db.Column(db.String(50), nullable=True)
    roll_number = db.Column(db.Integer, nullable=True)
    
    # Address Information
    address = db.Column(db.Text, nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    is_active = db.Column(db.Boolean, default=True, index=True)
    
    # Constraints
    __table_args__ = (
        db.Index('idx_name', 'first_name', 'last_name'),
        db.Index('idx_email_active', 'email', 'is_active'),
    )

    def __repr__(self):
        return f'<Student {self.first_name} {self.last_name}>'

    def __str__(self):
        return f'{self.first_name} {self.last_name} ({self.student_id})'

    @property
    def full_name(self):
        """Get full name of student"""
        return f'{self.first_name} {self.last_name}'

    def to_dict(self):
        """Convert student object to dictionary"""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone or 'N/A',
            'student_id': self.student_id,
            'class_name': self.class_name or 'Unassigned',
            'roll_number': self.roll_number,
            'address': self.address or 'N/A',
            'city': self.city or 'N/A',
            'state': self.state or 'N/A',
            'postal_code': self.postal_code or 'N/A',
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'is_active': self.is_active
        }

    @staticmethod
    def get_by_email(email):
        """Get student by email"""
        return Student.query.filter_by(email=email.lower()).first()

    @staticmethod
    def get_by_student_id(student_id):
        """Get student by student ID"""
        return Student.query.filter_by(student_id=student_id.upper()).first()

    @staticmethod
    def get_active_students():
        """Get all active students"""
        return Student.query.filter_by(is_active=True).all()

    @staticmethod
    def get_students_by_class(class_name):
        """Get all students in a specific class"""
        return Student.query.filter_by(class_name=class_name, is_active=True).all()

    def deactivate(self):
        """Mark student as inactive (soft delete)"""
        self.is_active = False
        db.session.commit()

    def activate(self):
        """Reactivate student"""
        self.is_active = True
        db.session.commit()

    def update(self, **kwargs):
        """Update student attributes"""
        for key, value in kwargs.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'is_active']:
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        db.session.commit()
        return self
