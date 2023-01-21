

# same stackoverflow link:
#
# To work with the larger video, we need to replace process.stdin.write
# the process.communicate. Updating the following lines

...
# process.stdin.write(stream.getvalue())  # Write stream content to the pipe
outs, errs = process.communicate(input=stream.getvalue())
# process.stdin.close()  # close stdin (flush and send EOF)
# Read decoded video (frame by frame), and display each frame (using cv2.imshow)

position = 0
ct = time.time()
while(True):
    # Read raw video frame from stdout as bytes array.
    in_bytes = outs[position: position + width * height * 3]
    position += width * height * 3
...



