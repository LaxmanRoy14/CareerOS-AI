from flask import Flask
from flask_cors import CORS

from config import Config
from extensions import bcrypt, jwt

from routes.auth import auth_bp

app = Flask(__name__)

CORS(app)

app.config["JWT_SECRET_KEY"] = Config.JWT_SECRET_KEY

bcrypt.init_app(app)
jwt.init_app(app)

app.register_blueprint(auth_bp, url_prefix="/api/auth")


@app.route("/")
def home():
    return {
        "message": "CareerOS AI Backend Running Successfully"
    }


if __name__ == "__main__":
    app.run(debug=True)