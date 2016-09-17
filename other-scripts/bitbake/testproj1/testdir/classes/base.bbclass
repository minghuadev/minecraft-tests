# Copyright (C) 2003  Chris Larson
#

inherit logging

addtask showdata
do_showdata[nostamp] = "1"
python do_showdata() {
	import sys
	# emit variables and shell functions
	bb.data.emit_env(sys.__stdout__, d, True)
	# emit the metadata which isnt valid shell
	for e in bb.data.keys(d):
		if d.getVarFlag(e, 'python'):
			sys.__stdout__.write("\npython %s () {\n%s}\n" % (e, d.getVar(e, True)))
			bb.warn("python DO_SHOWDATA  %s () {\n%s}\n" % (e, d.getVar(e, True)))
}

addtask listtasks
do_listtasks[nostamp] = "1"
python do_listtasks() {
	bb.warn("python DO_LISTTASKS")
	import sys
	for e in bb.data.keys(d):
		if d.getVarFlag(e, 'task'):
			sys.__stdout__.write("%s\n" % e)
			bb.warn("python DO_LISTTASKS key task %s" % e)
}

addtask build after do_fetch
do_build[dirs] = "${TOPDIR}"
do_build[nostamp] = "1"
python base_do_build () {
	bb.warn("The included, default BB base.bbclass does not define a useful default task.")
	bb.warn("Try running the 'listtasks' task against a .bb to see what tasks are defined.")
}

addtask fetch
do_fetch[dirs] = "${TOPDIR}"
do_fetch[nostamp] = "1"
python base_do_fetch() {
    bb.note("BASE_DO_FETCH")
    bb.warn("BASE_DO_FETCH")
}

EXPORT_FUNCTIONS do_clean do_mrproper do_build do_fetch
