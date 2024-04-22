class StationMetadataService:
    def __init__(self, station_metadata_repository):
        self.station_metadata_repository = station_metadata_repository

    def get_station_metadata(self, station_id):
        raw_metadata = self.station_metadata_repository.get_station_metadata(station_id)[0]

        if raw_metadata:
            return self._parse_station_metadata(raw_metadata)
        else:
            return None

    def _parse_station_metadata(self, raw_metadata):
        return {
            'guid': raw_metadata.get('stationGuid'),
            'riverName': raw_metadata.get('riverName'),
            'label': raw_metadata.get('label'),
            'dateOpened': raw_metadata.get('dateOpened'),
            'eaLink': raw_metadata.get('@id'),
            'referenceId': raw_metadata.get('stationReference'),
            'lat': raw_metadata.get('lat'),
            'long': raw_metadata.get('long'),
            'town': raw_metadata.get('town'),
            'catchmentName': raw_metadata.get('catchmentName')
        }

    def get_station_stage(self, station_id):
        raw_stage  = self.station_metadata_repository.get_station_stage(station_id)

        if raw_stage:
            return self._parse_station_stage(raw_stage)
        else:
            return None

    def _parse_station_stage(self, raw_stage):
        return {
            'guid': raw_stage.get('stationGuid'),
            'typicalRangeHigh': raw_stage.get('typicalRangeHigh'),
            'typicalRangeLow': raw_stage.get('typicalRangeLow')
        }



