#!/bin/bash
# ci_auto_daily.sh
# append to log7.txt

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR

export CI_AUTO_TRIGGERED=goodgood
export CI_AUTO_PROJECT=`cat ${OPENSHIFT_DATA_DIR}/dotssh/projname`

  rm -rf ci-trial-project
  git clone https://github.com/${CI_AUTO_PROJECT} ci-trial-project
  cd ci-trial-project/buildco2
  git config user.name openshiftautouser
  git config user.email openshiftautouser@localhost
  bash check-inner >> $DIR/log7.txt 2>&1


