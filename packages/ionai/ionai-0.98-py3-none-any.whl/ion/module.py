#
# [name] ion.module.py
#
# Written by Yoshikazu NAKAJIMA
#
import nkj as n

# ionlib

from .core import *


#-- classes

DEFAULT_SEMANTICS_ID = 0

class semantics_list(n.listex):
	_classname = 'ion.semantics_list'

	def __new__(cls, second=None):
		return super().__new__(cls, second)

	def __init__(self, second=None):
		super().__init__(second)
		self.componentclass = semantics_cls
		self.id = None

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def getID(self):
		return self._id

	def setID(self, id):
		self._id = id

	@property
	def id(self):
		return self.getID()

	@id.setter
	def id(self, id_):
		self.setID(id_)

	def getSemantics(self, id=None):
		if (len(self) == 0):
			return None
		elif (id is None):
			return self[DEFAULT_SEMANTICS_ID] if (self.id is None) else self[self.id]
		else:
			return self[id]

	def setSemantics(self, id, s):
		s = copy.deepcopy(s)
		if (id is None):
			self.append(s)
		else:
			self[id] = s

	@property
	def semantics(self):
		return self.getSemantics()

	@semantics.setter
	def semantics(self, s):
		self.setSemantics(None, s)

	@property
	def sem(self):
		return self.semantics

	@sem.setter
	def sem(self, s):
		self.semantics = s

	@property
	def s(self):
		return self.semantics

	@s.setter
	def s(self, s_):
		self.semantics = s_

	def getQuery(self, id=None):
		return self.getSemantics(id).getQuery()

	@property
	def query(self):
		return self.getQuery()

	@property
	def q(self):
		return self.query

class semanticslist(semantics_list):
	pass

class semlist(semantics_list):
	pass

class slist(semantics_list):
	pass


