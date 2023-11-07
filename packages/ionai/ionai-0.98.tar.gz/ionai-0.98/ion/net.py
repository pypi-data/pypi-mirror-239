
# [name] ion.net.py
# [test] python -m ion.net
#
# Written by Yoshikazu NAKAJIMA
#

import sys
import json
import pprint  # リストや辞書を整形して出力
import datetime
import copy
from typing import Union
import socket
import pickle
import time

# nkjlib

from nkj.str import *
import nkj.time as nt


# ionlib

from .core import *


# constants

__BROADCAST_BINDING_ADDRESS = ''
__BROADCAST_SENDING_ADDRESS = '255.255.255.255'

_DEFAULT_UDPPORT = 8060
_DEFAULT_TCPPORT = 8061
_DEFAULT_BUFFERSIZE = 4096
_DEFAULT_BACKLOG = 1
_DEFAULT_TIMEOUT = 5.0 # sec
_DEFAULT_SLEEPTIME = 0  # sec
_DEFAULT_CODING = 'json'  # {'utf-8', 'shift_jis', 'json', 'pickle', 'binary'}

"""
[encoding methods]
'文字列'.encode()/b'バイト列'decode():  文字列 <-> バイト列の変換．
json.dumps()/json.loads():              辞書形式 <-> 文字列の直列化．これと encode()/decode() の組合せが安全．
pickle.dumps()/pickle.loads(): データのシリアライズ(Serialize)．安全でない．非シリアライズの過程で任意のコードを実行するような悪意のある pickle オブジェクトを生成可能．
json に比べ、pickle はバイナリを処理できるが、(1) python 特有、かつ (2) 安全でない
"""

__PACKET_PREPOSITION = 'iON.PACKET: '

__DEFAULT_PACKET_ENCRYPTION_FLAG = True

__COMMAND_SHUTDOWN = 'ion.shutdown'
__RESPONSE_SHUTDOWN = 'ion.bye'
__COMMAND_RESPONSEREQUEST = 'ion.response_request'
__RESPONSE_RESPONSEREQUEST = 'ion.alive'
__COMMAND_DATAREQUEST = 'ion.data_request'
__RESPONSE_SUCCESS = 'ion.success'
__RESPONSE_ERROR = 'ion.error'
__RESPONSE_SUCCEEDED = __RESPONSE_SUCCESS
__RESPONSE_FAILED = __RESPONSE_ERROR
__RESPONSE_OK = 'ion.ok'
__RESPONSE_CANCEL = 'ion.cancel'
__RESPONSE_YES = __RESPONSE_OK
__RESPONSE_NO = __RESPONSE_CANCEL

__UDPPORT = _DEFAULT_UDPPORT
__TCPPORT = _DEFAULT_TCPPORT
__BUFFERSIZE = _DEFAULT_BUFFERSIZE
__BACKLOG = _DEFAULT_BACKLOG
__TIMEOUT = _DEFAULT_TIMEOUT
__SLEEPTIME = _DEFAULT_SLEEPTIME
__CODING = _DEFAULT_CODING

__ID_ERROR = -1


# local access

_PACKET_ENCRYPTION_FLAG = __DEFAULT_PACKET_ENCRYPTION_FLAG

_PACKET_PREPOSITION = __PACKET_PREPOSITION
_COMMAND_SHUTDOWN = __COMMAND_SHUTDOWN
_RESPONSE_SHUTDOWN = __RESPONSE_SHUTDOWN
_COMMAND_RESPONSEREQUEST = __COMMAND_RESPONSEREQUEST
_RESPONSE_RESPONSEREQUEST = __RESPONSE_RESPONSEREQUEST
_COMMAND_DATAREQUEST = __COMMAND_DATAREQUEST
_RESPONSE_SUCCESS = __RESPONSE_SUCCESS
_RESPONSE_ERROR = __RESPONSE_ERROR
_RESPONSE_SUCCEEDED = __RESPONSE_SUCCEEDED
_RESPONSE_FAILED = __RESPONSE_FAILED
_RESPONSE_OK = __RESPONSE_OK
_RESPONSE_CANCEL = __RESPONSE_CANCEL
_RESPONSE_YES = __RESPONSE_YES
_RESPONSE_NO = __RESPONSE_NO

