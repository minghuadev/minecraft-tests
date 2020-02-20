#
# bb.dockerfile

FROM centos:7
RUN yum update -y
RUN yum clean all -y 

 ARG UNAME=centloopuser
 ARG UID=9999
 ARG GID=9999
 RUN groupadd -g $GID $UNAME
 RUN useradd -m -u $UID -g $GID -s /bin/bash $UNAME

ADD bb.dockerfile /bb.dockerfile

ADD entrypoint.bash /entrypoint.bash
RUN chmod +x /entrypoint.bash

 USER $UNAME

ENTRYPOINT ["/entrypoint.bash"]

#docker build --build-arg UID=$(id -u) --build-arg GID=$(id -g) \
#       -f bb.dockerfile  -t centloop .

#    mkdir docker_mount
#    docker run -td \
#         -v "$(pwd)/docker_mount":/home/centloopuser/docker_mount \
#         --name centosloop  \
#         centloop

# create or modify /etc/docker/daemon.json
# { "insecure-registries":["myregistry.example.com:5000"] }
#
# docker push myregistry.example.com:5000/centloop:latest

# https://github.com/BradleyA/Search-docker-registry-v2-script.1.0
# curl -ik http://myregistry.example.com:5000/v2/centloop/list
# curl -ik http://myregistry.example.com:5000/v2/centloop/tags/list


