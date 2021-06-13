#!/bin/sh

fps=10
in_fps=$1
if [ ${in_fps} -ge 1 -a ${in_fps} -le 60 ]; then
    fps=${in_fps}
fi

echo ; echo To set fps to $fps ... ; echo

dbus-send --system --print-reply --dest=webcam.dbserver / webcam.dbserver.media.Cmd \
    string:"{ \"table\": \"image_adjustment\", \"key\": { \"id\": 0 }, \"data\": { \"iFPS\": ${fps} }, \"cmd\": \"Update\" }"

