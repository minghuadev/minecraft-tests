

from botocore.exceptions import ClientError
from boto3.exceptions import S3UploadFailedError
from boto_t01_s3hello import BaseS3BucketResource
from boto_t02_s3bucket_exist import BucketWrapper
import settings

import time, os, io

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


    def delete(self):
        """
        Deletes the object.
        """
        try:
            self.object.delete()
            self.object.wait_until_not_exists()
            logger.info(
                "Deleted object '%s' from bucket '%s'.",
                self.object.key,
                self.object.bucket_name,
            )
        except ClientError:
            logger.exception(
                "Couldn't delete object '%s' from bucket '%s'.",
                self.object.key,
                self.object.bucket_name,
            )
            raise


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
    while file_in_name is None:
        file_in_name = input("\nEnter a file you want to upload to your bucket: ")
        if not os.path.exists(file_in_name):
            print(f"Couldn't find file {file_in_name}. Are you sure it exists?")
            file_name = None

    total_num = 8
    def obj_name(idx, name_in):
        if (idx % 4) in [2, 3]:
            return "demo_folder/" + name_in
        return name_in

    for idx in range(total_num):
        o_name = obj_name(idx, os.path.basename(file_in_name + ("_%02d" % idx)))
        obj = bucket.Object(o_name)
        try:
            obj.upload_file(file_in_name)
            print(
                f"Uploaded file {file_in_name} idx {idx} into bucket {bucket.name} with key {obj.key}."
            )
        except S3UploadFailedError as err:
            print(f"Couldn't upload file {file_in_name} idx {idx} to bucket {bucket.name}.")
            print(f"\t{err}")
    tm3 = time.time()

    for idx in range(total_num):
        o_name = obj_name(idx, os.path.basename(file_in_name + ("_%02d" % idx)))
        obj = bucket.Object(o_name)

        data = io.BytesIO()
        try:
            obj.download_fileobj(data)
            data.seek(0)
            print(f"Got your object. Here are the first 20 bytes:\n")
            print(f"\t{data.read(20)}")
        except ClientError as err:
            print(f"Couldn't download {obj.key}.")
            print(
                f"\t{err.response['Error']['Code']}:{err.response['Error']['Message']}"
            )
    tm4 = time.time()

    for idx in range(total_num):
        if (idx %2 ) == 0:
            continue
        o_name = obj_name(idx, os.path.basename(file_in_name + ("_%02d" % idx)))
        obj = bucket.Object(o_name)

        wrapper = ObjectWrapper(obj)
        wrapper.delete()
    tm5 = time.time()

    tdiff1 = tm1 - tm0
    tdiff2 = tm2 - tm1
    tdiff3 = tm3 - tm2
    tdiff4 = tm4 - tm3
    tdiff5 = tm5 - tm4
    print("Time used: %.2f %.2f %.2f %.2f %.2f" % (tdiff1, tdiff2, tdiff3, tdiff4, tdiff5))

