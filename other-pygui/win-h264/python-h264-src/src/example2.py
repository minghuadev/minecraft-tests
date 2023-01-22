#!/usr/bin/env python
# example2.py
# read h264 from file, zoom out, print k-count and p-count, show

import ffmpeg
import numpy as np
import cv2
import os


# Place the ffmpeg.exe at ../bin/ffmpeg/bin/
###############################################
old_path = os.environ['PATH']
os.environ['PATH'] = old_path + os.pathsep + "../bin/ffmpeg/bin"
###############################################


# Use ffprobe to get video frames resolution
###############################################
g_base_dir = "./sample-video"
g_in_first_file = g_base_dir + "/" + "frame000101.bin"
if not os.path.isfile(g_in_first_file):
    raise RuntimeError(" file not exist ")
###############################################


# Use ffprobe to get video frames resolution
###############################################
g_p = ffmpeg.probe(g_in_first_file, select_streams='v');
g_width = g_p['streams'][0]['width']
g_height = g_p['streams'][0]['height']
n_frames = g_p['streams'][0].get('nb_frames', 1)
###############################################


# Create a generator to read and feed k-p sequence of frames
###############################################
def generate_frames():
    all_done = None
    print("Stage ... read ... ")
    for i in range(0,5): # we have 5 k frames
        idx_i = i + 1 # 1..5
        if all_done: break

        out_bytes = b''
        for j in range(0,30): # k-p sequence consists of 30 frames
            idx_j = j + 1 # 1..30
            if all_done: break

            filename = g_base_dir + "/" + "frame00%02d%02d.bin" % (idx_i, idx_j)
            if os.path.isfile(filename):
                if j == 0:
                    p = ffmpeg.probe(filename, select_streams='v');
                    width = p['streams'][0]['width']
                    height = p['streams'][0]['height']
                    if width != g_width or height != g_height:
                        all_done = True
                        break
                with open(filename, "rb") as in_f:
                    read_bytes = in_f.read()
                    if not read_bytes:
                        all_done = True
                        break
                    out_bytes += read_bytes

            print("  Yield %d %d: len %d" % ( idx_i, idx_j, len(out_bytes)))
            yield out_bytes # yield the frame data of a single frame
            out_bytes = b''

    while True:
        print("  Yield empty")
        yield b''
###############################################


# the test main
###############################################
frame_gen = generate_frames()
fr_k_cnt = 0
while(True):
    fr_k_cnt += 1

    out_bytes = b''
    for i in range(30): # assemble the whole k-p sequence
        read_bytes = next(frame_gen)
        if len(read_bytes) < 1:
            break
        out_bytes += read_bytes
    if len(out_bytes) < 1:
        break

    # FFmpeg in a subprocess, sdtin as input pipe and stdout as output pipe
    process = (
        ffmpeg
            .input('pipe:')
            .video
            .output('pipe:', format='rawvideo', pix_fmt='bgr24')
            .run_async(pipe_stdin=True, pipe_stdout=True)
    )

    # Open In-memory binary streams
    print("Stage ... write ... ")
    process.stdin.write( out_bytes )

    # close so the process will generate result
    print("Stage ... close ... ")
    process.stdin.close()

    fr_p_cnt = 0
    while True:
        fr_p_cnt += 1
        # Read raw video frame from stdout as bytes array.
        in_bytes = process.stdout.read(g_width * g_height * 3)

        if not in_bytes:
            break

        print("State ... show ... ", fr_k_cnt, " ", fr_p_cnt)
        # transform the byte read into a numpy array
        in_frame = (
            np
            .frombuffer(in_bytes, np.uint8)
            .reshape([g_height, g_width, 3])
        )

        # zoom out by half
        if True:
            # pythonexamples.org
            # python-opencv-cv2-resize-image
            in_shape = in_frame.shape[0:2]
            dsz = (int(in_shape[1]/2), int(in_shape[0]/2)) # w, h
            out_frame = cv2.resize(in_frame, dsz)
            in_frame = out_frame

        # put text to the image
        if True:
            # pythonexamples.org
            # python-opencv-write-text-on-image-puttext
            in_shape = in_frame.shape[0:2]
            x_pos = int(in_shape[1]/2 + in_shape[1]/10) # w
            y_pos = int(in_shape[0]/10) # h
            cv2.putText(in_frame,
                        " k-%d p-%d " % (fr_k_cnt, fr_p_cnt),
                        (x_pos, y_pos),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1, # FONT SIZE
                        (209, 80, 0, 255), # font color (209, 80, 0, 255)
                        3 # font stroke
                        )

        #Display the frame
        cv2.imshow('in_frame', in_frame)

        if cv2.waitKey(100) & 0xFF == ord('q'):
            break
        if fr_k_cnt == 1 and fr_p_cnt == 1:
            cv2.waitKey(3000)
    process.wait()

cv2.waitKey(3000)
cv2.destroyAllWindows()
###############################################

