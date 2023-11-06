import unittest
import gcshus
from google.cloud import storage
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.


class TestSignedURL(unittest.TestCase):
    def test_generate_download_signed_url(self):
        try:
            url = gcshus.generate_download_signed_url(
                storage.Client(), os.environ["TEST_GCS_BUCKET"], "test.txt", 5
            )
            assert len(url) > 0
        except AttributeError as e:  # Credentials error
            self.skipTest(e)

    def test_generate_download_signed_url_with_token_refresh(self):
        try:
            url = gcshus.generate_download_signed_url_with_token_refresh(
                storage.Client(), os.environ["TEST_GCS_BUCKET"], "test.txt", 5
            )
            assert len(url) > 0
        except gcshus.NotServiceAccountException:
            self.skipTest("Not a service account")


if __name__ == "__main__":
    unittest.main()
