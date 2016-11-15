#!/usr/bin/env python

# Light each LED in sequence, and repeat.

import opc, time

class Chase():
  def __init__(self, client, numLEDs=64):
    self._numLEDs = numLEDs
    self._client = opc.Client(client)

  def run(self):
    for i in range(self._numLEDs):
      pixels = [ (0,0,0) ] * self._numLEDs
      pixels[i] = (255, 255, 255)
      self._client.put_pixels(pixels)
      time.sleep(0.1)