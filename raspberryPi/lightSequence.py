# -*- coding: utf-8 -*-
# @Author: djvolz
# @Date:   2016-11-14 17:04:42
# @Last Modified by:   djvolz
# @Last Modified time: 2016-11-15 21:31:19

import time
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
        elif type == "christmas":
            while True:
                time.sleep(1)
                print("christmas")
            return "christmas"
        else:
            return None
        # assert 0, "Bad light sequence creation: " + type
