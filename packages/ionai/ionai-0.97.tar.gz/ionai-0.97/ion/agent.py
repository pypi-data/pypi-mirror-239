#
# [name] ion.agent.py
# [exec] python -m ion.agent
#
# Written by Yoshikazu NAKAJIM
#

from .const import *
from .core import *
from .net import *


#-- data provider

class data_agent(server_agent):
	_classname = 'ion.data_agent'

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def __init__(self):
		super().__init__()
		self._output_queryid = ID_ERROR

	def getOutputQueryID(self):
		return self._output_queryid

	def setOutputQueryID(self, id):
		self._output_queryid = id

	@property
	def output_queryid(self):
		return self.getOutputQueryID()

	@output_queryid.setter
	def output_queryid(self, id):
		self.setOutputQueryID(id)

	@property
	def output_qid(self):
		return self.output_queryid

	@output_qid.setter
	def output_qid(self, id):
		self.output_queryid = id

	@property
	def queryid(self):
		return self.output_queryid

	@queryid.setter
	def queryid(self, id):
		self.output_queryid = id

	def semantics(self, id=None):
		if (id is None):
			if (self.output_queryid == ID_ERROR):
				return super().semantics(0)
			else:
				return super().semantics(self.output_queryid)
		else:
			return super().semantics(id)

	def query_processing(self, cli_sock, cli_query):
		ldprint0('--> ion.data_agent.query_processing()')
		ldprint0('Client query: \'{0}\', {1}'.format(cli_query, type(cli_query)))

		self.output_queryid = self.query_check(cli_query)  # ここで，どの出力クエリと整合したかを確認
		ldprint0('Matched query ID: {}'.format(self.output_queryid))

		if (self.output_queryid == ID_ERROR):
			cli_sock.sendall(_encode(RESPONSE_ERROR))
			ldprint0('<-- ion.data_agent.query_processing(): {}'.format(False))
			return False

		self.update_data(cli_query)

		data = self.semantics(self.output_queryid).databody

		if (data is not None):
			cli_sock.sendall(_encode(RESPONSE_SUCCESS))

			if (isinstance(data, bytes)):
				ldprint0('Bytes data')
				cli_sock.sendall(_encode(data, 'json'))
			else:
				ldprint0('Non-bytes data')
				cli_sock.sendall(_encode(data))

		else:
			svr_message = RESPONSE_ERROR
			cli_sock.sendall(_encode(svr_message))

		ldprint0('<-- ion.data_agent.query_processing(): {}'.format(True))
		return True

	def update_data(self, cli_query):
		pass  # Nothing to do for genenral data agent

class data_provider(data_agent):
	pass


class database_agent(server_agent):  # query check（=事前登録したquery listとの整合確認）を行わないので、data_agent でなく server_agent を継承
	_classname = 'ion.database_agent'

	def __init__(self):
		super().__init__()
		self._outputdata = None

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def query_check(cli_query):
		__ERROR__ # disabled

	def getOutputData(self):
		return self._outputdata

	def setOutputData(self, d):
		self._outputdata = d

	@property
	def outputdata(self):
		return self.getOutputData()

	@outputdata.setter
	def outputdata(self, d):
		self.setOutputData(d)

	def getData(self):
		return self.getOutputData()

	def setData(self, d):
		self.setOutputData(d)

	@property
	def data(self):
		return self.getData()

	@data.setter
	def data(self, d):
		self.setData(d)

	def data_provision(self):
		return self.getOutputData()

class DB_agent(database_agent):
	pass

class database(database_agent):
	pass

class DB(database_agent):
	pass


class sensor_agent(data_agent):  # Realtime data provider
	_classname = 'ion.sensor_agent'

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def update_data(self, query):
		# Update data here.
		pass

class sen_agent(sensor_agent):
	pass

class sensor(sensor_agent):
	pass


#-- algorithm agent

class algorithm_agent(server_agent):
	_classname = 'ion.algorithm_agent'

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def query_processing(self, cli_sock, cli_query):
		#
		# (1) 出力クエリを比較
		# (2-1) クエリが整合したならば、SUCCESS を返し、(3) へ
		# (2-2) クエリが整合しなかったならば、ERROR を返し終了
		# (3) 出力クエリに基づいて、入力クエリを生成
		#     設定した入力クエリとは別に、出力インスタンスクエリから入力インスタンスクエリを生成すること
		# (4) 入力クエリの収集
		# (5-1) 入力クエリの収集が成功ならば、アルゴリズムを起動してデータを生成し、(6) へ
		# (5-2) 入力クエリの収集が失敗ならば、ERROR を返し終了
		# (6-1) データの生成が成功ならば、SUCCESS を返し、さらにデータを返す
		# (6-2) データの生成が失敗ならば ERROR を返し終了
		#
		pass

class algorithmagent(algorithm_agent):
	pass

class alg_agent(algorithm_agent):
	pass

class algagent(algorithm_agent):
	pass

class data_processor(algorithm_agent):
	pass

class dataprocessor(data_processor):
	pass

class processor(data_processor):
	pass


#-- main

if __name__ == '__main__':
	import argparse
	import nkj
	import ion

	_DEBUGLEVEL = 1 
	_LIB_DEBUGLEVEL = 0 
	nkj.str.debuglevel(_DEBUGLEVEL)
	nkj.str.lib_debuglevel(_LIB_DEBUGLEVEL)

	dpv = ion.data_provider()
	dpc = ion.data_processor()
