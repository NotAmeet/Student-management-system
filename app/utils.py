from functools import wraps
from flask import flash, redirect, url_for
from app import db

def commit_to_db(func):
    """Decorator to commit changes to database"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            raise e
    return wrapper

def get_or_404(model, id):
    """Get an object or return 404"""
    from flask import abort
    return model.query.get_or_404(id)

def flash_errors(form):
    """Flash form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{field}: {error}', 'danger')

def calculate_letter_grade(score):
    """Calculate letter grade from score"""
    if score >= 90:
        return 'A'
    elif score >= 80:
        return 'B'
    elif score >= 70:
        return 'C'
    elif score >= 60:
        return 'D'
    else:
        return 'F'

def paginate_query(query, page, per_page=10):
    """Paginate a query"""
    return query.paginate(page=page, per_page=per_page, error_out=False)
