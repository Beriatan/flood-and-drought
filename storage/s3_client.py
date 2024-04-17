import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError


class S3Client:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            try:
                cls._instance = super(S3Client, cls).__new__(cls, *args, **kwargs)
                cls._instance.s3_client = boto3.client('s3')
            except (NoCredentialsError, PartialCredentialsError) as e:
                raise EnvironmentError(f"Error initialising S3 Client: {e}")
        return cls._instance

    def get_client(self):
        return self._instance.s3_client
