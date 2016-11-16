# -*- coding: utf-8 -*-
# @Author: djvolz
# @Date:   2016-11-14 17:15:36
# @Last Modified by:   djvolz
# @Last Modified time: 2016-11-15 20:52:37

# Light each LED in sequence, and repeat.

import opc
import time


class Chase():
    def __init__(self, client, numLEDs=64):
        self._numLEDs = numLEDs
        self._client = opc.Client(client)

    def run(self):
        while True:
            for i in range(self._numLEDs):
                pixels = [(0, 0, 0)] * self._numLEDs
                pixels[i] = (255, 255, 255)
                self._client.put_pixels(pixels)
                time.sleep(0.1)
