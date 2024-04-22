import logging
import os

import joblib
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from keras.src.preprocessing.sequence import TimeseriesGenerator

from service.s3_storage_service import S3StorageService
from storage.s3_client import S3Client
from tensorflow.keras.models import load_model


class PredictionService:

    def __init__(self):
        self.s3_client = S3Client().get_client()
        self.s3_service = S3StorageService(self.s3_client)

    def predict(self, station_guid):
        # Create a temporary directory to store the model and scaler
        local_path = 'local_model'
        # Ensure local directory exists
        os.makedirs(local_path, exist_ok=True)
        # Generate the input dataframes
        df, df_without_rain = self.generate_input_dataframes(station_guid)
        # Load the scaler
        scaler = self.download_and_load_scaler(station_guid, 'lmax', True, local_path, 'scaler')
        scaler_no_rain = self.download_and_load_scaler(station_guid, 'lmax', False, local_path, 'scaler_no_rain')

        # Normalise the input dataframes
        print("Normalising normal dataframe")
        df_normalised = self.normalise_input_dataframe(df, scaler)
        print("Normalising no rain dataframe")
        df_no_rain_normalised = self.normalise_input_dataframe(df_without_rain, scaler_no_rain)

        # Get the models
        model_lmax_rain, model_lmax_no_rain, model_lmin_rain, model_lmin_no_rain = self.get_all_prediction_models_for_station(
            station_guid, local_path)

        # Make the train generators
        tg_lmax_rain, tg_lmax_no_rain, tg_lmin_rain, tg_lmin_no_rain = self.make_train_generators(station_guid, df,
                                                                                                  df_normalised,
                                                                                                  df_without_rain,
                                                                                                  df_no_rain_normalised)

        # Make the predictions
        prediction_lmax_rain = model_lmax_rain.predict(tg_lmax_rain)
        prediction_lmax_no_rain = model_lmax_no_rain.predict(tg_lmax_no_rain)
        prediction_lmin_rain = model_lmin_rain.predict(tg_lmin_rain)
        prediction_lmin_no_rain = model_lmin_no_rain.predict(tg_lmin_no_rain)\

        print("Predictions made pre-normalisation")
        print(f"Prediction lmax values: {prediction_lmax_rain}")
        print(f"Prediction lmin values: {prediction_lmin_rain}")
        print(f"Prediction lmax no rain values: {prediction_lmax_no_rain}")
        print(f"Prediction lmin no rain values: {prediction_lmin_no_rain}")


        # # Denormalise the predictions
        prediction_lmax_rain = self.denormalize_predictions(prediction_lmax_rain, scaler, df.shape[1],
                                                            [df.columns.get_loc('lmax')]).flatten()
        prediction_lmax_no_rain = self.denormalize_predictions(prediction_lmax_no_rain, scaler_no_rain,
                                                               df_without_rain.shape[1],
                                                               [df_without_rain.columns.get_loc('lmax')]).flatten()
        prediction_lmin_rain = self.denormalize_predictions(prediction_lmin_rain, scaler, df.shape[1],
                                                            [df.columns.get_loc('lmin')]).flatten()
        prediction_lmin_no_rain = self.denormalize_predictions(prediction_lmin_no_rain, scaler_no_rain,
                                                               df_without_rain.shape[1],
                                                               [df_without_rain.columns.get_loc('lmin')]).flatten()

        print("Predictions made")
        print(f"Prediction lmax values: {prediction_lmax_rain}")
        print(f"Prediction lmin values: {prediction_lmin_rain}")
        print(f"Prediction lmax no rain values: {prediction_lmax_no_rain}")
        print(f"Prediction lmin no rain values: {prediction_lmin_no_rain}")

        # Get the dates for the predictions
        dates = pd.date_range(start=datetime.now().date(), periods=len(prediction_lmax_rain), freq='D')

        return self.generate_prediction_response(dates, prediction_lmax_rain, prediction_lmax_no_rain,
                                                 prediction_lmin_rain, prediction_lmin_no_rain)

    def generate_prediction_response(self, dates, prediction_lmax_rain, prediction_lmax_no_rain, prediction_lmin_rain,
                                     prediction_lmin_no_rain):
        max_mean_values = np.mean([prediction_lmax_rain, prediction_lmax_no_rain], axis=0)
        min_mean_values = np.mean([prediction_lmin_rain, prediction_lmin_no_rain], axis=0)
        mean_values = np.mean([max_mean_values, min_mean_values], axis=0)

        max_data = [{'date': date.strftime('%Y-%m-%d'), 'value': value} for date, value in zip(dates, max_mean_values)]
        min_data = [{'date': date.strftime('%Y-%m-%d'), 'value': value} for date, value in zip(dates, min_mean_values)]
        mean_data = [{'date': date.strftime('%Y-%m-%d'), 'value': value} for date, value in zip(dates, mean_values)]

        return {
            'max_predictions': max_data,
            'min_predictions': min_data,
            'mean_predictions': mean_data
        }

    def denormalize_predictions(self, predictions, scaler, n_features, feature_index):
        """
        Denormalizes predictions for a single target feature across multiple time steps.

        Args:
        - predictions (numpy.array): The predicted values to be denormalized. Expected shape (1, n_predictions).
        - scaler (scaler object): The scaler used for the original data normalization.
        - feature_index (int): Index of the target feature in the dataset used to fit the scaler.
        - n_features (int): Total number of features in the dataset used to fit the scaler.

        Returns:
        - numpy.array: Denormalized predictions (1D array of length `n_predictions`).
        """
        # Check if predictions are a single batch, reshape if necessary
        if predictions.ndim > 1:
            predictions = predictions.reshape(-1, 1)

        # Create a dummy array with the correct shape
        dummy_array = np.zeros((len(predictions), n_features))

        # Place the predictions into the appropriate feature column
        dummy_array[:, feature_index] = predictions

        # Inverse transform the data to get denormalized predictions
        denormalized_data = scaler.inverse_transform(dummy_array)

        # Extract the denormalized predictions for the target feature
        denormalized_predictions = denormalized_data[:, feature_index]

        return denormalized_predictions

    def get_all_model_metadata_for_station(self, station_guid):
        # Load the metadata files
        metadata_lmax_rain = self.s3_service.load_json_from_s3(
            f'flood_stations/{station_guid}/models/lmax/1d_LSTM_rainfall/metadata.json')
        metadata_lmax_no_rain = self.s3_service.load_json_from_s3(
            f'flood_stations/{station_guid}/models/lmax/1d_LSTM_no_rainfall/metadata.json')
        metadata_lmin_rain = self.s3_service.load_json_from_s3(
            f'flood_stations/{station_guid}/models/lmin/1d_LSTM_rainfall/metadata.json')
        metadata_lmin_no_rain = self.s3_service.load_json_from_s3(
            f'flood_stations/{station_guid}/models/lmin/1d_LSTM_no_rainfall/metadata.json')

        return metadata_lmax_rain, metadata_lmax_no_rain, metadata_lmin_rain, metadata_lmin_no_rain

    def get_all_prediction_models_for_station(self, station_guid, local_path):
        # Load the models
        model_lmax_rain = self.download_and_load_model(station_guid, 'lmax', True, local_path, 'model_lmax_rain')
        model_lmax_no_rain = self.download_and_load_model(station_guid, 'lmax', False, local_path, 'model_lmax_no_rain')
        model_lmin_rain = self.download_and_load_model(station_guid, 'lmin', True, local_path, 'model_lmin_rain')
        model_lmin_no_rain = self.download_and_load_model(station_guid, 'lmin', False, local_path, 'model_lmin_no_rain')

        return model_lmax_rain, model_lmax_no_rain, model_lmin_rain, model_lmin_no_rain

    def make_train_generators(self, station_guid, df, df_normalised, df_no_rain, df_no_rain_normalised):
        # Get the models metadata
        metadata_lmax_rain, metadata_lmax_no_rain, metadata_lmin_rain, metadata_lmin_no_rain = self.get_all_model_metadata_for_station(
            station_guid)

        # Create the train generators
        target_data_lmax_rain = df_normalised[:, df.columns.get_loc('lmax')]
        target_data_lmax_no_rain = df_no_rain_normalised[:, df_no_rain.columns.get_loc('lmax')]
        target_data_lmin_rain = df_normalised[:, df.columns.get_loc('lmin')]
        target_data_lmin_no_rain = df_no_rain_normalised[:, df_no_rain.columns.get_loc('lmin')]

        tg_lmax_rain = self.create_generator(df_normalised, metadata_lmax_rain['n_input'],
                                             metadata_lmax_rain['batch_size'], target_data_lmax_rain)
        tg_lmax_no_rain = self.create_generator(df_no_rain_normalised, metadata_lmax_no_rain['n_input'],
                                                metadata_lmax_no_rain['batch_size'], target_data_lmax_no_rain)
        tg_lmin_rain = self.create_generator(df_normalised, metadata_lmin_rain['n_input'],
                                             metadata_lmin_rain['batch_size'], target_data_lmin_rain)
        tg_lmin_no_rain = self.create_generator(df_no_rain_normalised, metadata_lmin_no_rain['n_input'],
                                                metadata_lmin_no_rain['batch_size'], target_data_lmin_no_rain)

        return tg_lmax_rain, tg_lmax_no_rain, tg_lmin_rain, tg_lmin_no_rain

    def create_generator(self, normalised_df, lookback, batch_size, target_data):
        # Extracting the feature and target arrays

        # Create the generator
        generator = TimeseriesGenerator(normalised_df, target_data, length=lookback, batch_size=batch_size)
        return generator

    def generate_model_path(self, station_guid, measurement_type, with_rainfall):
        measurement_path = f'models/{measurement_type}/1d_LSTM_rainfall' if with_rainfall else f'models/{measurement_type}/1d_LSTM_no_rainfall'

        model_path = f'flood_stations/{station_guid}/{measurement_path}'
        return model_path

    def get_model_file(self, station_guid, measurement_type, with_rainfall, filename):
        model_path = self.generate_model_path(station_guid, measurement_type, with_rainfall)
        file = self.s3_service.load_file_from_s3(f"{model_path}/{filename}", f"local_model/{filename}")
        return file

    def generate_input_dataframes(self, station_guid):
        urls = self.generate_csv_urls(station_guid)
        df = self.get_and_merge_all_measurements(urls)
        df, df_without_rain = self.split_dataframe(df)

        return df, df_without_rain

    def normalise_input_dataframe(self, df, scaler):
        df = scaler.transform(df.values)
        return df

    def download_and_load_model(self, guid, measurement_type, with_rainfall, local_path, model_filename):
        model_key = self.generate_model_path(guid, measurement_type, with_rainfall)
        model_key = f'{model_key}/model.keras'
        local_model_path = os.path.join(local_path, f'{model_filename}.keras')  # Assuming .keras format for simplicity
        self.s3_service.download_file_from_s3(model_key, local_model_path)  # Download the model file
        model = load_model(local_model_path)  # Load the model
        return model

    def download_and_load_scaler(self, guid, measurement_type, with_rainfall, local_path, scaler_filename):
        scaler_key = self.generate_model_path(guid, measurement_type, with_rainfall)
        scaler_key = f'{scaler_key}/scaler.pkl'
        scaler_path = os.path.join(local_path, f'{scaler_filename}.pkl')
        self.s3_service.download_file_from_s3(scaler_key, scaler_path)  # Download the scaler file
        scaler = joblib.load(scaler_path)  # Load the scaler
        return scaler

    def generate_csv_urls(self, station_guid, measurement_interval="15min"):
        if measurement_interval == "15min":
            filename = "15min_measurements_links.json"
        elif measurement_interval == "1d":
            filename = "1d_measurements_links.json"
        else:
            raise ValueError("Invalid measurement interval. Choose either '15min' or '1d'.")

        return self.s3_service.load_json_from_s3(f"flood_stations/{station_guid}/{filename}")

    def get_and_merge_all_measurements(self, links):
        final_df = None
        for link_item in links:
            print(f"Processing data from {link_item['link']}")
            # Generate the initial dataframe for 12 years of data
            df = self.generate_multi_day_dataframe(link_item['link'])

            # Generate the learning dataframe with aggregated min, max, and mean
            learning_df = self.generate_learning_dataframe(df, link_item['type'][0])

            # Set the index right before the merge
            learning_df.set_index('date', inplace=True)

            # Merge with the final dataframe
            if final_df is None:
                final_df = learning_df
            else:
                final_df = final_df.join(learning_df, how='outer')

        return final_df

    def generate_learning_dataframe(self, input_df, measurement_type):
        # Convert 'date' column to datetime, attempting to parse any recognized format
        input_df['date'] = pd.to_datetime(input_df['date'], errors='coerce')

        # Group by date and aggregate
        aggregated_data = input_df.groupby('date')['value'].agg(['min', 'max', 'mean'])

        # Rename the columns to include the measurement type
        aggregated_data.columns = [f'{measurement_type}{col}' for col in aggregated_data.columns]

        return aggregated_data.reset_index()  # Keep 'date' as a column, not an index

    def generate_multi_day_dataframe(self, url, number_of_days=58):
        try:
            end_date = datetime.now()  # Today's date
            start_date = end_date - timedelta(days=number_of_days)

            # Format dates for the URL
            formatted_end_date = end_date.strftime('%Y-%m-%d')
            formatted_start_date = start_date.strftime('%Y-%m-%d')

            # Construct the download URL
            download_url = f"{url}?min-date={formatted_start_date}&max-date={formatted_end_date}"
            logging.info(f"Downloading data from {download_url}")

            # Load the data into a DataFrame
            df = pd.read_csv(download_url, parse_dates=['dateTime'], low_memory=False, on_bad_lines='skip')
            logging.info("Data loaded successfully")
            return df
        except Exception as e:
            logging.error(f"Failed to download or parse data from {url}: {e}")
            return None

    def split_dataframe(self, df):
        # Return two dataframes - one with and without rainfall columns

        # Create a DataFrame without the last three columns ('rmin', 'rmax', 'rmean')
        if 'rmin' in df.columns and 'rmax' in df.columns and 'rmean' in df.columns:
            df_without_r = df.drop(columns=['rmin', 'rmax', 'rmean'])
            df_without_r = df_without_r.fillna(df_without_r.mean())
        else:
            df_without_r = df

        df = df.fillna(df.mean())

        return df, df_without_r
