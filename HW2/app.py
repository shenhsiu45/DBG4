from flask import Flask
from create import create_bp
from read import read_bp
from delete import delete_bp
from update import update_bp
from search import search_bp
from join import join_bp

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Register blueprints
app.register_blueprint(create_bp)
app.register_blueprint(read_bp)
app.register_blueprint(delete_bp)
app.register_blueprint(update_bp)
app.register_blueprint(search_bp)
app.register_blueprint(join_bp)

if __name__ == '__main__':
    app.run(debug=True)
