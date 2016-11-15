# -*- coding: utf-8 -*-
# @Author: djvolz
# @Date:   2016-11-14 17:04:42
# @Last Modified by:   djvolz
# @Last Modified time: 2016-11-15 01:10:24

import chase

client = 'carl.local:7890'
numLEDs = 64


class LightSequence(object):
    # Create based on class name:
    @staticmethod
    def factory(type):
        # return eval(type + "()")
        if type == "chase":
            return chase.Chase(client, numLEDs)
        else:
          return None
        # assert 0, "Bad light sequence creation: " + type
