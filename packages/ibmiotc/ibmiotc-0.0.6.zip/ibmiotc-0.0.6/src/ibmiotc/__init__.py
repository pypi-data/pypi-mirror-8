# *****************************************************************************
# Copyright (c) 2014 IBM Corporation and other Contributors.
#
# All rights reserved. This program and the accompanying materials
# are made available under the terms of the Eclipse Public License v1.0
# which accompanies this distribution, and is available at
# http://www.eclipse.org/legal/epl-v10.html 
#
# Contributors:
#   David Parker - Initial Contribution
# *****************************************************************************

import os
import time
import json
import socket
import ssl
import logging
import paho.mqtt.client as paho
import threading
import iso8601
from datetime import datetime

__version__ = "0.0.6"

class Message:
	def __init__(self, message):
		self.payload = json.loads(str(message.payload))
		self.timestamp = self.__parseMessageTimestamp()
		self.data = self.__parseMessageData()

		
	def __parseMessageTimestamp(self):
		try:
			if 'ts' in self.payload:
				return iso8601.parse_date(self.payload['ts'])
			else:
				return datetime.now()
		except iso8601.ParseError as e:
			raise InvalidEventException("Unable to parse event timestamp: %s" % str(e))
	
	
	def __parseMessageData(self):
		if 'd' in self.payload:
			return self.payload['d']
		else:
			return None

class AbstractClient:
	def __init__(self, organization, clientId, username, password, logDir=None):
		self.organization = organization
		self.username = username
		self.password = password
		self.address = organization + ".messaging.internetofthings.ibmcloud.com"
		self.port = 1883
		self.keepAlive = 60
		
		self.connectEvent = threading.Event()
		
		self.messages = 0
		self.recv = 0

		self.clientId = clientId
		
		# Configure logging
		self.logDir = logDir
		
		self.logger = logging.getLogger(self.__module__+"."+self.__class__.__name__)
		self.logger.setLevel(logging.DEBUG)

		logFileName = '%s.log' % (clientId.replace(":", "_"))
		self.logFile = os.path.join(self.logDir, logFileName) if (self.logDir is not None) else logFileName 

		# create file handler, set level to debug & set format
		fhFormatter = logging.Formatter('%(asctime)-25s %(name)-25s ' + ' %(levelname)-7s %(message)s')
		fh = logging.FileHandler(self.logFile)
		fh.setFormatter(fhFormatter)
		
		self.logger.addHandler(fh)

		self.client = paho.Client(self.clientId, clean_session=True)
		
		
		# Configure authentication
		if self.username is not None:
			#TODO: Support TLS 
			#self.port = 8883
			#self.client.tls_set(ca_certs="../../src/ibmiotc/cert/primary_intermediate.crt")
			#self.client.tls_set(ca_certs="../../src/ibmiotc/cert/primary_intermediate.crt", certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLSv1)
			#self.client.tls_insecure_set(True)
			self.client.username_pw_set(self.username, self.password)
			
		#attach MQTT callbacks
		self.client.on_log = self.on_log
		self.client.on_connect = self.on_connect
		self.client.on_disconnect = self.on_disconnect
		self.client.on_publish = self.on_publish

		self.start = time.time()

	def __logAndRaiseException(self, e):
		self.logger.critical(str(e))
		raise e
	
	def connect(self):
		self.logger.debug("Connecting... (address = %s, port = %s, clientId = %s, username = %s, password = %s)" % (self.address, self.port, self.clientId, self.username, self.password))
		try:
			self.connectEvent.clear()
			self.client.connect(self.address, port=self.port, keepalive=self.keepAlive)
			self.client.loop_start()
			if not self.connectEvent.wait(timeout=10):
				self.__logAndRaiseException(ConnectionException("Operation timed out connecting to the IBM Internet of Things service: %s" % (self.address)))
				
		except socket.error as serr:
			self.client.loop_stop()
			self.__logAndRaiseException(ConnectionException("Failed to connect to the IBM Internet of Things service: %s - %s" % (self.address, str(serr))))

	def disconnect(self):
		self.logger.info("Closing connection to the IBM Internet of Things Cloud")
		self.client.disconnect()
		self.stats()
		self.logger.info("Closed connection to the IBM Internet of Things Cloud")
			
	def stats(self):
		elapsed = ((time.time()) - self.start)
		
		msgPerSecond = 0 if self.messages == 0 else elapsed/self.messages
		recvPerSecond = 0 if self.recv == 0 else elapsed/self.recv
		self.logger.info("Messages published : %s, life: %.0fs, rate: 1/%.2fs" % (self.messages, elapsed, msgPerSecond))
		self.logger.info("Messages recieved  : %s, life: %.0fs, rate: 1/%.2fs" % (self.recv, elapsed, recvPerSecond))

		
	def on_log(self, mqttc, obj, level, string):
		self.logger.debug("%s" % (string))

	'''
	This is called after the client has received a CONNACK message from the broker in response to calling connect(). 
	The parameter rc is an integer giving the return code:
	0: Success
	1: Refused - unacceptable protocol version
	2: Refused - identifier rejected
	3: Refused - server unavailable
	4: Refused - bad user name or password (MQTT v3.1 broker only)
	5: Refused - not authorised (MQTT v3.1 broker only)
	'''
	def on_connect(self, client, userdata, flags, rc):
		if rc == 0:
			self.connectEvent.set()
			self.logger.info("Connected successfully")
		elif rc == 5:
			self.__logAndRaiseException(ConnectionException("Not authorized: s (%s, %s, %s)" % (self.clientId, self.username, self.password)))
		else:
			self.__logAndRaiseException(ConnectionException("Connection failed: RC= %s" % (rc)))

	'''
	This is called when the client disconnects from the broker. The rc parameter indicates the status of the disconnection. 
	When 0 the disconnection was the result of disconnect() being called, when 1 the disconnection was unexpected.
	'''
	def on_disconnect(self, mosq, obj, rc):
		if rc == 1:
			self.logger.error("Unexpected disconnect from the IBM Internet of Things Cloud")
		
	'''
	This is called when a message from the client has been successfully sent to the broker. 
	The mid parameter gives the message id of the successfully published message.
	'''
	def on_publish(self, mosq, obj, mid):
		self.messages = self.messages + 1


'''
See: http://stackoverflow.com/questions/2819696/parsing-properties-file-in-python/2819788#2819788
'''			
class ConfigFile(object):
	def __init__(self, fp, header):
		self.fp = fp
		self.sechead = '['+header+']\n'
	
	def readline(self):
		if self.sechead:
			try: 
				return self.sechead
			finally: 
				self.sechead = None
		else: 
			return self.fp.readline()


'''
Generic Connection exception "Something went wrong"
'''
class ConnectionException(Exception):
	def __init__(self, reason):
		self.reason = reason
	
	def __str__(self):
		return self.reason

'''
Specific Connection exception where the configuration is invalid
'''
class ConfigurationException(ConnectionException):
	def __init__(self, reason):
		self.reason = reason
	
	def __str__(self):
		return self.reason


'''
Specific Connection exception where the authentication method specified is not supported
'''
class UnsupportedAuthenticationMethod(ConnectionException):
	def __init__(self, method):
		self.method = method
	
	def __str__(self):
		return "Unsupported authentication method %s" % self.method


'''
Specific exception where and Event object can not be constructed
'''
class InvalidEventException(Exception):
	def __init__(self, reason):
		self.reason = reason
	
	def __str__(self):
		return "Invalid Event %s" % self.reason


