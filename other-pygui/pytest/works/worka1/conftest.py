
def pytest_load_initial_conftests(args, early_config, parser):
	print "\n  Inside load_initial_conftests", "\n"

def pytest_configure(config):
	print "\n  Inside config", "\n"

def pytest_ignore_collect(path, config):
	print "\n  Inside ignore_collect", "\n"
	print "\n  Inside ignore_collect path ", path, "\n"
	print "\n  Inside ignore_collect config ", config, "\n"

def pytest_collection_modifyitems(session, config, items):
	print "\n  Inside collection_modifyitems", "\n"
	print "\n  Inside collection_modifyitems session ", session, "\n"
	print "\n  Inside collection_modifyitems config  ", config,  "\n"
	print "\n  Inside collection_modifyitems items   ", items,   "\n"

