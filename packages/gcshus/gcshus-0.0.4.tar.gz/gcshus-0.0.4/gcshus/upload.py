def upload(storage_client, bucket_name, source_file_name, destination_blob_name):
    if len(bucket_name) == 0:
        raise Exception("Bucket name is empty")

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
