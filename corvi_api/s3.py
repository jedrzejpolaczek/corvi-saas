import boto3
from .config import settings

session = boto3.session.Session(
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
)
s3 = session.client("s3", endpoint_url=settings.S3_ENDPOINT_URL, use_ssl=settings.S3_SECURE)

def put_object(key: str, data: bytes, content_type: str):
    s3.put_object(Bucket=settings.S3_BUCKET, Key=key, Body=data, ContentType=content_type)
    return f"s3://{settings.S3_BUCKET}/{key}"
