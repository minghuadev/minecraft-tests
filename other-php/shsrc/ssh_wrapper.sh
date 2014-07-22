#!/bin/bash
#ssh_wrapper.sh

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

ssh -F ${OPENSHIFT_DATA_DIR}/dotssh/config $*


#config file contains:
#Host yoursite.com
#        IdentityFile       /var/lib/openshift/932d044655001b/app-root/data/dotssh/id_rsa_opengit
#        UserKnownHostsFile /var/lib/openshift/932d044655001b/app-root/data/dotssh/known_host
#        User yourname

