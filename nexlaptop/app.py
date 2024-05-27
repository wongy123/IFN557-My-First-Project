from flask import Flask
from models import db
from views.main import main_bp
from views.admin import admin_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///nexlaptop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secret_key'

db.init_app(app)

# Register blueprints
app.register_blueprint(main_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')

# Custom filters
@app.template_filter('format_storage')
def format_storage(storage):
    if storage >= 1000:
        return f"{storage // 1000}TB"
    else:
        return f"{storage}GB"

@app.template_filter('format_screensize')
def format_screensize(screensize):
    if screensize % 1 == 0:
        return f"{int(screensize)}"
    else:
        return f"{screensize}"

if __name__ == "__main__":
    app.run(debug=False)
