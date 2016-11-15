# -*- coding: utf-8 -*-
# @Author: djvolz
# @Date:   2016-11-14 17:03:11
# @Last Modified by:   djvolz
# @Last Modified time: 2016-11-15 01:13:28

import time
import json  # import json library to parse messages
import boto3  # import boto library that handles queuing functions
import lightSequence as ls


class Controller:

    def __init__(self):
        # Set the default action
        self._action = 'undefined'

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
        for message in \
                self._queue.receive_messages(
                MessageAttributeNames=['Author']):

            # Parse the message request for the action.
            request = json.loads(message.body)
            action = request['request']['action']
            if(action):
                self._action = action

            # Let the queue know that the message is processed
            message.delete()

    def run(self):
        # Jump straight in
        while True:
            # Process messages from Alexa
            self.processMessages()

            # Generate the light sequence based on the specified action
            self.lightsFactory(self._action)

            # Sleepy time
            time.sleep(1)
