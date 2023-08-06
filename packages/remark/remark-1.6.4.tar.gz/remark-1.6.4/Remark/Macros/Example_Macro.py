# -*- coding: utf-8 -*-

# Description: Example macro

# Remark 1.6.4
# Copyright (c) 2009 - 2014
# Kalle Rutanen
# Distributed under the MIT license (see license.txt).

from Remark.Macro_Registry import registerMacro

class Example_Macro(object):
    def name(self):
        return 'Example'

    def expand(self, parameter, remark):
        text = []
        
        text.append('')
        text.append('This')
        text.append('')
        text.append('[[Verbatim]]:')
        for line in parameter:
            text.append('\t' + line)
        text.append('produces this')
        text.append('')
        text += parameter
        text.append('')

        return text

    def outputType(self):
        return 'remark'

    def expandOutput(self):
        return True

    def htmlHead(self, remark):
        return []                

    def postConversion(self, remark):
        None

registerMacro('Example', Example_Macro())
