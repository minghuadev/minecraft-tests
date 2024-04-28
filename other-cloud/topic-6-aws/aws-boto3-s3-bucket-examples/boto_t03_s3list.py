#
# search aws s3 list files in folder
# https://docs.aws.amazon.com/AmazonS3/latest/userguide/example_s3_ListObjects_section.html
# Use ListObjectsV2 with an AWS SDK or command line too
#

from botocore.exceptions import ClientError
from boto3.exceptions import S3UploadFailedError
from boto_t01_s3hello import BaseS3BucketResource
from boto_t02_s3bucket_exist import BucketWrapper
import settings

import time, os

import logging # configured in boto_t02

logger = logging.getLogger(__name__)


class ObjectWrapper:
    """Encapsulates S3 object actions."""

    def __init__(self, s3_object):
        """
        :param s3_object: A Boto3 Object resource. This is a high-level resource in Boto3
                          that wraps object actions in a class-like structure.
        """
        self.object = s3_object
        self.key = self.object.key


    @staticmethod
    def list(bucket, prefix=None):
        """
        Lists the objects in a bucket, optionally filtered by a prefix.

        :param bucket: The bucket to query. This is a Boto3 Bucket resource.
        :param prefix: When specified, only objects that start with this prefix are listed.
        :return: The list of objects.
        """
        try:
            if not prefix:
                objects = list(bucket.objects.all())
            else:
                objects = list(bucket.objects.filter(Prefix=prefix))
            logger.info(
                "Got objects %s from bucket '%s'", [o.key for o in objects], bucket.name
            )
        except ClientError:
            logger.exception("Couldn't get objects for bucket '%s'.", bucket.name)
            raise
        else:
            return objects


if __name__ == "__main__":
    tm0 = time.time()
    s3_resource = BaseS3BucketResource().get_s3_resource()
    tm1 = time.time()
    bucket_name = settings.BUCKET_NAME
    bucket = s3_resource.Bucket(bucket_name)
    wrapper = BucketWrapper(bucket)
    result = wrapper.exists()
    tm2 = time.time()

    file_in_name = "./xdata-100k"

    total_num = 8
    def obj_name(idx, name_in):
        if (idx % 4) in [2, 3]:
            return "demo_folder/" + name_in
        return name_in

    for idx in range(total_num):
        print("")
        o_name = obj_name(idx, os.path.basename(file_in_name + ("_%02d" % idx)))

        print("  idx ", idx, "  oname ", o_name)
        obj = bucket.Object(o_name)
    
    wrapper = ObjectWrapper(obj)
    objs = wrapper.list(bucket, prefix="demo")

    for x in objs:
        print("  list obj key: ", x.key)


