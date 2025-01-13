from flask import Flask
from models import db
from routes import routes_bp
from admin import admin_bp
from extensions import bcrypt  # Import bcrypt from extensions

app = Flask(__name__)
bcrypt.init_app(app)  # Initialize Bcrypt with app

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:pessword@127.0.0.1:3306/procurement_logistics_management'
app.config['SECRET_KEY'] = "random string"

db.init_app(app)
app.register_blueprint(admin_bp)
app.register_blueprint(routes_bp)

if __name__ == '__main__':
    app.run(debug=True)
