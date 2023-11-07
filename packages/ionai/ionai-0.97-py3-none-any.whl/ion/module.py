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

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def search_data(query):  # for override
		return None

	def collateQuery(self, query):  # for override
		return True if (query <= self.query) else False

	def query_collation(self, query):
		return self.collateQuery(query)

	def getData(self):  # for override
		return None

	@property
	def data(self):
		return self.getData()

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
	def output_semlist(self):
		return self.output_semanticslist

	@output_semlist.setter
	def output_semlist(self, l):
		self.output_semanticslist = l

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

	def getOutputSemanticsID(self):
		return self.oslist.id

	def setOutputSemanticsID(self, id):
		self.oslist.id = id

	@property
	def oslistid(self):
		return self.getOutputSemanticsID()

	@oslistid.setter
	def oslistid(self, id):
		self.setOutputSemanticsID(id)

	def getOutputSemantics(self, id=None):
		return self.oslist.getSemantics(id)

	@property
	def output_semantics(self):
		return self.getOutputSemantics()

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
		pass

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
