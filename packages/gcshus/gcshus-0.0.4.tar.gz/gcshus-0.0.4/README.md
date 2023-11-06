# gcshus
GCS Helper Utils for Python

## How to use
### Upload a file
```
import gcshus
from google.cloud import storage

gcshus.upload(
    storage.Client(), "my-bucket", "/path/to/src.txt", "dst.txt"
)
```

### Generate a signed url for download
```
import gcshus
from google.cloud import storage

url = gcshus.generate_download_signed_url_with_token_refresh(
    storage.Client(), "my-bucket", "dst.txt", 5
)
```

### Download a file
```
import gcshus
from google.cloud import storage

gcshus.download(storage.Client(), bucket, "some/remote/blob.txt", "local-file.txt")
```

## Run test
```
docker compose up
```