class module():
	_classname = 'ion.module'

	def __init__(self):
		self.output_semlist = semantics_list()
		self.output_semlist_id = None

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def searchData(query):
		ldprint('--> ion.module.searchData()')
		if (not collateOutputQuery(query)):
			ldprint('<-- ion.module.searchData()')
			return None

		if (False):  # for DEBUG
			ldprint('list ID: {}'.format(self.oslist_id))
			if (self.oslist_id is None):
				ldprint('<-- ion.module.searchData()')
				return None

		data = self._getData()
		ldprint('data: {}'.format(data))
		ldprint('<-- ion.module.searchData()')
		return data

	def search_data(query):
		return self.searchData(query)

	def collateOutputQuery(self, query):
		if (len(self.oslist) == 0):
			return False
		for i in range(len(self.oslist)):
			if (query <= self.oslist[i].getQuery()):
				self.oslist_id = i
				return True
		return False

	def collateQuery(self, query):
		return self.collateOutputQuery(query)

	def collate(self, query):
		return self.collateQuery(query)

	def query_collation(self, query):
		return self.collateQuery(query)

	def getData(self, id=None):  # for override
		#-- 8< --- ここから書き換え --- 8< --
		data = self.oslist[id].getData()
		#-- 8< --- ここまで書き換え --- 8< --
		return data

	def _getData(self, id=None):
		ldprint('--> ion.module._getData()')
		if (len(self.oslist) == 0):
			ldprint('<-- ion.module._getData()')
			return None
		if (id is None):
			id = self.oslist_id
		if (id is None):  # id is None or self.oslist_id is None
			id = 0
		ldprint('list ID: {}'.format(id))
		if (id < 0 or id > len(self.oslist) - 1):
			ldprint('<-- ion.module._getData()')
			return None
		data = self.getData(id)
		ldprint('data: {}'.format(data))
		ldprint('<-- ion.module._getData()')
		return data

	@property
	def data(self):
		return self._getData()

	def getOutputSemanticsList(self):
		return self._output_semlist

	def setOutputSemanticsList(self, l):
		self._output_semlist = l

	@property
	def output_semanticslist(self):
		return self.getOutputSemanticsList()

	@output_semanticslist.setter
	def output_semanticslist(self, l):
		self.setOutputSemanticsList(l)

	@property
	def output_slist(self):
		return self.output_semanticslist

	@output_slist.setter
	def output_slist(self, l):
		self.output_semanticslist = l

	@property
	def oslist(self):
		return self.output_semanticslist

	@oslist.setter
	def oslist(self, l):
		self.output_semanticslist = l

	def getOutputSemanticsListID(self):
		return self._output_semlist_id

	def setOutputSemanticsListID(self, id):
		self._output_semlist_id = id

	@property
	def output_semanticslist_id(self):
		return self.getOutputSemanticsListID()

	@output_semanticslist_id.setter
	def output_semanticslist_id(self, id):
		self.setOutputSemanticsListID(id)

	@property
	def output_slist_id(self):
		return self.output_semanticslist_id

	@output_slist_id.setter
	def output_slist_id(self, id):
		self.output_semanticslist_id = id

	@property
	def oslist_id(self):
		return self.output_semanticslist_id

	@oslist_id.setter
	def oslist_id(self, id):
		self.output_semanticslist_id = id

	def getOutputSemanticsID(self):
		return self.getOutputSemanticsListID()

	def setOutputSemanticsID(self, id):
		self.setOutputSemanticsListID(id)

	@property
	def output_semantics_id(self):
		return self.getOutputSemanticsID()

	@output_semantics_id.setter
	def output_semantics_id(self, id):
		self.setOutputSemanticsID(id)

	@property
	def output_sid(self):
		return self.output_semantics_id

	@output_sid.setter
	def output_sid(self, id):
		self.output_semantics_id = id

	@property
	def osid(self):
		return self.output_semantics_id

	@osid.setter
	def osid(self, id):
		self.output_semantics_id = id

	def getSemanticsList(self):
		return self.getOutputSemanticsList()

	def setSemanticsList(self, l):
		self.setOutputSemanticsList(l)

	@property
	def semanticslist(self):
		return self.getSemanticsList()

	@semanticslist.setter
	def semanticslist(self, l):
		self.setSemanticsList(l)

	@property
	def semlist(self):
		return self.semanticslist

	@semlist.setter
	def semlist(self, l):
		self.semanticslist = l

	@property
	def slist(self):
		return self.semanticslist

	@slist.setter
	def slist(self, l):
		self.semanticslist = l

	def getOutputSemantics(self, id=None):
		if (self.islist is None):
			return None
		if (len(self.islist) == 0):
			return None
		if (id is None):
			id = self.oslist_id
		if (id is None):  # id is None or self.oslist_id is None
			id = 0
		return self.oslist.getSemantics(id)

	@property
	def output_semantics(self):
		return self.getOutputSemantics()

	@property
	def output_s(self):
		return self.output_semantics

	@property
	def os(self):
		return self.output_semantics

	def getSemantics(self):
		return self.getOutputSemantics()

	@property
	def semantics(self):
		return self.getSemantics()

	@property
	def sem(self):
		return self.semantics

	@property
	def s(self):
		return self.semantics

	def getOutputQuery(self, id=None):
		return self.getOutputSemantics(id).getQuery()

	@property
	def output_query(self):
		return self.getOutputQuery()

	@property
	def oq(self):
		return self.output_query

	def getQuery(self, id=None):
		return self.getOutputQuery(id)

	@property
	def query(self):
		return self.getQuery()

	@property
	def q(self):
		return self.query


# data module

class data_module(module):
	_classname = 'ion.data_module'

	def __init__(self):
		super().__init__()
		self._osemlist = None

	@classmethod
	def getClassName(cls):
		return cls._classname

	def getData(self, id=None):  # for override
		ldprint('--> ion.module.getData()')
		if (id < 0 or id > len(self.oslist) - 1):
			ldprint('<-- ion.module.getData()')
			return None
		#-- 8< --- ここから書き換え --- 8< --
		#
		data = self.oslist[id].getData()
		#-- 8< --- ここまで書き換え --- 8< --
		ldprint('data: {}'.format(data))
		ldprint('<-- ion.module.getData()')
		return data

