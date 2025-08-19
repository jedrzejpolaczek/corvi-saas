import io, os, hashlib
import boto3
from botocore.client import Config as BotoConfig
from app.config import settings

class S3Client:
    def __init__(self):
        self._client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            region_name=settings.S3_REGION,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            config=BotoConfig(s3={"addressing_style": "path"}),
        )
        self.bucket = settings.S3_BUCKET
        self._ensure_bucket()

    def _ensure_bucket(self):
        s3 = self._client
        try:
            s3.head_bucket(Bucket=self.bucket)
        except Exception:
            # Attempt create for MinIO/dev; ignore if race
            try:
                s3.create_bucket(Bucket=self.bucket)
            except Exception:
                pass

    def upload_fileobj(self, fileobj, key: str, content_type: str = "application/octet-stream"):
        fileobj.seek(0)
        self._client.upload_fileobj(
            Fileobj=fileobj, Bucket=self.bucket, Key=key,
            ExtraArgs={"ContentType": content_type}
        )

    def download_to_path(self, key: str, path: str):
        self._client.download_file(Bucket=self.bucket, Key=key, Filename=path)

    @staticmethod
    def sha256_of_fileobj(fileobj) -> str:
        h = hashlib.sha256()
        pos = fileobj.tell()
        fileobj.seek(0)
        for chunk in iter(lambda: fileobj.read(8192), b""):
            h.update(chunk)
        fileobj.seek(pos)
        return h.hexdigest()

s3_client = S3Client()
