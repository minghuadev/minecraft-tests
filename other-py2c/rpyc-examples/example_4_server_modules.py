#!/usr/bin/env python

import time

class Example4ServerModules(object):

    persistent_name = "Example4ServerModules-persistent_name"
    persistent_instances = []

    def __init__(self, name=None):
        self._obj_name = name
    def get_names(self):
        return __class__.persistent_name + "/" + \
               self._obj_name + "/" + repr(__class__.persistent_instances)
    def append_instance(self, inst_name):
        __class__.persistent_instances.append(inst_name)

instance_one = Example4ServerModules( name="obj_at_%.3f" % time.time() )

