from flask import Flask

from flask_cors import CORS

from database import db

from routes.bins import bins_bp
from routes.monitoring import monitoring_bp
from routes.access import access_bp


app = Flask(__name__)

CORS(app)

app.config[
    'SQLALCHEMY_DATABASE_URI'
] = 'sqlite:///./smart_bins.db'

app.config[
    'SQLALCHEMY_TRACK_MODIFICATIONS'
] = False


db.init_app(app)


with app.app_context():

    db.create_all()


app.register_blueprint(
    bins_bp
)

app.register_blueprint(
    monitoring_bp
)

app.register_blueprint(
    access_bp
)


@app.route('/')
def home():

    return {
        'message':
        'Sistema de Lixeira Inteligente Online'
    }


if __name__ == '__main__':

    app.run(debug=True)