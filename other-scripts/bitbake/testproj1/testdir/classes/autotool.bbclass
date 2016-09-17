
autotool_do_fetch() {
    bbnote "AUTOTOOLS_CONFIGURE"
    bbwarn "AUTOTOOLS_CONFIGURE"
}

autotool_do_unpack() {
    bbnote "AUTOTOOLS_MAKE"
    bbwarn "AUTOTOOLS_MAKE"
}

EXPORT_FUNCTIONS do_fetch do_unpack

