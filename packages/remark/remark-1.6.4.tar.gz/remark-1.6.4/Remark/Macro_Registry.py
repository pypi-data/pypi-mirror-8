# -*- coding: utf-8 -*-

# Description: Macro registry
# Documentation: data_structures.txt

# Remark 1.6.4
# Copyright (c) 2009 - 2014
# Kalle Rutanen
# Distributed under the MIT license (see license.txt).

_macroMap = dict()

def registerMacro(name, macro):
    '''
    Registers a macro-object by a name.

    See also:
    findMacro()
    '''
    #print "Macro '" + name + "' registered."
    _macroMap[name] = macro

def findMacro(name):
    '''
    Returns a registered macro-object by its name,
    provided such exists (otherwise returns None).
    The search is case-sensitive.

    See also:
    registerMacro()
    '''
    return _macroMap.get(name)

