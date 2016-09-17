# Copyright (C) 2003  Chris Larson
#    derived from base.bbclass

die() {
	bbfatal "$*"
}

bbnote() {
	echo "NOTEs:" "$*"
}

bbwarn() {
	echo "WARNINGs:" "$*"
}

bbfatal() {
	echo "FATALs:" "$*"
	exit 1
}

