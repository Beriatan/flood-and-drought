from flask import Blueprint, jsonify, current_app
import repository.station_metadata_repository as smr
import service.staton_metadata_service as sms

station_data_controller = Blueprint('station_data_controller', __name__, url_prefix='/api/v1')


@station_data_controller.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, this is the station data controller'}), 200


@station_data_controller.route('/stations/<string:guid>/metadata', methods=['GET'])
def get_station_metadata(guid):
    # Access the service via the application's context if it's set globally or create a new instance
    station_metadata_service = current_app.config.get('station_metadata_service') or sms.StationMetadataService(
        smr.StationMetadataRepository())

    # Fetch metadata using the service
    try:
        metadata = station_metadata_service.get_station_metadata(guid)
        if metadata:
            return jsonify(metadata), 200
        else:
            return jsonify({'message': 'Station metadata not found'}), 404
    except Exception as e:
        # Logging the exception can be helpful for debugging
        current_app.logger.error(f"Failed to retrieve station metadata for GUID {guid}: {str(e)}")
        return jsonify({'message': 'Error retrieving station metadata', 'error': str(e)}), 500


@station_data_controller.route('/stations/<string:guid>/stage', methods=['GET'])
def get_river_stage(guid):
    # Access the service via the application's context if it's set globally or create a new instance
    station_metadata_service = current_app.config.get('station_metadata_service') or sms.StationMetadataService(
        smr.StationMetadataRepository())

    # Fetch metadata using the service
    try:
        metadata = station_metadata_service.get_station_stage(guid)
        if metadata:
            return jsonify(metadata), 200
        else:
            return jsonify({'message': 'Station metadata not found'}), 404
    except Exception as e:
        # Logging the exception can be helpful for debugging
        current_app.logger.error(f"Failed to retrieve station metadata for GUID {guid}: {str(e)}")
        return jsonify({'message': 'Error retrieving station metadata', 'error': str(e)}), 500


@station_data_controller.route('/stations', methods=['GET'])
def get_stations_list():
    repository = smr.StationMetadataRepository()
    stations_list = repository.get_all_stations_locations()

    if stations_list:
        return jsonify(stations_list), 200
    else:
        return jsonify({'message': 'Stations list not found'}), 404


@station_data_controller.route('/stations/<string:guid>/predictions', methods=['POST'])
def predict(guid):
    prediction_service = current_app.config.get('prediction_service')
    if prediction_service:
        try:
            predictions = prediction_service.predict(guid)
            return jsonify(predictions), 200
        except Exception as e:
            current_app.logger.error(f"Failed to predict for station GUID {guid}: {str(e)}")
            return jsonify({'message': 'Error predicting for station', 'error': str(e)}), 500
    else:
        return jsonify({'message': 'Predictions not implemented yet'}), 501