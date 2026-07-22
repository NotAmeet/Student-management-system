"""
Seed data for Student Management System
Run this to populate the database with sample students
"""

from app import app, db
from models import Student
from datetime import datetime

def seed_database():
    """Seed the database with sample student data"""
    
    # Check if data already exists
    if Student.query.first():
        print("⚠️  Database already has data. Skipping seed.")
        return
    
    sample_students = [
        Student(
            first_name='Aman',
            last_name='Bhatt',
            email='aman.bhatt@example.com',
            phone='+91-9876543210',
            student_id='STU001001',
            class_name='Class 10',
            roll_number=5,
            address='123 Main Street, Mumbai',
            city='Mumbai',
            state='Maharashtra',
            postal_code='400001',
            is_active=True
        ),
        Student(
            first_name='Priya',
            last_name='Joshi',
            email='priya.joshi@example.com',
            phone='+91-8765432109',
            student_id='STU001002',
            class_name='Class 9',
            roll_number=12,
            address='456 Oak Avenue, Delhi',
            city='Delhi',
            state='Delhi',
            postal_code='110001',
            is_active=True
        ),
        Student(
            first_name='Raj',
            last_name='Singh',
            email='raj.singh@example.com',
            phone='+91-7654321098',
            student_id='STU001003',
            class_name='Class 11',
            roll_number=8,
            address='789 Pine Road, Bangalore',
            city='Bangalore',
            state='Karnataka',
            postal_code='560001',
            is_active=True
        ),
        Student(
            first_name='Anjali',
            last_name='Sharma',
            email='anjali.sharma@example.com',
            phone='+91-6543210987',
            student_id='STU001004',
            class_name='Class 10',
            roll_number=15,
            address='321 Elm Street, Hyderabad',
            city='Hyderabad',
            state='Telangana',
            postal_code='500001',
            is_active=True
        ),
        Student(
            first_name='Vikram',
            last_name='Patel',
            email='vikram.patel@example.com',
            phone='+91-5432109876',
            student_id='STU001005',
            class_name='Class 12',
            roll_number=3,
            address='654 Maple Drive, Pune',
            city='Pune',
            state='Maharashtra',
            postal_code='411001',
            is_active=True
        ),
        Student(
            first_name='Neha',
            last_name='Kumar',
            email='neha.kumar@example.com',
            phone='+91-4321098765',
            student_id='STU001006',
            class_name='Class 9',
            roll_number=7,
            address='987 Cedar Lane, Chennai',
            city='Chennai',
            state='Tamil Nadu',
            postal_code='600001',
            is_active=True
        ),
        Student(
            first_name='Aditya',
            last_name='Reddy',
            email='aditya.reddy@example.com',
            phone='+91-3210987654',
            student_id='STU001007',
            class_name='Class 11',
            roll_number=11,
            address='159 Birch Street, Kolkata',
            city='Kolkata',
            state='West Bengal',
            postal_code='700001',
            is_active=True
        ),
        Student(
            first_name='Sakshi',
            last_name='Verma',
            email='sakshi.verma@example.com',
            phone='+91-2109876543',
            student_id='STU001008',
            class_name='Class 10',
            roll_number=9,
            address='753 Ash Road, Jaipur',
            city='Jaipur',
            state='Rajasthan',
            postal_code='302001',
            is_active=True
        ),
        Student(
            first_name='Rohan',
            last_name='Gupta',
            email='rohan.gupta@example.com',
            phone='+91-1098765432',
            student_id='STU001009',
            class_name='Class 12',
            roll_number=6,
            address='246 Spruce Avenue, Lucknow',
            city='Lucknow',
            state='Uttar Pradesh',
            postal_code='226001',
            is_active=True
        ),
        Student(
            first_name='Divya',
            last_name='Nair',
            email='divya.nair@example.com',
            phone='+91-9098765432',
            student_id='STU001010',
            class_name='Class 9',
            roll_number=14,
            address='864 Willow Drive, Kochi',
            city='Kochi',
            state='Kerala',
            postal_code='682001',
            is_active=True
        ),
    ]
    
    try:
        for student in sample_students:
            db.session.add(student)
        
        db.session.commit()
        print(f"✅ Successfully seeded database with {len(sample_students)} students!")
        
        # Print summary
        total = Student.query.filter_by(is_active=True).count()
        classes = db.session.query(db.func.count(db.func.distinct(Student.class_name))).filter_by(is_active=True).scalar()
        print(f"📊 Database Summary:")
        print(f"   - Total Students: {total}")
        print(f"   - Total Classes: {classes}")
        
    except Exception as e:
        print(f"❌ Error seeding database: {str(e)}")
        db.session.rollback()

if __name__ == '__main__':
    with app.app_context():
        seed_database()
