#
# search aws s3 rename object python
# https://medium.com/plusteam/move-and-rename-objects-within-an-s3-bucket-using-boto-3-58b164790b78
# https://stackoverflow.com/questions/34492462/how-to-rename-objects-boto3-s3
#

import time
import boto3
import settings


tm0 = time.time()

#s3_resource = boto3.resource('s3')
s3_session = boto3.Session(
            aws_access_key_id=settings.AWS_SERVER_PUBLIC_KEY,
            aws_secret_access_key=settings.AWS_SERVER_SECRET_KEY,
        )
s3_resource = s3_session.resource("s3")

bucket_name = settings.BUCKET_NAME
bucket = s3_resource.Bucket(bucket_name)
tm1 = time.time()

bucket_ok = False
try:
    bucket.meta.client.head_bucket(Bucket=bucket_name)
    bucket_ok = True
except:
    pass
tm2 = time.time()

if bucket_ok:
    obj_first_name = "demo_folder/xdata-100k_06"

    # Copy object A as object B
    dst1 = obj_first_name + "_copy1"
    dst2 = obj_first_name + "_copy2"
    dst3 = obj_first_name + "_copy2moved"

    # copy to dst1
    dest_obj = s3_resource.Object(bucket_name, dst1)
    dest_obj.copy_from(CopySource=bucket_name + 
                       "/" + obj_first_name)
    tm3 = time.time()

    # copy to dst2
    dest_obj = s3_resource.Object(bucket_name, dst2)
    dest_obj.copy_from(CopySource=bucket_name + 
                       "/" + obj_first_name)
    tm4 = time.time()

    # move dst2 to dst3
    dest_obj = s3_resource.Object(bucket_name, dst3)
    dest_obj.copy_from(CopySource=bucket_name + 
                       "/" + dst2)
    tm5 = time.time()

    # Delete the former object A
    src_obj = s3_resource.Object(bucket_name, dst2)
    src_obj.delete()
    src_obj.wait_until_not_exists()
    tm6 = time.time()

def prt_tm(tm1, tm2, why):
    print("  %.3f" % (tm2 - tm1), why)

prt_tm(tm0, tm1, "init")
prt_tm(tm1, tm2, "bucket ok")
if bucket_ok:
    prt_tm(tm2, tm3, "copy to dst1")
    prt_tm(tm3, tm4, "copy to dst2")
    prt_tm(tm4, tm5, "copy dst2 to dst2copy")
    prt_tm(tm5, tm6, "remove dst2")
    prt_tm(tm0, tm6, "total time")


''' two local runs: 
  0.363 init
  1.484 bucket ok
  0.185 copy to dst1
  0.116 copy to dst2
  0.138 copy dst2 to dst2copy
  0.248 remove dst2
  2.534 total time

  0.321 init
  1.340 bucket ok
  0.166 copy to dst1
  0.131 copy to dst2
  0.144 copy dst2 to dst2copy
  0.258 remove dst2
  2.360 total time
'''

''' two aws lambda runs: 
1.942 init
0.261 bucket ok
0.098 copy to dst1
0.099 copy to dst2
0.116 copy dst2 to dst2copy
0.224 remove dst2
2.741 total time
REPORT RequestId: a123b	Duration: 5686.63 ms	Billed Duration: 5687 ms	Memory Size: 128 MB	Max Memory Used: 87 MB	Init Duration: 77.51 ms

1.402 init
0.162 bucket ok
0.168 copy to dst1
0.068 copy to dst2
0.076 copy dst2 to dst2copy
0.225 remove dst2
2.102 total time
REPORT RequestId: a123b	Duration: 2233.20 ms	Billed Duration: 2234 ms	Memory Size: 128 MB	Max Memory Used: 92 MB

'''

