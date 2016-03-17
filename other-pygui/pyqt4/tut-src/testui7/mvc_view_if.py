#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class Mvc_View_Interface(object):
    __metaclass__=ABCMeta

    @abstractmethod
    def updateNodeData(self, nodekey=None, nodevalue=None):
        pass

    @abstractmethod
    def updateSlotData(self, slotkey=None, slotvalue=None, slotindex=-1):
        pass

