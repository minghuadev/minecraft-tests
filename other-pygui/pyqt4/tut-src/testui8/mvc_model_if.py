#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class Mvc_Model_Interface(object):
    __metaclass__=ABCMeta

    @abstractmethod
    def setView(self, uiref=None):
        pass

    @abstractmethod
    def get_node_names(self):
        pass

    @abstractmethod
    def get_slot_names(self):
        pass

    @abstractmethod
    def eval_from_top(self):
        return 0  # return events processed

