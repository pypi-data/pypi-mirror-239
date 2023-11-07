#
# [name] nkj.ncore.py
# [exec] python -m nkj.ncore
#
# Written by Yoshikazu NAKAJIMA
#
import os
import sys
import platform

sys.path.append(os.path.abspath(".."))
import nkj.str as ns
from nkj.str import *

#-- global constants/variables

__ROOTPATH = None


#-- global functions

def rootpath(rootpath=None):
	global __ROOTPATH
	if (rootpath is None):
		if (__ROOTPATH == None):
			__ROOTPATH = os.getenv('NKJ_ROOT')
		return __ROOTPATH
	else:
		__ROOTPATH = rootpath
		return True

def getPythonVersion():
	major = sys.version_info.major
	minor = sys.version_info.minor
	return major, minor

def checkPythonVersion():
	dprint(["--> checkPythonVersion()"])
	vermajor, verminor = getPythonVersion()
	ldprint(["python version: ", str(vermajor), ".", str(verminor)])
	if (vermajor < 3):
		print_error("python version is too old.")
		exit
	elif (vermajor == 3 and verminor < 6):
		print_error("python version is too old.")
		exit
	dprint(["<-- checkPythonVersion()"])

def is_iterable(l):
	print('{0} ({1})'.format(l, type(l)))
	try:
		for i in l:
			pass
	except:
		return False
	else:
		return True


#-- global initialization

# Append root path

if (rootpath() == None):
	rootpath(os.path.abspath(".."))

sys.path.append(rootpath())

# !Append root path


#-- class

DEFAULT_ID = 0

class listex(list):
	_classname = 'nkj.listex'

	def __new__(cls, second=None):
		if (second is None):
			self = super().__new__(cls)
		else:
			self = super().__new__(cls, cls._tolist(second))
		return self

	def __init__(self, second=None):
		if (second is None):
			super().__init__([])
		else:
			super().__init__(self._tolist(second))
		self.componentclass = None if (second is None) else self._tocompclass(self)
		ldprint2('component class: {}'.format(self.componentclass))

	def __str__(self):
		return self.str

	def get(self, id=None):
		return self.getList() if (id is None) else self.getComponent(id)

	def set(self, second):
		self = self._tolist(second)

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def getComponentClass(self):
		return self._componentclass

	def setComponentClass(self, c):
		self._componentclass = c

	@property
	def componentclass(self):
		return self.getComponentClass()

	@componentclass.setter
	def componentclass(self, c):
		self.setComponentClass(c)

	@property
	def compcls(self):
		return self.componentclass

	@compcls.setter
	def compcls(self, c):
		self.componentclass = c

	def resetComponentClass(self):
		self.componentclass = self._tocompclass(self)

	@classmethod
	def _tolist(cls, c):
		if (isinstance(c, list)):
			return copy.deepcopy(c)
		elif (isinstance(c, tuple)):
			return list(copy.deepcopy(c))
		else:
			return [copy.deepcopy(c)]

	def _tocompclass(self, c):
		if (c is None):
			return None
		elif (is_iterable(c)):
			c = list(c)
			if (len(c) == 0):
				return None
			cc = c[0].__class__
			for i in range(len(c)):
				if (cc is not c[i].__class__):
					return None
			return cc
		else:
			__ERROR__

	def getList(self):
		return self

	def setList(self, l):
		self = self._tolist(l)

	@property
	def list(self):
		return self.getList()

	@list.setter
	def list(self, l):
		self.setList(l)

	def getComponent(self, id):
		return self[id] if (id >= 0 and id < len(self)) else None

	def setComponent(self, id, c):
		if (id is None):
			self.append(c)
		else:
			self[id] = c

	def component(self, id, c=None):
		if (c is None):
			return self.getComponent(id)
		else:
			self.setComponent(id, c)
			return True

	def comp(self, id, c=None):
		return self.component(id, c)

	def c(self, id, c=None):
		return self.component(id, c)

	# string

	def getStr(self):
		return super().__str__()

	@property
	def str(self):
		return self.getStr()

	def getDataStr(self):
		s = ''
		for i in range(len(self)):
			if (i > 0):
				s += ', '
			s += '\'{}\''.format(self[i]) if (isinstance(self[i], str)) else '{}'.format(self[i])
		return s

	def setDataStr(self, s):
		l = list(s.replace('(', '').replace(')', '').split(','))
		self.setList(l)

	@property
	def datastr(self):
		return self.getDataStr()

	@datastr.setter
	def datastr(self, s):
		self.setDataStr(s)

	# print

	def getPrintString(self, title=None):
		s = ''
		if (title is not None):
			s += '-- {0}[{1}] --\n'.format(title, len(self))
		for i in range(len(self)):
			if (i > 0):
				s += '\n'
			s += '\'{}\''.format(self[i]) if (isinstance(self[i], str)) else '{}'.format(self[i])
		if (title is not None):
			if (len(self) != 0):
				s += '\n'
			s += '--'.format(title)
		return s

	@property
	def printstr(self):
		return self.getPrintString()

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)

	# load, save

	def load(self, filename):
		with open(filename, 'r') as f:
			self.setDataStr(f.read())

	def save(self, filename):
		with open(filename, 'w') as f:
			f.write(self.getDataStr())


#-- main

if __name__ == '__main__':
	import json
	import nkj as n

	_DEBUGLEVEL = 2

	#ns.debuglevel(_DEBUGLEVEL)
	dprint(["ROOTPATH: ", rootpath()])
	checkPythonVersion()

	exl = n.exlist()
