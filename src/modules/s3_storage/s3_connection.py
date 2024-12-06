import json
from typing import Dict, Any

from config_section.config import config
import boto3
import botocore.exceptions as botocore_exceptions

class S3Connection:
    def __init__(self, bucket_name: str, access_key: str, secret_key: str):
        self._bucket_name = bucket_name
        self._s3conn = boto3.client('s3',
                                    aws_access_key_id=access_key,
                                    aws_secret_access_key=secret_key,
                                    region_name='eu-north-1')


    def generate_url(self, object_key: str) -> dict[str, Any] | dict[str, str]:
        try:
            # Generate a signed URL for the S3 object
            signed_url = self._s3conn.generate_presigned_url(
                'get_object',
                Params={'Bucket': self._bucket_name, 'Key': object_key},
                ExpiresIn=3600  # The URL will be valid for 1 hour
            )
            return {"url": signed_url}
        except botocore_exceptions.NoCredentialsError:
            return {"error": "Credentials not available"}
    def list_all_files(self):
        s3_files = self._s3conn.list_objects(Bucket=self._bucket_name)['Contents']
        return s3_files