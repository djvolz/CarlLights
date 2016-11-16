# -*- coding: utf-8 -*-
# @Author: djvolz
# @Date:   2016-11-14 17:03:11
# @Last Modified by:   djvolz
# @Last Modified time: 2016-11-15 22:13:31

import time
import json  # import json library to parse messages
import boto3  # import boto library that handles queuing functions
import lightSequence as ls
from multiprocessing import Process


class Controller:

    def __init__(self):
        # Get the service resource
        sqs = boto3.resource('sqs')

        # Get the queue
        self._queue = sqs.get_queue_by_name(QueueName='talkWithCarlLights')

    def lightsFactory(self, type):
        program = ls.LightSequence.factory(type)
        if (program):
            print("TURNING LIGHTS ON LIKE WE AIN'T GOT NO POWER BILL")
            program.run()

    def processMessages(self):
        # Process messages by printing out body and optional author name
        for message in self._queue.receive_messages():
            # Parse the message request for the action.
            request = json.loads(message.body)
            action = request['request']['action']

            # Let the queue know that the message is processed
            message.delete()

            if(action):
                return action
            else:
                return None

    def run(self):
        procs = []
        while True:
            # Process messages from Alexa
            sequence = self.processMessages()

            print(sequence)

            # Generate the light sequence based on the specified action
            if(sequence):
                # Terminate other processes
                for proc in procs:
                    print("Terminating process")
                    proc.terminate()
                    procs.remove(proc)
                p = Process(target=self.lightsFactory, args=(sequence,))
                procs.append(p)
                p.start()

            # Time to rest
            time.sleep(5)
