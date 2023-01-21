#!/usr/bin/evn python

# search
# stackoverflow.com/questions/59998641/
# decode-and-show-h-264-chucked-video-sequence-with-python-from-pi-camera

# Assumptions:
#
#     stream holds the entire captured h264 stream in memory buffer.
#     You don't want to write the stream into a file.
#
# The solution applies the following:
#
#     Execute FFmpeg in a sub-process with sdtin as input pipe and stdout as output pipe.
#     The input is going to be the video stream (memory buffer).
#     The output format is raw video frames in BGR pixel format.
#     Write stream content to the pipe (to stdin).
#     Read decoded video (frame by frame), and display each frame (using cv2.imshow)

# Note: I used sdtin and stdout as pipes (instead of using named-pipes), because I wanted
# the code to work in Windows too.

import ffmpeg
import numpy as np
import cv2
import io

width, height = 640, 480


# Seek to stream beginning
stream.seek(0)

# Execute FFmpeg in a subprocess with sdtin as input pipe and stdout as output pipe
# The input is going to be the video stream (memory buffer)
# The output format is raw video frames in BGR pixel format.
# https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md
# https://github.com/kkroening/ffmpeg-python/issues/156
# http://zulko.github.io/blog/2013/09/27/read-and-write-video-frames-in-python-using-ffmpeg/
process = (
    ffmpeg
    .input('pipe:')
    .video
    .output('pipe:', format='rawvideo', pix_fmt='bgr24')
    .run_async(pipe_stdin=True, pipe_stdout=True)
)


# https://stackoverflow.com/questions/20321116/can-i-pipe-a-io-bytesio-stream-to-subprocess-popen-in-python
# https://gist.github.com/waylan/2353749
process.stdin.write(stream.getvalue())  # Write stream content to the pipe
process.stdin.close()  # close stdin (flush and send EOF)


#Read decoded video (frame by frame), and display each frame (using cv2.imshow)
while(True):
    # Read raw video frame from stdout as bytes array.
    in_bytes = process.stdout.read(width * height * 3)

    if not in_bytes:
        break

    # transform the byte read into a numpy array
    in_frame = (
        np
        .frombuffer(in_bytes, np.uint8)
        .reshape([height, width, 3])
    )

    #Display the frame
    cv2.imshow('in_frame', in_frame)

    if cv2.waitKey(100) & 0xFF == ord('q'):
        break

process.wait()
cv2.destroyAllWindows()

