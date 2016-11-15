# -*- coding: utf-8 -*-
# @Author: djvolz
# @Date:   2016-11-14 17:04:42
# @Last Modified by:   djvolz
# @Last Modified time: 2016-11-14 17:31:13

import chase

client = 'carl.local:7890'
numLEDs = 64


class LightSequence(object):
    # Create based on class name:
    def factory(type):
        # return eval(type + "()")
        if type == "Chase":
            return chase.Chase(client, numLEDs)
        assert 0, "Bad light sequence creation: " + type
    factory = staticmethod(factory)
