#
# docs.aws.amazon.com/code-library/latest/ug/python_3_s3_code_examples.html
# check s3 bucket existance

from botocore.exceptions import ClientError
from boto_t01_s3hello import BaseS3BucketResource
import settings
import logging
import time


logging.basicConfig(filename=None, encoding='utf-8', level=logging.INFO)
logger = logging.getLogger(__name__)


class BucketWrapper:
    """Encapsulates S3 bucket actions."""

    def __init__(self, bucket):
        """
        :param bucket: A Boto3 Bucket resource. This is a high-level resource in Boto3
                       that wraps bucket actions in a class-like structure.
        """
        self.bucket = bucket
        self.name = bucket.name


    def exists(self):
        """
        Determine whether the bucket exists and you have access to it.

        :return: True when the bucket exists; otherwise, False.
        """
        try:
            self.bucket.meta.client.head_bucket(Bucket=self.bucket.name)
            logger.info("Bucket %s exists.", self.bucket.name)
            exists = True
        except ClientError:
            logger.warning(
                "Bucket %s doesn't exist or you don't have access to it.",
                self.bucket.name,
            )
            exists = False
        return exists


if __name__ == "__main__":
    tm0 = time.time()
    s3_resource = BaseS3BucketResource().get_s3_resource()
    tm1 = time.time()
    bucket_name = settings.BUCKET_NAME
    bucket = s3_resource.Bucket(bucket_name)
    wrapper = BucketWrapper(bucket)
    result = wrapper.exists()
    tm2 = time.time()
    tdiff1 = tm1 - tm0
    tdiff2 = tm2 - tm1
    print("Time used: %.2f %.2f" % (tdiff1, tdiff2))

