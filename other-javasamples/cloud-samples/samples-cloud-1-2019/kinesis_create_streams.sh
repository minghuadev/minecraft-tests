

# https://docs.aws.amazon.com/streams/latest/dev/get-started-exercise.html

$ cat cmd1

aws2 kinesis create-stream \
--stream-name ExampleInputStream \
--shard-count 1 \
--region us-east-2 \
--profile adminuser


$ cat cmd2

aws2 kinesis create-stream \
--stream-name ExampleOutputStream \
--shard-count 1 \
--region us-east-2 \
--profile adminuser




