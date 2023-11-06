import unittest
import gcshus
from google.cloud import storage
from dotenv import load_dotenv
import os
import tempfile
from datetime import datetime

load_dotenv()  # take environment variables from .env.


class TestUpload(unittest.TestCase):
    def test_upload(self):
        with tempfile.TemporaryDirectory() as tempdir:
            testfile = os.path.join(tempdir, "test.txt")
            with open(testfile, "w") as f:
                print(datetime.now(), file=f)
            gcshus.upload(
                storage.Client(), os.environ["TEST_GCS_BUCKET"], testfile, "test.txt"
            )


if __name__ == "__main__":
    unittest.main()
