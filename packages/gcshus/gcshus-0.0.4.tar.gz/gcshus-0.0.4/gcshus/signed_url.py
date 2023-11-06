import datetime
import google.auth
from google.auth.transport import requests


class NotServiceAccountException(Exception):
    "Raised when the credentials has no service_account_email attribute"
    pass


def generate_download_signed_url_with_token_refresh(
    storage_client, bucket_name, blob_name, expiration_mins
):
    credentials, _ = google.auth.default(
        scopes=[
            "https://www.googleapis.com/auth/devstorage.read_only",
            "https://www.googleapis.com/auth/iam",
        ]
    )
    credentials.refresh(requests.Request())

    if hasattr(credentials, "service_account_email"):
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)

        return blob.generate_signed_url(
            version="v4",
            expiration=datetime.timedelta(minutes=expiration_mins),
            method="GET",
            service_account_email=credentials.service_account_email,
            access_token=credentials.token,
        )
    else:
        raise NotServiceAccountException


def generate_download_signed_url(
    storage_client, bucket_name, blob_name, expiration_mins
):
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    return blob.generate_signed_url(
        version="v4",
        expiration=datetime.timedelta(minutes=expiration_mins),
        method="GET",
    )
