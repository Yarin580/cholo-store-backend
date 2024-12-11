import json
import os
from typing import Dict, Any, Union

from fastapi import UploadFile

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



    def upload_file(self, file_path: Union[str, UploadFile], object_path_key: str):

        try:
            if isinstance(file_path, str):  # If it's a local file path
                with open(file_path, "rb") as file:
                    self._s3conn.upload_fileobj(file, self._bucket_name, object_path_key,
                                      ExtraArgs={"ACL": "public-read", "ContentType": "application/octet-stream"})
            else:
                self._s3conn.upload_fileobj(file_path.file, self._bucket_name, object_path_key)
        except Exception as e:
            raise Exception("File could not be uploaded, " + str(e))

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



# conn = (S3Connection(bucket_name="cholo-store", access_key=config.AWS_CREDS.aws_access_key_id, secret_key=config.AWS_CREDS.aws_secret_access_key))