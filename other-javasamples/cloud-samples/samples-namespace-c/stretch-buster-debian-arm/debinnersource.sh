#!/bin/bash
# container_inner_source.sh -- bash script running inside the container
# source this script by the pid 1 bash to start systemd

exec /lib/systemd/systemd --system --unit=multi-user.target

