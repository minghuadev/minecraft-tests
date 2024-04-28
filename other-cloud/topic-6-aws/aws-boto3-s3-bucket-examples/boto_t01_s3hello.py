#
# docs.aws.amazon.com/code-library/latest/ug/python_3_s3_code_examples.html
# hello s3 -- list buckets

import boto3
import settings


class BaseS3BucketResource(object):
    def __init__(self) -> None:
        """
        Use the AWS SDK for Python (Boto3) to create an Amazon Simple Storage Service
        (Amazon S3) resource and list the buckets in your account.
        This example uses the default settings specified in your shared credentials
        and config files.
        """
        #s3_resource = boto3.resource("s3")
        self._s3_session = boto3.Session(
            aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY,
            aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY,
        )
        self._s3_resource = self._s3_session.resource("s3")
    
    def get_s3_resource(self):
        return self._s3_resource


def hello_s3():
    s3_resource = BaseS3BucketResource().get_s3_resource()
    print("Hello, Amazon S3! Let's list your buckets:")
    for bucket in s3_resource.buckets.all():
        print(f"\t{bucket.name}")


if __name__ == "__main__":
    hello_s3()