_ID_ERROR = __ID_ERROR


# global access

BROADCAST_BINDING_ADDRESS = __BROADCAST_BINDING_ADDRESS
BROADCAST_SENDING_ADDRESS = __BROADCAST_SENDING_ADDRESS
BROADCAST_BINDADDR = BROADCAST_BINDING_ADDRESS
BROADCAST_SENDADDR = BROADCAST_SENDING_ADDRESS

UDPPORT = __UDPPORT
TCPPORT = __TCPPORT

COMMAND_SHUTDOWN = _COMMAND_SHUTDOWN
RESPONSE_SHUTDOWN = _RESPONSE_SHUTDOWN
COMMAND_RESPONSEREQUEST = _COMMAND_RESPONSEREQUEST
RESPONSE_RESPONSEREQUEST = _RESPONSE_RESPONSEREQUEST
COMMAND_DATAREQUEST = _COMMAND_DATAREQUEST
RESPONSE_SUCCESS = _RESPONSE_SUCCESS
RESPONSE_ERROR = _RESPONSE_ERROR
RESPONSE_SUCCEEDED = _RESPONSE_SUCCEEDED
RESPONSE_FAILED = _RESPONSE_FAILED
RESPONSE_OK = _RESPONSE_OK
RESPONSE_CANCEL = _RESPONSE_CANCEL
RESPONSE_YES = _RESPONSE_YES
RESPONSE_NO = _RESPONSE_NO

ID_ERROR = _ID_ERROR


# global functions

def udpport(port=None):
	global UDPPORT
	if (port is None):
		return UDPPORT
	else:
		UDPPORT = port
		return True

def tcpport(port=None):
	global TCPPORT
	if (port is None):
		return TCPPPORT
	else:
		TCPPORT = port
		return True

def encryption_flag(flag=None):
	global _PACKET_ENCRYPTION_FLAG
	if (flag is None):
		return _PACKET_ENCRYPTION_FLAG
	else:
		_PACKET_ENCRYPTION_FLAG = flag
		return True

def buffersize(size=None):
	global __BUFFERSIZE
	if (size is None):
		return __BUFFERSIZE
	else:
		__BUFFERSIZE = size
		return True

def buffer_size(size=None):
	return buffersize(size)

def backlog(num=None):
	global __BACKLOG
	if (num is None):
		return __BACKLOG
	else:
		__BACKLOG = num
		return True

def listen_num(num=None):
	return backlog(num)

def timeout(time=None):
	global __TIMEOUT
	if (time is None):
		return __TIMEOUT
	else:
		__TIMEOUT = time
		return True

def timeout_(time=None):
	return timeout(time)

def sleeptime(time=None):
	global __SLEEPTIME
	if (time is None):
		return __SLEEPTIME
	else:
		__SLEEPTIME = time
		return True

def sleep_time(time=None):
	return sleeptime(time)

def coding(code=None):
	global __CODING
	if (code is None):
		return __CODING
	else:
		__CODING = code
		return True

def coding_(code=None):
	return coding(code)

# encoding/decoding functions

def _add_preposition(message):
	global _PACKET_PREPOSITION
	return _PACKET_PREPOSITION + message

def _remove_preposition(message):
	global _PACKET_PREPOSITION
	lenpp = len(_PACKET_PREPOSITION)
	prestr = message[0:lenpp]
	if (prestr == _PACKET_PREPOSITION):
		message = message[lenpp:]
	else:
		raise ValueError("ERROR: Non-iON packet.")  # iON packet でない場合は、例外を発生
	return message

def _encrypt(message):
	if (encryption_flag()):
		ldprint2('encrypt...')
		return message
	else:
		return message  # Noting done

