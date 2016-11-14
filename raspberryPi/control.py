# contro.py
# <Description>
# Author: djvolz 11/14/16
    
import os
import time
import json # import json library to parse messages
import boto3 # import boto library that handles queuing functions
import chase

class Controller:

  def __init__(self):
    # Get the service resource
    sqs = boto3.resource('sqs')

    # Get the queue
    self._queue = sqs.get_queue_by_name(QueueName='talkWithCarlLights')


  # The response is NOT a resource, but gives you a message ID and MD5
  # print(response.get('MessageId'))
  # print(response.get('MD5OfMessageBody'))

  def launchScheme(self, scheme):
    program = chase.Chase('carl.local:7890', 64)
    while True:
      program.run()
    

  def processMessages(self):
    # Create a new message for testing
    response = self._queue.send_message(MessageBody='world')
    
    while True:
      # Process messages by printing out body and optional author name
      for message in self._queue.receive_messages(MessageAttributeNames=['Author']):
          # Get the custom author message attribute if it was set
          author_text = ''
          if message.message_attributes is not None:
              author_name = message.message_attributes.get('Author').get('StringValue')
              if author_name:
                  author_text = ' ({0})'.format(author_name)

          # Print out the body and author (if set)
          print('Hello, {0}!{1}'.format(message.body, author_text))

          # Let the queue know that the message is processed
          message.delete()

      time.sleep(1)

  def run(self):
    # Jump straight in
    # self.processMessages()



if __name__ == '__main__':
  controller = Controller()

  try:
    # DO PROGRAM THAT WE WROTE, MAKE VALHALLA PRETTY
    controller.run()
  except (KeyboardInterrupt, SystemExit):  #these aren't caught with exceptions...
    print("except (KeyboardInterrupt, SystemExit):")
    os._exit(0)
  except Exception as e:
    print("EXCEPTION:")
    print(e)
    os._exit(0) #kill process immediately so it can be respawned by the service.





  # for i in range(1,1000):
  #     # check queue to see if a request exists 
  #     incomingMsgs = queue.get_messages()

  #     # if messages are found, process
  #     if len(incomingMsgs) > 0:
  #         for incomingMsg in incomingMsgs:
  #             msg = json.loads(incomingMsg.get_body())
  #             action = msg['request']['action']

  # 	    # check what the requested action is
  # 	    if action == 'lights on':
  # 	        print 'pitch the ball'

  #         	# set parameters for IO on raspberry PI
  #     	        # relay_pin = 12

  # 	    	# configure IO on raspberry PI to communicate
  # 	    	# GPIO.setmode(GPIO.BOARD)
  # 	    	# GPIO.setwarnings(False)
  # 	    	# GPIO.setup(relay_pin, GPIO.OUT)

  # 	    	print "Relay Active"

  # 	    	# GPIO.output(relay_pin, GPIO.HIGH)

  # 	    	# pause
  # 	    	time.sleep(rotor_duration)

  # 	   	print "Relay Off"

  # 	    	# GPIO.output(relay_pin, GPIO.LOW)

  # 	    	#remove message from queue
  # 	    	queue.delete_message(incomingMsg)

  # 	    	# GPIO.cleanup()

  #     print i
