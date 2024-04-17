import os
from flask import Blueprint, request, jsonify

from repository.data_repository import load_station_metadata, load_flood_events
from service.historical_data_service import HistoricalDataService
from util.data_utilities import sort_flood_event_dates, compile_stations_with_flood_events

historical_data_controller = Blueprint('historical_data_controller', __name__, url_prefix='/data/flood/history')


@historical_data_controller.route('/stations', methods=['POST'])
def match_historical_floods_with_stations():
    global station_metadata_list
    if not request.is_json:
        return jsonify({'message': 'Request body must be JSON'}), 400

    data = request.get_json()
    flood_event_filename = data.get('flood_event_filename')
    stations_base_folder = data.get('stations_base_folder', 'nrfa_stations')
    flood_event_file_path = os.path.join('data', 'recorded_flood_outlines', flood_event_filename)
    if not os.path.exists(flood_event_file_path):
        return jsonify({'message': 'Flood event file does not exist'}), 400

    station_metadata_filepath = os.path.join('data', 'nrfa_stations_metadata', 'all_stations_metadata.json')
    if os.path.exists(station_metadata_filepath):
        station_metadata_list = load_station_metadata(station_metadata_filepath)

    flood_event_data = load_flood_events(flood_event_file_path)

    hds = HistoricalDataService(station_metadata_list, flood_event_data, stations_base_folder)

    hds.process_flood_events_for_stations()

    return jsonify({'message': 'Flood events processed and matched with stations'}), 200


@historical_data_controller.route('/flood-dates/sort', methods=['POST'])
def sort_historical_flood_events():
    base_folder = os.path.join('data', 'nrfa_stations')
    try:
        sort_flood_event_dates(base_folder)
        return jsonify({'message': 'Flood event dates sorted successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@historical_data_controller.route('/flood-dates/list', methods=['POST'])
def compile_stations_list_with_historical_flood_data():
    base_folder = os.path.join('data', 'nrfa_stations')
    output_file = 'data/stations_with_flood_events.txt'
    try:
        compile_stations_with_flood_events(base_folder, output_file)
        return jsonify({'message': 'Station list compiled successfully.'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500