def _decrypt(message):
	if (encryption_flag()):
		ldprint2('decrypt...')
		return message
	else:
		return message  # Noting done

def _package(message):
	return _add_preposition(_encrypt(message))

def _unpackage(message):
	return _decrypt(_remove_preposition(message))

def _encode(message, coding=None):
	ldprint('--> _encode(\'{0}\', {1})'.format(message, coding))
	coding = coding_() if (coding is None) else coding
	ldprint2('message: \'{}\''.format(message))
	ldprint2('coding:  \'{}\''.format(coding))
	if (coding == 'utf-8' or coding == 'shift_jis'):
		encoded_message = _package(message).encode(coding)
	elif (coding == 'json'):
		encoded_message = _package(json.dumps(message)).encode('utf-8')
	elif (coding == 'pickle' or coding == 'binary'):
		encoded_message = _package(pickle.dumps(message))
	else:
		__ERROR__
	ldprint('<-- _encode(): {}'.format(encoded_message))
	return encoded_message

def _decode(packet_message, coding=None):
	ldprint('--> _decode({0}, {1})'.format(packet_message, coding))
	coding = coding_() if (coding is None) else coding
	ldprint2('packet: \'{}\''.format(packet_message))
	ldprint2('coding: \'{}\''.format(coding))
	"""
	if (packet_message == b''):
		ldprint('<-- _decode(): \'{}\''.format(''))
		return ''
	"""
	if (coding == 'utf-8' or coding == 'shift_jis'):
		message = _unpackage(packet_message.decode())
	elif (coding == 'json'):
		message = json.loads(_unpackage(packet_message.decode()))
	elif (coding == 'pickle' or coding == 'binary'):
		message = pickle.loads(_unpackage(packet_message))
	else:
		__ERROR__
	ldprint('<-- _decode(): \'{}\''.format(message))
	return message

def _binary_encode(message):
	return _encode(message, 'binary')

def _binary_deode(packet_message):
	return _deode(packet_message, 'binary')

def encode(message, coding=None):
	return _encode(message, coding)

def decode(packet_message, coding=None):
	return _decode(packet_message, coding)

def binary_encode(message):
	return _binary_encode(message)

def binary_decode(packet_message):
	return _binary_decode(packet_message)

def server_response(cli_sock, response):
	cli_sock.sendall(_encode(response))

def svr_response(cli_sock, response):
	server_response(cli_sock, response)


#------ class ------------------------------------------------
# server

