import os
import logging
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from flask import Flask, send_from_directory
from flask_cors import CORS

from controller.historical_data_controller import historical_data_controller
from controller.nrfa_controller import nrfa_controller
from controller.station_data_controller import station_data_controller
from service.s3_storage_service import S3StorageService
from storage.s3_client import S3Client
from service.nrfa_data_service import NRFADataService

app = Flask(__name__, static_folder='./frontend/build', static_url_path='/')
load_dotenv()  # take environment variables from .env.

# Apply CORS to all routes
CORS(app)
CORS(historical_data_controller)
CORS(nrfa_controller)
CORS(station_data_controller)

# Register Blueprints
app.register_blueprint(nrfa_controller)
app.register_blueprint(historical_data_controller)
app.register_blueprint(station_data_controller)

# Setup S3 services
s3_client_instance = S3Client().get_client()
s3_service = S3StorageService(s3_client_instance)

with app.app_context():
    # Dependency injection for all application services
    app.config['s3_service'] = s3_service
    app.config['nrfa_service'] = NRFADataService(s3_service)


def configure_logging():
    if not os.path.exists('app/logs'):
        os.makedirs('app/logs')
    file_handler = RotatingFileHandler('app/logs/flought-backend.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Flought app startup')


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        app.logger.info(f"Path: {path}, not running REACT app...")
        return send_from_directory(app.static_folder, path)
    else:
        app.logger.info(f"Path: {path}, running REACT app...")
        return send_from_directory(app.static_folder, 'index.html')


@app.route('/test')
def test():
    return 'Test route is working'


if __name__ == '__main__':
    configure_logging()
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True, use_reloader=True, passthrough_errors=True)
