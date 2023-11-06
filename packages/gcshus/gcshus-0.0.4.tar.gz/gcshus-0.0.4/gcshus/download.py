def download(storage_client, bucket_name, remote_blob_name, local_file_name):
    if len(bucket_name) == 0:
        raise Exception("Bucket name is empty")

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(remote_blob_name)
    blob.download_to_filename(local_file_name)
