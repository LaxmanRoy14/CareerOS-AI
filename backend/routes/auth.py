from flask import Blueprint, request, jsonify

from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from models.user import User
from extensions import bcrypt
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

@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No input data provided",
            "data": None
        }), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "success": False,
            "message": "Email and password are required",
            "data": None
        }), 400

    user = User.get_user_by_email(email)

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid email or password",
            "data": None
        }), 401

    if not bcrypt.check_password_hash(user["password"], password):
        return jsonify({
            "success": False,
            "message": "Invalid email or password",
            "data": None
        }), 401

    access_token = create_access_token(identity=str(user["id"]))

    return jsonify({
        "success": True,
        "message": "Login successful",
        "data": {
            "access_token": access_token,
            "user": {
                "id": user["id"],
                "full_name": user["full_name"],
                "email": user["email"]
            }
        }
    }), 200

@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.get_user_by_id(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found",
            "data": None
        }), 404

    return jsonify({
        "success": True,
        "message": "Profile fetched successfully",
        "data": user
    }), 200