from flask import Blueprint, request, jsonify
from datetime import datetime

from app import db
from app.models import Student

api_bp = Blueprint("api", __name__)


# GET all students
@api_bp.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])


# GET one student
@api_bp.route("/students/<int:id>", methods=["GET"])
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(student.to_dict())


# POST create student
@api_bp.route("/students", methods=["POST"])
def create_student():
    data = request.get_json()

    student = Student(
        first_name=data["first_name"],
        last_name=data["last_name"],
        email=data["email"],
        enrollment_number=data["enrollment_number"],
        phone=data.get("phone"),
        date_of_birth=datetime.strptime(
            data["date_of_birth"], "%Y-%m-%d"
        ).date() if data.get("date_of_birth") else None,
        address=data.get("address")
    )

    db.session.add(student)
    db.session.commit()

    return jsonify({
        "message": "Student created successfully",
        "student": student.to_dict()
    }), 201


# PUT update student
@api_bp.route("/students/<int:id>", methods=["PUT"])
def update_student(id):

    student = Student.query.get_or_404(id)
    data = request.get_json()

    student.first_name = data.get("first_name", student.first_name)
    student.last_name = data.get("last_name", student.last_name)
    student.email = data.get("email", student.email)
    student.enrollment_number = data.get(
        "enrollment_number",
        student.enrollment_number
    )
    student.phone = data.get("phone", student.phone)

    if data.get("date_of_birth"):
        student.date_of_birth = datetime.strptime(
            data["date_of_birth"],
            "%Y-%m-%d"
        ).date()

    student.address = data.get("address", student.address)

    db.session.commit()

    return jsonify({
        "message": "Student updated successfully",
        "student": student.to_dict()
    })


# DELETE student
@api_bp.route("/students/<int:id>", methods=["DELETE"])
def delete_student(id):

    student = Student.query.get_or_404(id)

    db.session.delete(student)
    db.session.commit()

    return jsonify({
        "message": "Student deleted successfully"
    })