class server_cls():
	_classname = 'ion.server_cls'

	def __init__(self):
		self._commsock = None
		self._datasock = None
		self._address = socket.gethostbyname(socket.gethostname())
		self._datafound = False
		self._tcpport = TCPPORT
		self._udpport = UDPPORT
		ldprint('Server IP Address: {}'.format(self.address))
		if (not self.open()):
			__ERROR__

	def __del__(self):
		self.close()

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	@property
	def address(self):
		return self._address

	@address.setter
	def address(self, a):
		self._address = a

	@property
	def udpport(self):
		return self._udpport

	@udpport.setter
	def udpport(self, p):
		self._udpport = p

	@property
	def tcpport(self):
		return self._tcpport

	@tcpport.setter
	def tcpport(self, p):
		self._tcpport = p

	@property
	def buffersize(self):
		return buffer_size()

	@buffersize.setter
	def buffersize(self, size):
		buffer_size(size)

	@property
	def command_socket(self):
		return self._commsock

	@command_socket.setter
	def command_socket(self, s):
		self._commsock = s

	@property
	def comm_sock(self):
		return self.command_socket

	@comm_sock.setter
	def comm_sock(self, s):
		self.command_socket = s

	@property
	def data_socket(self):
		return self._datasock

	@data_socket.setter
	def data_socket(self, s):
		self._datasock = s

	@property
	def data_sock(self):
		return self.data_socket

	@data_sock.setter
	def data_sock(self, s):
		self.data_socket = s

	@property
	def backlog(self):
		return backlog()

	@backlog.setter
	def backlog(self, n):
		backlog(n)

	@property
	def timeout(self):
		return timeout_()

	@timeout.setter
	def timeout(self, t):
		timeout_(t)

	@property
	def sleeptime(self):
		return sleep_time()

	@sleeptime.setter
	def sleeptime(self, t):
		sleep_time(t)

	@property
	def coding(self):
		return coding_()

	@coding.setter
	def coding(self, c):
		coding_(c)

	@property
	def datafound(self):
		return self._datafound

	@datafound.setter
	def datafound(self, flag):
		self._datafound = flag

	def _udprecv(self, cli_sock):
		ldprint('[SVR] Buffersize: {}'.format(self.buffersize))
		return cli_sock.recvfrom(self.buffersize)            # サーバからメッセージを受け取る．

	def _tcprecv(self, cli_sock):
		ldprint('[SVR] Buffersize: {}'.format(self.buffersize))
		return cli_sock.recv(self.buffersize)            # サーバからメッセージを受け取る．

	def open(self):
		if (self.comm_sock is not None):
			self.close()
		if (self.data_sock is not None):
			self.close()

		try:
			self.comm_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  #-- UDP socket 生成
			"""
			"""
			self.comm_sock = socket.socket(socket.AF_INET, type=socket.SOCK_DGRAM)  #-- UDP socket 生成
			ldprint('[SVR] Timeout: {} (sec)'.format(self.timeout))
			self.comm_sock.settimeout(self.timeout)
			ldprint('[SVR] broadcast (UDP) binding address: \'{}\''.format(BROADCAST_BINDING_ADDRESS))
			ldprint('[SVR] broadcast (UDP) port:            {}'.format(self.udpport))
			self.comm_sock.bind((BROADCAST_BINDING_ADDRESS, self.udpport))  #-- broadcast で UDP socket を binding
			ldprint('[SVR] Binding succeeded')

		except socket.error as e:
			print('[SVR] ERROR: {}'.format(e), flush=True)
			self.close()
			return False

		except OSError:
			print_error('iON ERROR: OS error')
			self.close()
			return False

		return True

	def launch(self):
		def __ion_command(cli_message):
			ldprint('--> server.__ion_command(\'{}\')'.format(cli_message))
			if (self.data_sock is None):
				__ERROR__
			if (cli_message == _COMMAND_RESPONSEREQUEST):
				ldprint('[SVR] command: response request')
				svr_message = _RESPONSE_RESPONSEREQUEST
				ldprint('[SVR] SVRMESSAGE: {}'.format(svr_message))
				self.data_sock.sendall(_encode(svr_message))
			else:
				ldprint('[SVR] command: unknown')
				ldprint('<-- server.__ion_command(): {}'.format(False))
				return False
			ldprint('<-- server.__ion_command(): {}'.format(True))
			return True

		while True:
			ldprint('[SVR] Start connection process...')

			try:
				cli_data, cli_info = self.comm_sock.recvfrom(self.buffersize)  # UDP packet を receive
				cli_addr, cli_port = cli_info
				ldprint('[SVR] received data: \'{}\''.format(cli_data))
				ldprint('[SVR] client address: {0}, client port: {1}'.format(cli_addr, cli_port))

			except socket.error as e:
				#ldprint0('[SVR] ERROR: {}'.format(e))
				continue

			except KeyboardInterrupt:
				ldprint0('[SVR] Keyboard Interrupt')
				break

			else:
				ldprint('[SVR] Receive data, {}, from client:{}'.format(cli_data, cli_addr))

			#----- client message processing -----

			try:
				cli_message = None if (cli_data == '') else _decode(cli_data)  #-- packet のデコード

			except ValueError as e:  # Including non-iON-packet error
				print_error(e)
				continue  # UDP packet の receive を継続する

			ldprint('[SVR] Received message: \'{0}\', Client address: {1}, Client port: {2}'.format(cli_message, cli_addr, cli_port))

			#----- send response -----

			ldprint('[SVR] data socket preparation')

			try:
				self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #-- TCP/IP socket を生成
				self.data_sock.connect((cli_addr, self.tcpport))  #-- データ通信のため client と TCP/IP で接続

			except socket.error as e:
				print_error(e)
				self.datasock_close()
				__ERROR__

			if (self.data_sock is None):
				__ERROR__

			if (self.sleeptime != 0):
				time.sleep(self.sleeptime)  # client への接続準備待ち

			ldprint('[SVR] data socket preparation was done')
			ldprint('[SVR] start processing...')

			if (cli_message == _COMMAND_SHUTDOWN):
				ldprint('[SVR] command: shutdown')
				svr_message = _RESPONSE_SHUTDOWN
				ldprint('[SVR] SVRMESSAGE: {}'.format(svr_message))
				self.data_sock.sendall(_encode(svr_message))
				print_message('iON SERVER: Shutdown...')
				self.close()
				break

			if (__ion_command(cli_message)):
				ldprint('[SVR] ion command')
				pass

			elif (self._data_processing(self.data_sock, cli_message)):
				ldprint('[SVR] ion data processing')
				self.datafound = False  # データ供給を終えたので，フラグを False にする．

			elif (self.query_processing(self.data_sock, cli_message)):
				ldprint('[SVR] ion query processing')
				self.datafound = True  # クエリチェックで整合したので、フラグを True にしてデータ供給に備える．

			else:
				self.error_processing(self.data_sock)
				ldprint('[SVR] ion error')

			self.datasock_close()
		#-- end: while
		return True

	def datasock_close(self):
		if (self.data_sock is None):
			return False
		self.data_sock.close()
		self.data_sock = None
		return True

	def close(self):
		self.datasock_close()
		if (self.comm_sock is None):
			return False
		self.comm_sock.close()
		self.comm_sock = None
		return True

	def is_closed(self):
		return (self.svr_socket is None)

	def closed(self):
		return self.is_closed()

	def is_opened(self):
		return (not self.is_closed())

	def opened(self):
		return self.is_opened()

	# iON data processing

	def data_provision(self):  # Function for Override
		return 'DEFAULT_DATA_RESPONSE'

	def dataprovision(self):
		return self.data_provision()

	@property
	def data(self):
		return self.data_provision()

	def _data_sending(self, data_sock):
		ldprint('--> ion.server._data_sending()'.format())
		data_sock.sendall(_encode(self.data_provision()))
		ldprint('<-- ion.server._data_sending()')

	def _data_processing(self, data_sock, cli_query):
		ldprint('--> ion.server._data_processing(,, \'{}\')'.format(cli_query))
		if (cli_query == _COMMAND_DATAREQUEST):
			if (self.datafound):
				self._data_sending(data_sock)
			else:
				data_sock.sendall(_encode(RESPONSE_ERROR))
				raise ValueError("ERROR: Illegal iON protocol.")  # iON 通信プロトコル違反
		else:
			ldprint('<-- ion.server._data_processing(): {}'.format(False))
			return False
		ldprint('<-- ion.server._data_processing(): {}'.format(True))
		return True

	# iON query processing

	def query_processing(self, data_sock, cli_query):  # Function for Override
		if (cli_query == 'query #1' or cli_query == 'query #2' or cli_query == 'query #3'):
			data_sock.sendall(_encode(RESPONSE_SUCCESS))
			return True
		else:
			data_sock.sendall(_encode(RESPONSE_ERROR))
			return False

	def queryprocessing(self, data_sock, cli_query):
		return query_processing(data_sock, cli_query)

	# iON error processing

	def error_processing(self, data_sock):
		print_error('Query search was failed.')
		data_sock.sendall(_encode(RESPONSE_ERROR))

	def errorprocessing(self, data_sock):
		error_processing(data_sock)

