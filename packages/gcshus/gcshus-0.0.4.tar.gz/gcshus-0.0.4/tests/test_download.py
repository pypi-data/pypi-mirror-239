import unittest
import gcshus
from google.cloud import storage
from dotenv import load_dotenv
import os
import tempfile
from datetime import datetime

load_dotenv()  # take environment variables from .env.


class TestUpload(unittest.TestCase):
    def test_download(self):
        with tempfile.TemporaryDirectory() as tempdir:
            bucket = os.environ["TEST_GCS_BUCKET"]
            current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # upload file
            testfile = os.path.join(tempdir, "test.txt")
            with open(testfile, "w") as f:
                print(current_datetime, file=f)
            gcshus.upload(storage.Client(), bucket, testfile, "test.txt")

            # download file
            downloadedfile = os.path.join(tempdir, "downloaded.txt")
            gcshus.download(storage.Client(), bucket, "test.txt", downloadedfile)

            # check if file is downloaded
            with open(downloadedfile, "r") as f:
                self.assertEqual(current_datetime, f.read().strip())


if __name__ == "__main__":
    unittest.main()
