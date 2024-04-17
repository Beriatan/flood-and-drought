from flask import current_app
from flask import request, jsonify, Blueprint

nrfa_controller = Blueprint('nrfa_controller', __name__, url_prefix='/data/external/nrfa')


@nrfa_controller.route('/stations', methods=['POST'])
def download_all_stations():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    data = request.get_json()
    station_ids = data.get('station_ids', None)
    data_folder = data.get('data_folder', 'nrfa_stations')
    data_types = data.get('data_types', None)

    current_app.config['nrfa_service'].download_all_stations_data(data_folder=data_folder, data_types=data_types,
                                                                  station_ids=station_ids)

    return jsonify({'message': 'All stations downloaded'}), 200


@nrfa_controller.route('/stations/id/all', methods=['POST'])
def fetch_and_save_station_ids():
    ns = current_app.config['nrfa_service']
    ns.fetch_and_save_station_ids()
    return jsonify({'message': 'Station IDs fetched and saved'}), 200


@nrfa_controller.route('/stations/metadata', methods=['POST'])
def download_stations_metadata():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    data = request.get_json()
    station_ids = data.get('station_ids', None)
    data_folder = data.get('data_folder', 'nrfa_stations_metadata')
    data_fields = data.get('data_fields', None)

    # data_folder_location = os.path.join('data', data_folder)
    ns = current_app.config['nrfa_service']
    if station_ids is None:
        ns.download_all_stations_metadata(data_folder=data_folder, fields=data_fields)
    else:
        ns.download_station_metadata(data_folder=data_folder, station_ids=station_ids, fields=data_fields)

    return jsonify({'message': 'All stations metadata downloaded'}), 200


@nrfa_controller.route('/stations/metadata/detailed', methods=['POST'])
def download_detailed_stations_metadata():
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    data = request.get_json()
    station_ids = data.get('station_ids', None)  # List of station IDs or None to fetch for all
    base_folder = data.get('base_folder', 'nrfa_stations')

    ns = current_app.config['nrfa_service']

    if station_ids:
        # Download detailed metadata for specified station IDs
        for station_id in station_ids:
            ns.fetch_and_save_detailed_station_metadata(station_id, base_folder)
    else:
        # Fetch station IDs from the API if not provided and download detailed metadata for all
        all_station_ids = ns.fetch_station_ids()
        for station_id in all_station_ids:
            ns.fetch_and_save_detailed_station_metadata(station_id, base_folder)

    return jsonify({'message': 'Detailed metadata downloaded for stations'}), 200