class server(server_cls):  # alias
	pass


# client

class client_cls():
	_classname = 'ion.client_cls'

	def __init__(self):
		self._comm_sock = None
		self._data_sock = None
		self._udpport = UDPPORT
		self._tcpport = TCPPORT
		if (not self.open()):
			__ERROR__

	def __del__(self):
		if (not self.close()):
			__ERROR__

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	@property
	def command_socket(self):
		return self._comm_sock

	@command_socket.setter
	def command_socket(self, s):
		self._comm_sock = s

	@property
	def comm_sock(self):
		return self.command_socket

	@comm_sock.setter
	def comm_sock(self, s):
		self.command_socket = s

	@property
	def data_socket(self):
		return self._data_sock

	@data_socket.setter
	def data_socket(self, s):
		self._data_sock = s

	@property
	def data_sock(self):
		return self.data_socket

	@data_sock.setter
	def data_sock(self, s):
		self.data_socket = s

	@property
	def udpport(self):
		return self._udpport

	@udpport.setter
	def udpport(self, p):
		self._udpport = p

	@property
	def tcpport(self):
		return self._tcpport

	@tcpport.setter
	def tcpport(self, p):
		self._tcpport = p

	@property
	def buffersize(self):
		return buffer_size()

	@buffersize.setter
	def buffersize(self, size):
		buffer_size(size)

	@property
	def sleeptime(self):
		return sleep_time()

	@sleeptime.setter
	def sleeptime(self, t):
		sleep_time(t)

	def open(self):
		ldprint('--> ion.client.open()')

		if (self.comm_sock is not None):
			__ERROR__
		if (self.data_sock is not None):
			__ERROR__

		try:
			self.comm_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)     # UDP socket の生成
			self.comm_sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)  # socket option で broadcast 設定

		except socket.error as e:
			ldprint2('[CLI] Connection failed.')
			print_error(e)
			self.close()
			if (self.sleeptime != 0.0):
				time.sleep(self.sleeptime)
			ldprint('<-- ion.client.open(): {}'.format(False))
			return False

		try:
			self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)    # TCP/IP で socket を生成
			ldprint('[CLI] broadcast (TCP) binding address: \'{}\''.format(BROADCAST_BINDING_ADDRESS))
			ldprint('[CLI] broadcast (TCP) port:            {}'.format(self.tcpport))
			self.data_sock.bind((BROADCAST_BINDING_ADDRESS, self.tcpport))       # socket を broadcast (空アドレス'') で bind
			self.data_sock.listen(1)                                              # listen 開始

		except socket.error as e:
			ldprint2('[CLI] Connection failed.')
			print_error(e)
			self.close()
			ldprint('<-- ion.client.open(): {}'.format(False))
			return False

		ldprint('[CLI] Connection succeeded.')
		ldprint('<-- ion.client.open(): {}'.format(True))
		return True

	def close(self):
		if (self.data_sock is not None):
			self.data_sock.close()
			self.data_sock = None
		if (self.comm_sock is not None):
			self.comm_sock.close()
			self.comm_sock = None
		return True

	def is_closed(self):
		if ((self.comm_sock is None) or (self.data_sock is None)):
			if ((self.comm_sock is not None) or (self.data_sock is not None)):
				__ERROR__
		return (self.comm_sock is None)

	def closed(self):
		return self.is_closed()

	def is_opened(self):
		return (not self.is_closed())

	def opened(self):
		return self.is_opened()

	def _udprecv(self, cli_sock):
		ldprint('[SVR] Buffersize: {}'.format(self.buffersize))
		return cli_sock.recvfrom(self.buffersize)            # サーバからメッセージを受け取る．

	def _tcprecv(self, cli_sock):
		ldprint('[SVR] Buffersize: {}'.format(self.buffersize))
		return cli_sock.recv(self.buffersize)            # サーバからメッセージを受け取る．

	"""
	def recv(self):
		ldprint('--> client.recv()')
		connectionflag = False
		if (not self.opened()):
			ldprint2('[CLI] Not opened. Trying to open socket.')
			if (self.connect()):
				ldprint2('[CLI] Connection succeeded.')
				connectionflag = True
			else:
				ldprint2('<Server connection failed>')
				ldprint('<-- client.send(): \'{}\''.format(None))
				return None

		if (self.comm_sock is None):
			__ERROR__

		svr_packet = self.__recv(self.comm_sock)
		ldprint2('[CLI] Packet from server: {}'.format(svr_packet))

		try:
			svr_message = _decode(svr_packet)
		except ValueError as e:
			print_error(e)
			svr_message = e
		ldprint2('[CLI] Received:   \'{}\''.format(svr_message))

		if (connectionflag):
			self.close()
		ldprint('<-- client.recv(): \'{}\''.format(svr_message))
		return svr_message
	"""

	def send(self, cli_message):
		ldprint('--> client.send(\'{}\')'.format(cli_message))

		packet_message = _encode(cli_message)
		ldprint('[CLI] Packet message: {}'.format(packet_message))

		if (self.comm_sock is None):
			__ERROR__

		self.comm_sock.sendto(packet_message, (BROADCAST_SENDING_ADDRESS, self.udpport))  # サーバへメッセージを送る．
		ldprint('[CLI] Packet sent.')

		# データ受信

		while True:
			try:
				conn, addr = self.data_sock.accept()
				svr_packet = conn.recv(self.buffersize)  # サーバからメッセージを受け取る．
				ldprint2('[CLI] Packet from server: {}'.format(svr_packet))
				conn.close()

				try:
					svr_message = _decode(svr_packet)
				except ValueError as e:
					print_error(e)
					svr_message = e
					break

				ldprint2('[CLI] Received:   \'{}\''.format(svr_message))

			except socket.error as e:
				print_error(e)
				__ERROR__

			else:
				break

		ldprint('<-- client.send(): \'{}\''.format(svr_message))
		return svr_message

	def command(self, command):
		return self.send(command)

	def data_acquisition(self):
		return self.command(_COMMAND_DATAREQUEST)

	def dataacquisition(self):
		return self.data_acquisition()

	def data_search(self, querystr):
		ldprint('--> ion.client.data_search(, \'{0}\' ({1}))'.format(querystr, type(querystr)))
		res = self.command(querystr)
		ldprint2('RESPONSE: \'{}\''.format(res))
		if (res == _RESPONSE_SUCCESS):
			ldprint('[CLI] DATA ACQUISITION')
			res = self.data_acquisition()
			ldprint('RESPONSE: \'{}\''.format(res))
		else:
			return _RESPONSE_ERROR
		ldprint('<-- ion.client.data_search()')
		return res

	def datasearch(self, querystr):
		return self.data_search(querystr)

	def query_search(self, querystr):
		return self.data_search(querystr)

	def querysearch(self, querystr):
		return self.query_search(querystr)

	def receive(self):
		return self.recv()

	def response(self):  # Receive response from the server
		return self.receive()

	def query(self, query):
		return self.send(query)

