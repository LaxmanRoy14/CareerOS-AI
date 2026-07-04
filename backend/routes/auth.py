from flask import Blueprint, request, jsonify

from extensions import bcrypt

from models.user import User

import re

auth_bp = Blueprint("auth", __name__)



@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")

    # Validation
    if not full_name or not email or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required"
        }), 400

    email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

    if not re.match(email_pattern, email):
        return jsonify({
            "success": False,
            "message": "Invalid email format"
        }), 400
    
    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must be at least 8 characters"
        }), 400

    # Check existing user
    existing_user = User.get_user_by_email(email)

    if existing_user:
        return jsonify({
            "success": False,
            "message": "Email already exists"
        }), 409

    # Hash password
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    # Save user
    User.create_user(
        full_name,
        email,
        hashed_password
    )

    return jsonify({
        "success": True,
        "message": "User registered successfully"
    }), 201