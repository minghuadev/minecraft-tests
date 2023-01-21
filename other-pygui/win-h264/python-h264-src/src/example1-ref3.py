#!/usr/bin/evn python
# the full code, original.

# search python decode h264
# stackoverflow.com/questions/59998641/
# decode-and-show-h-264-chucked-video-sequence-with-python-from-pi-camera

# the full code
# For testing the solution, I created a sample video file, and read it into
# memory buffer (encoded as H.264).
# I used the memory buffer as input to the above code (replacing your stream).

import ffmpeg
import numpy as np
import cv2
import io

in_filename = 'in.avi'

# Build synthetic video, for testing begins:
###############################################
# ffmpeg -y -r 10 -f lavfi -i testsrc=size=160x120:rate=1 -c:v libx264 -t 5 in.mp4
width, height = 160, 120

(
    ffmpeg
    .input('testsrc=size={}x{}:rate=1'.format(width, height), r=10, f='lavfi')
    .output(in_filename, vcodec='libx264', crf=23, t=5)
    .overwrite_output()
    .run()
)
###############################################


# Use ffprobe to get video frames resolution
###############################################
p = ffmpeg.probe(in_filename, select_streams='v');
width = p['streams'][0]['width']
height = p['streams'][0]['height']
n_frames = int(p['streams'][0]['nb_frames'])
###############################################


# Stream the entire video as one large array of bytes
###############################################
# https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md
in_bytes, _ = (
    ffmpeg
    .input(in_filename)
    .video # Video only (no audio).
    .output('pipe:', format='h264', crf=23)
    .run(capture_stdout=True) # Run asynchronous, and stream to stdout
)
###############################################


# Open In-memory binary streams
stream = io.BytesIO(in_bytes)

# Execute FFmpeg in a subprocess with sdtin as input pipe and stdout as output pipe
# The input is going to be the video stream (memory buffer)
# The ouptut format is raw video frames in BGR pixel format.
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
