# -*- coding: utf-8 -*-
# @Author: djvolz
# @Date:   2016-11-14 17:03:11
# @Last Modified by:   djvolz
# @Last Modified time: 2016-11-14 18:53:59

import time
# import json  # import json library to parse messages
import boto3  # import boto library that handles queuing functions
import lightSequence as ls


class Controller:

    def __init__(self):
        # Get the service resource
        sqs = boto3.resource('sqs')

        # Get the queue
        self._queue = sqs.get_queue_by_name(QueueName='talkWithCarlLights')

    # The response is NOT a resource, but gives you a message ID and MD5
    # print(response.get('MessageId'))
    # print(response.get('MD5OfMessageBody'))

    def lightsFactory(self, type):
        program = ls.LightSequence.factory(type)
        while True:
            program.run()

    def processMessages(self):
        # Create a new message for testing
        # response = self._queue.send_message(MessageBody='world')

        while True:
            # Process messages by printing out body and optional author name
            for message in \
                    self._queue.receive_messages(
                    MessageAttributeNames=['Author']):

                print(message)

                # TODO: process the message and respond with appropriate action
                # msg = json.loads(incomingMsg.get_body())
                # action = message['request']['action']

                # if action == 'lights on':
                #     print 'TURNING LIGHTS ON LIKE WE AIN'T GOT NO POWER BILL'
                # if this works then:
                # lightsFactory(action)

                # Get the custom author message attribute if it was set
                author_text = ''
                if message.message_attributes is not None:
                    author_name = message.message_attributes.get(
                        'Author').get('StringValue')
                    if author_name:
                        author_text = ' ({0})'.format(author_name)

                # Print out the body and author (if set)
                print('Hello, {0}!{1}'.format(message.body, author_text))

                # Let the queue know that the message is processed
                message.delete()

            time.sleep(1)

    def run(self):
        # Jump straight in
        self.processMessages()