class datamodule(data_module):
	pass

class datmodule(data_module):
	pass

class dmodule(data_module):
	pass


# algorithm module

class algorithm_module(module):
	_classname = 'ion.algorithm_module'

	def __init__(self):
		super().__init__()
		self.input_semlist = semantics_list()

	@classmethod
	def getClassName(cls):
		return cls._classname

	def developQuery(self, query):  # for override
		if (self.islist is None):
			return False
		if (len(self.islist) == 0):
			return False
		for isem in self.islist:
			#-- 8< --- ここから書き換え --- 8< --
			#
			# ここで、self.output_semantics あるいは self.output_query を参照しながら、各 input semantics, isem を（必要があれば）更新する。
			#
			pass
			#-- 8< --- ここまで書き換え --- 8< --

	def develop(self, query):
		return developQuery(query)

	def query_development(self, query):
		return developQuery(query)

	def getInputSemanticsList(self):
		return self._input_semlist

	def setInputSemanticsList(self, l):
		self._input_semlist = l

	@property
	def input_semanticslist(self):
		return self.getInputSemanticsList()

	@input_semanticslist.setter
	def input_semanticslist(self, l):
		self.setInputSemanticsList(l)

	@property
	def input_semlist(self):
		return self.input_semanticslist

	@input_semlist.setter
	def input_semlist(self, l):
		self.input_semanticslist = l

	@property
	def input_slist(self):
		return self.input_semanticslist

	@input_slist.setter
	def input_slist(self, l):
		self.input_semanticslist = l

	@property
	def islist(self):
		return self.input_semanticslist

	@islist.setter
	def islist(self, l):
		self.input_semanticslist = l

	def getInputSemantics(self, id=None):
		return self.islist.getSemantics(id)

	@property
	def input_semantics(self):
		return self.getInputSemantics()

	@property
	def input_s(self):
		return self.input_semantics

	@property
	def is(self):
		return self.input_semantics

	def getInputQuery(self, id=None):
		if (self.islist is None):
			return None
		if (len(self.islist) == 0):
			return None
		if (id is None):
			id = 0
		return self.getInputSemantics(id).getQuery()

	@property
	def input_query(self):
		return self.getInputQuery()

	@property
	def iq(self):
		return self.input_query

class algorithmmodule(algorithm_module):
	pass

class algmodule(algorithm_module):
	pass

class amodule(algorithm_module):
	pass


#-- main

if __name__ == '__main__':
	import nkj as n
	import ion

	if (False):
		print('\n-- listex test')
		lx = n.listex()
		lx.print('list')
		print(lx.datastr)

		print('\n-- listex test')
		lx = n.listex('test')
		lx.print('list')
		print(lx.datastr)

		print('')
		lx = n.listex(['test', 'test2', 3])
		lx.print('list')
		print(lx)
		print(lx.datastr)

		print('')
		lx = n.listex(('test', 'test2', 3))
		lx.print('list')
		print(lx)
		print(lx.datastr)

		print('')
		lx = n.listex({0:'test', 1:'test2', 2:3})
		lx.print('list')
		print(lx)
		print(lx.datastr)

		print('')
		lx = n.listex([{0:'test', 1:'test2'}, {2:3}])
		lx.print('list')
		print(lx)
		print(lx.datastr)
		print(lx.c(0))
		print(lx.c(1))
		lx.c(1, {4:5})
		print(lx.c(1))

	if (False):
		print('\n-- ion.semantics_list')
		sl = semantics_list()
		print('component class: {}'.format(sl.componentclass))

	if (True):
		print('\n-- ion.module test')

		dm = data_module()
		dm.slist.print('semantics list')

		print('')
		s = ion.semantics()
		s.role = 'test_role'
		s.entity = 'test_entity'
		dm.slist.append(s)
		dm.slist.print('semantics list')
