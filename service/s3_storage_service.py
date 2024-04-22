import json
import os

from botocore.exceptions import ClientError


class S3StorageService:
    def __init__(self, s3_client):
        self.bucket_name = os.getenv("BUCKET_NAME")
        self.s3_client = s3_client

    def save_json_to_s3(self, key, data):
        """Save data to S3 bucket under the specified key"""
        try:
            self.s3_client.put_object(Bucket=self.bucket_name, Key=key, Body=json.dumps(data, indent=5))
        except ClientError as e:
            raise EnvironmentError(f"Error saving data to {key} in S3 {self.bucket_name}, error: {e}")

    def load_json_from_s3(self, key):
        """Load data from S3 bucket under the specified key"""
        try:
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            data = json.loads(response['Body'].read())
            return data
        except ClientError as e:
            raise EnvironmentError(f"Error loading data from {key} in S3 {self.bucket_name}, error: {e}")
        except json.JSONDecodeError as e:
            raise EnvironmentError(f"Error decoding JSON from {key} in S3 {self.bucket_name}, error: {e}")

    def save_file_to_s3(self, key, file_path):
        """Save file to S3 bucket under the specified key"""
        try:
            self.s3_client.upload_file(file_path, self.bucket_name, key)
        except ClientError as e:
            raise EnvironmentError(f"Error saving file to {key} in S3 {self.bucket_name}, error: {e}")

    def load_file_from_s3(self, key, file_path):
        """Load file from S3 bucket under the specified key"""
        try:
            self.s3_client.download_file(self.bucket_name, key, file_path)
        except ClientError as e:
            raise EnvironmentError(f"Error loading file from {key} in S3 {self.bucket_name}, error: {e}")

    def list_files_in_s3(self, prefix):
        """List files in S3 bucket under the specified prefix"""
        try:
            response = self.s3_client.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            files = [content['Key'] for content in response['Contents']]
            return files
        except ClientError as e:
            raise EnvironmentError(f"Error listing files in S3 {self.bucket_name} under {prefix}, error: {e}")

    def delete_file_from_s3(self, key):
        """Delete file from S3 bucket under the specified key"""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=key)
        except ClientError as e:
            raise EnvironmentError(f"Error deleting file from {key} in S3 {self.bucket_name}, error: {e}")

    def delete_files_from_s3(self, prefix):
        """Delete files from S3 bucket under the specified prefix"""
        try:
            files = self.list_files_in_s3(prefix)
            for file in files:
                self.delete_file_from_s3(file)
        except ClientError as e:
            raise EnvironmentError(f"Error deleting files from S3 {self.bucket_name} under {prefix}, error: {e}")

    def list_buckets(self):
        """List all buckets in S3"""
        try:
            response = self.s3_client.list_buckets()
            buckets = [bucket['Name'] for bucket in response['Buckets']]
            return buckets
        except ClientError as e:
            raise EnvironmentError(f"Error listing buckets in S3, error: {e}")

    def download_file_from_s3(self, key, local_path):
        """Download a single file from S3 to the local path."""
        self.s3_client.download_file(self.bucket_name, key, local_path)

    def download_directory_from_s3(self, prefix, local_dir):
        """Download an entire directory from S3 to a local directory."""
        os.makedirs(local_dir, exist_ok=True)
        paginator = self.s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=self.bucket_name, Prefix=prefix):
            for obj in page.get('Contents', []):
                key = obj['Key']
                local_file_path = os.path.join(local_dir, key[len(prefix):])
                self.s3_client.download_file(self.bucket_name, key, local_file_path)