class client(client_cls):  # alias
	pass


# Network agents

class server_agent(server_cls):  # Add query operations to server_cls()
	_classname = 'ion.server_agent'

	def __init__(self, sl=None):
		super().__init__()
		self.setSemanticsList(sl)

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def getSemanticsList(self):
		return self._semlist

	def setSemanticsList(self, sl):
		if (sl is None):
			self._semlist = [ion_agent()]
		elif (isinstance(sl, ion.ion_agent)):
			self._semlist = [sl]
		elif (isinstance(sl, dict)):
			self._semlist = [ion_agent(dict)]
		elif (isinstance(sl, list) or isinstance(sl, tuple)):
			self._semlist = [ion_agent(todict(sl))]
		else:
			__ERROR__  # Illegal type of semantics list

		self._updateQueryList()  # Synchronize the semantics list to the query list

	@property
	def semanticslist(self):
		return self.getSemanticsList()

	@semanticslist.setter
	def semanticslist(self, sl):
		self.setSemanticsList(sl)

	def getSemList(self):
		return self.getSemanticsList()

	def setSemList(self, sl):
		self.setSemanticsList(sl)

	@property
	def semlist(self):
		return self.getSemList()

	@semlist.setter
	def semlist(self, sl):
		self.setSemList(sl)

	def getSemantics(self, id=0):
		if (id >= 0 and id < len(self.semanticslist)):
			return self.semanticslist[id]
		else:
			return None  # ERROR

	def setSemantics(self, s, id=None):
		sllen = len(self.semanticslist)
		if (id is None):
			self.semanticslist.append(s)
		elif (id < 0):
			return False
		elif (id == sllen):
			self.semanticslist.append(s)
		elif (id > sllen):
			for i in range(sllen, id):
				self.semanticslist.append(ion_agent())
			self.semanticslist.append(s)
		else:
			self.semanticslist[id] = s
		self._updateQueryList()
		return True

	def semantics(self, id=0, s=None):
		if (s is None):
			if (id < 0 or id > len(self.semanticslist) - 1):
				return None
			else:
				return self.getSemantics(id)
		else:
			return self.setSemantics(id, s)

	def sem(self, id=0, s=None):
		return semantics(id, s)

	def s(self, id=0, s=None):
		return semantics(id, s)

	def _updateQueryList(self):
		if (self.semantics is None):
			self._querylist = None
		else:
			self._querylist = [sem.query for sem in self.semanticslist]

	def getQueryList(self):
		return self._querylist

	@property
	def querylist(self):
		return self.getQueryList()

	def getQuery(self, id=0):
		if (id >= 0 and id < len(self.querylist)):
			return self.querylist[id]
		else:
			return None  # ERROR

	def query(self, id=0):
		return self.getQuery(id)

	def q(self, id=0):
		return self.query(id)

	def query_check(self, cli_query):
		ldprint('--> ion.server_agent()')
		ldprint('Query: \'{0}\' ({1})'.format(cli_query, type(cli_query)))
		if (type(cli_query) == 'dict'):
			ldprint('Dict type')
			cli_query = query(dict)
			ldprint('Query: \'{0}\' ({1})'.format(cli_query, type(cli_query)))
		else:
			__ERROR__
		if (not isinstance(cli_query, ion.query)):
			ldprint0('ERROR: Non-query inputed.')
			ldprint('<-- ion.server_agent()')
			return _ID_ERROR
		for id in range(len(self.querylist)):
			if (self.query(id) <= cli_query):
				return id
		ldprint('<-- ion.server_agent()')
		return _ID_ERROR

	def query_processing(self, cli_sock, cli_query):
		ldprint0('Client query: \'{0}\', {1}'.format(cli_query, type(cli_query)))
		qid = self.query_check(cli_query)
		ldprint0('Matched query ID: {}'.format(qid))
		if (qid == _ID_ERROR):
			cli_sock.sendall(_encode(RESPONSE_ERROR))
			return False
		else:
			cli_sock.sendall(_encode(RESPONSE_SUCCESS))
			return True

class serveragent(server_agent):  # alias
	pass


class client_agent(client_cls):
	_classname = 'ion.client_agent'

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

class clientagent(client_agent):  # alias
	pass


#-- main

if __name__ == '__main__':
	import argparse
	import ion

	_DEBUGLEVEL = 1
	_LIB_DEBUGLEVEL = 0

	debuglevel(_DEBUGLEVEL)
	lib_debuglevel(_LIB_DEBUGLEVEL)

	parser = argparse.ArgumentParser()

	parser.add_argument('--mode', '-mode', choices=['server', 'client'], default='client')
	args = parser.parse_args()
	mode = args.mode

	if (mode == 'server'):
		svr = ion.server_agent()
		svr.launch()

	elif (mode == 'client'):
		for command in [ion.COMMAND_RESPONSEREQUEST, ion.COMMAND_SHUTDOWN]:
			dprint('[MAIN] command: \'{}\''.format(command))
			message = ion.client_agent().send(command)
			if (message is None):
				print_error('[MAIN] command sending error.')
				break
			else:
				dprint('[MAIN] server response: \'{}\''.format(message))
	else:
		__ERROR__
