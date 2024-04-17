from flask import Blueprint, jsonify
import repository.station_metadata_repository as smr

station_data_controller = Blueprint('station_data_controller', __name__, url_prefix='/api/v1')


@station_data_controller.route('/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello, this is the station data controller'}), 200


@station_data_controller.route('/stations/<int:station_id>/metadata', methods=['GET'])
def get_station_metadata(station_id):
    repository = smr.StationMetadataRepository()
    metadata = repository.get_station_metadata(station_id)

    if metadata:
        return jsonify(metadata), 200
    else:
        return jsonify({'message': 'Station metadata not found'}), 404


@station_data_controller.route('/stations', methods=['GET'])
def get_stations_list():
    repository = smr.StationMetadataRepository()
    stations_list = repository.get_all_stations_list()

    if stations_list:
        return jsonify(stations_list), 200
    else:
        return jsonify({'message': 'Stations list not found'}), 404
