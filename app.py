from flask import Flask
from adminRegister.admin_blueprint import admin_bp
from clientRegister.client_blueprint import client_bp
from databaseModel.models import db
from databaseModel.loginMgr import login_manager

app = Flask(__name__)
app.config["SECRET_KEY"] = "arunisto"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
login_manager.init_app(app)
db.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(admin_bp)
app.register_blueprint(client_bp)


if __name__ == "__main__":
    app.run(debug=True)