import unittest
import stowrap
from dotenv import load_dotenv
import tempfile
from datetime import datetime
import os

load_dotenv()


class TestDownload(unittest.TestCase):
    def upload_test_file(self, service, bucket, filename) -> stowrap.UploadResult:
        with tempfile.TemporaryDirectory() as tempdir:
            testfile = os.path.join(tempdir, "test.txt")
            with open(testfile, "w") as f:
                f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            return stowrap.Client(service).upload(bucket, testfile, filename)

    def test_gcs_download(self):
        result = self.upload_test_file("gcs", os.environ["TEST_GCS_BUCKET"], "test.txt")
        try:
            stowrap.Client("gcs").download(
                os.environ["TEST_GCS_BUCKET"], "test.txt", "test.txt"
            )
        except stowrap.NotServiceAccountException:
            self.skipTest("Not a service account")
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")

    def test_s3_download(self):
        bucket = os.environ["TEST_S3_BUCKET"]
        self.upload_test_file("s3", bucket, "test.txt")
        stowrap.Client("s3").download(bucket, "test.txt", "test.txt")
