from flask import Flask
from auth import auth_bp
from database import init_db
from admin import admin_bp
from member import member_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = "super-secret-key"

app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(member_bp)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
