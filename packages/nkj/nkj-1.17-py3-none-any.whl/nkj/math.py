#
# [name] nkj.math.py
# [exec] python -m nkj.math
#
# Written by Yoshikazu NAKAJIMA
#
_LIB_DEBUGLEVEL = 0

import os
import sys
import numpy as np
import math
from scipy.spatial.transform import Rotation as R
import copy
import numbers
from functools import singledispatch

sys.path.append(os.path.abspath(".."))
from .str import *
import nkj.prob as p

#-- flags

ENABLE_MULOPERATOR_FOR_GEOMETRYCOMPUTATION = False
ENABLE_MULOPERATOR_FOR_CSTRANS3D_CLASS = ENABLE_MULOPERATOR_FOR_GEOMETRYCOMPUTATION
ENABLE_MULOPERATOR_FOR_MAT4X4_CLASS = ENABLE_MULOPERATOR_FOR_GEOMETRYCOMPUTATION
ENABLE_MULOPERATOR_FOR_POINT3D_CLASS = ENABLE_MULOPERATOR_FOR_GEOMETRYCOMPUTATION
ENABLE_MULOPERATOR_FOR_LINE3D_CLASS = ENABLE_MULOPERATOR_FOR_GEOMETRYCOMPUTATION
ENABLE_MULOPERATOR_FOR_PLANE3D_CLASS = ENABLE_MULOPERATOR_FOR_GEOMETRYCOMPUTATION

#-- global functions

def arange2(x, y, step=None):
	if (step == None):
		return np.arange(x, y + 1)
	else:
		return np.arange(x, y + step, step)

def is_scalar(x):
	return isinstance(x, numbers.Number)

def is_geometric_primitive(x):
	ty = type(x)
	flag = False
	for object in [point3d, line3d, plane3d]:
		flag |= ty is object
	return flag

def is_geometric(x):
	return is_geometric_primitive(x)

def ndim(x):
	return np.ndim(x)

def shape(x):
	return np.shape(x)

def sq(x):
	return x * x

def sqrt(x):
	return np.sqrt(x)

def rad2deg(x):
	if (isinstance(x, list) or isinstance(x, tuple)):
		l = []
		for i in range(len(x)):
			l.append(rad2deg(x[i]))
		return l
	else:
		#return (x * 180.0 / np.pi)
		return math.degrees(x)

def deg2rad(x):
	if (isinstance(x, list) or isinstance(x, tuple)):
		l = []
		for i in range(len(deglist)):
			l.append(deg2rad(deglist[i]))
		return l
	else:
		#return (x * np.pi / 180.0)
		return math.radians(x)

"""
def rad2deg4list(radlist):
	deglist = []
	for i in range(len(radlist)):
		deglist.append(rad2deg(radlist[i]))
	return deglist

def deg2rad4list(deglist):
	radlist = []
	for i in range(len(deglist)):
		radlist.append(deg2rad(deglist[i]))
	return radlist
"""

def sigmoid(x, tau=1.0, x0=0.0):
	return 1.0 / (1.0 + np.exp(-(x - x0) / tau))

def vecnorm(v):
	if (isinstance(v, np.ndarray)):
		v = np.array(v)
	return np.linalg.norm(v)

def norm(x):
	if (isinstance(x, np.ndarray)):
		if (x.ndim == 1):
			return vecnorm(x)
		else:
			___ERROR___
	else:
		___ERROR___

def vecnormalize(v):
	if (isinstance(v, list) or isinstance(v, tuple)):
		v = np.array(v)
	vlen = vecnorm(v)
	if (vlen != 0):
		v = v / vlen   # np.array の要素に対して、v /= vlen はできない
	if (isinstance(v, np.ndarray)):
		pass
	elif (isinstance(v, list)):
		v = [v[0], v[1], v[2]]
	elif (isinstance(v, tuple)):
		v = (v[0], v[1], v[2])
	return v

def normalize(x):
	if (isinstance(x, np.ndarray)):
		if (x.ndim == 1):
			return vecnormalize(x)
		else:
			___ERROR___
	else:
		___ERROR___

def vecangle(basev, v):
	u = basev
	nu = vecnorm(u)
	nv = vecnorm(v)
	if (nu == 0.0):
		return 0.0
	if (nv == 0.0):
		return 0.0
	u = u / nu # normalize
	v = v / nv # normalize
	c = np.inner(u, v)
	s = np.linalg.norm(np.cross(u, v)) # np.cross() は、ベクトルが両方とも2次元の場合はスカラー返すが、3次元の場合は3次元ベクトルを返す。
	return np.arctan2(s, c)

"""
def angle_(base, target):
	if (base is None or target is None):
		___ERROR___
	if (isinstance(base, list) or isinstance(base, tuple)):
		base = np.array(base)
	if (isinstance(target, list) or isinstance(target, tuple)):
		target = np.array(target)
	if (isinstance(base, np.ndarray) and isinstance(target, np.ndarray)):
		return vecangle(base, target)
	elif (isinstance(base, vec3d) and isinstance(target, vec3d)):
		return vecangle(base.get(), target.get())
	elif (isinstance(base, line3d) and isinstance(target, line3d)):
		return vecangle(base.getVector(), target.getVector())
	elif (isinstance(base, plane3d) and isinstance(target, plane3d)):
		return vecangle(base.getNormal(), target.getNormal())
	elif (isinstance(base, plane3d) and isinstance(target, line3d)):
		return np.pi / 2.0 - vecangle(base.getNormal(), target.getVector())
	elif (isinstance(base, line3d) and isinstance(target, plane3d)):
		return np.pi / 2.0 - vecangle(base.getVector(), target.getNormal())
	else:
		___ERROR___
"""

def normalized(x):
	return x.normalized()

def inversed(x):
	return x.inversed()

def transposed(x):
	return x.transposed()

def conjugated(x):
	return x.conjugated()

def decimal_unit(x):
	if (x == 0.0):
		return 0.0
	elif (x > 0.0):
		sign = 1.0
	else:
		sign = -1.0
		x = -x
	unit = 1.0
	if (x > 1.0):
		while (unit < x):
			unit *= 10.0
		if (unit > x):
			unit /= 10.0
	else: # 0.0 < x < 1.0
		while (unit > x):
			unit /= 10.0
	return sign * unit

def logticks(min, max, ticks=10):
	ldprint2(["--> logticks({0}, {1}, {2})".format(min, max, ticks)])
	if (min < 0.0 or max < 0.0):
		print_error("Illegal arguments.")
		return None
	if (min > max):
		print_error("Illegal arguments.")
		return None
	if (ticks < 0):
		print_error("Illegal ticks.")
		return None
	tick_interval = 1.0 / float(ticks)
	ldprint3(["Tick interval: {0}".format(tick_interval)])
	min_log10 = np.log10(min)
	max_log10 = np.log10(max)
	unit_min_log10 = int(np.ceil(min_log10 * ticks))
	unit_max_log10 = int(np.floor(max_log10 * ticks))
	ldprint3(["min: {0} -> log10(min): {1} -> {2}".format(min, min_log10, unit_min_log10)])
	ldprint3(["max: {0} -> log10(max): {1} -> {2}".format(max, max_log10, unit_max_log10)])
	xlist = []
	if (min_log10 * ticks < unit_min_log10):
		xlist.append(min)
	for unit_tick_log10 in range(unit_min_log10, unit_max_log10 + 1):
		tick_log10 = unit_tick_log10 * tick_interval
		ldprint3(["Tick_log10: {0}".format(tick_log10)])
		tick = np.power(10.0, tick_log10)
		xlist.append(tick)
	if (max_log10 * ticks > unit_max_log10):
		xlist.append(max)
	ldprint(["xlist: ", xlist])
	ldprint2(["<-- logticks()"])
	return xlist

def pseudo_logticks(min, max, tick_scale=1.0):
	ldprint2(["--> pseudo_logticks({0}, {1}, {2})".format(min, max, tick_scale)])
	if (min < 0.0 or max < 0.0):
		print_error("Illegal arguments.")
		return None
	if (min > max):
		print_error("Illegal arguments.")
		return None
	if (tick_scale <= 0.0 or tick_scale > 1.0):
		print_error("Illegal tick scale.")
		return None
	min_unit = decimal_unit(min)
	max_unit = decimal_unit(max)
	if (max_unit < max):
		max_unit *= 10.0
	ldprint3(["unit: ", min, " -> ", min_unit])
	ldprint3(["unit: ", max, " -> ", max_unit])
	min_log10 = int(np.log10(min_unit))
	max_log10 = int(np.log10(max_unit))
	ldprint3(["log10: ", min_unit, " -> ", min_log10])
	ldprint3(["log10: ", max_unit, " -> ", max_log10])
	xlist = []
	for i in range(min_log10, max_log10):
		ldprint3(["log10: ", i])
		unit = np.power(10.0, i)
		ldprint3(["unit: ", unit])
		j_max = int(10.0 / tick_scale)
		for j in range(1, j_max):
			val = unit * tick_scale * j
			if (val < min):
				hval = unit * tick_scale * (j + 1)
				if (min < hval):
					xlist.append(min)
			elif (val < max):
				xlist.append(val)
			else:
				xlist.append(max)
				break
		if (val < max and max <= np.power(10.0, i + 1)):
			list.append(max)
	"""
	xlist = list(set(xlist))
	xlist = xlist.sort()
	"""
	ldprint2(["xlist: ", xlist])
	ldprint2(["<-- pseudo_logticks()"])
	return xlist

def _mat_4x4to3x3(m4):
	if (isinstance(m4, rot3d)):
		m = m4.getMatrix()
	elif (isinstance(m4, np.ndarray)):
		return np.array([[m4[0, 0], m4[0, 1], m4[0, 2]],
		                 [m4[1, 0], m4[1, 1], m4[1, 2]],
		                 [m4[2, 0], m4[2, 1], m4[2, 2]]])
	elif (isinstance(m4, list)):
		return [[m4[0, 0], m4[0, 1], m4[0, 2]],
		        [m4[1, 0], m4[1, 1], m4[1, 2]],
		        [m4[2, 0], m4[2, 1], m4[2, 2]]]
	elif (isinstance(m4, tuple)):
		return ((m4[0, 0], m4[0, 1], m4[0, 2]),
		        (m4[1, 0], m4[1, 1], m4[1, 2]),
		        (m4[2, 0], m4[2, 1], m4[2, 2]))
	else:
		___ERROR___

def _mat_3x3to4x4(m3):
	if (isinstance(m3, rot3d)):
		m = m3.getMatx3x3()
	elif (isinstance(m3, np.ndarray)):
		m = np.array([[m3[0, 0], m3[0, 1], m3[0, 2], 0.0],
		              [m3[1, 0], m3[1, 1], m3[1, 2], 0.0],
		              [m3[2, 0], m3[2, 1], m3[2, 2], 0.0],
		              [0.0, 0.0, 0.0, 1.0]])
	elif (isinstance(m3, list)):
		m = [[m3[0, 0], m3[0, 1], m3[0, 2], 0.0],
		     [m3[1, 0], m3[1, 1], m3[1, 2], 0.0],
		     [m3[2, 0], m3[2, 1], m3[2, 2], 0.0],
		     [0.0, 0.0, 0.0, 1.0]]
	elif (isinstance(m3, tuple)):
		m = ((m3[0, 0], m3[0, 1], m3[0, 2], 0.0),
		     (m3[1, 0], m3[1, 1], m3[1, 2], 0.0),
		     (m3[2, 0], m3[2, 1], m3[2, 2], 0.0),
		     (0.0, 0.0, 0.0, 1.0))
	else:
		___ERROR___
	return m

def to3x3(m4):
	return _mat_4x4to3x3(m4)

def to4x4(m3):
	return _mat_3x3to4x4(m3)

def tovec3(v):
	return v[0:3]

def tovec4(v):
	dprint2('--> nkj.math.tovec4')
	dprint2('v: {0}'.format(v))
	if (len(v) == 3):
		if (isinstance(v, np.ndarray)):
			v = np.append(v, 1.0)
		elif (isinstance(v, list) or isinstance(v, tuple)):
			v = v.append(1.0)
		else:
			___ERROR___
	elif (len(v) == 4):
		if (isinstance(v, np.ndarray)):
			pass
		else:
			v = np.array(v)
	else:
		___ERROR___
	dprint2('v: {0}'.format(v))
	dprint2('<-- nkj.math.tovec4')
	return v

def vec3(v):
	return tovec3(v)

def vec4(v):
	return tovec4(v)

def offsetTransform(r, base):
	if (type(r) is np.ndarray):
		r = to4x4(r)
	else:
		return base @ r @ base.inv

def offset_transform(r, base):
	return offsetTransformation(r, base)

def offset(a, base):
	ty = type(a)
	if (ty is np.ndarray):
		sh = a.shape
		if (sh == (4, 4) or sh == (3, 4)):
			return offsetTransformation(a, base)
		else:
			___ERROR___
	elif (ty is list or ty is tuple):
		sh = shape(a)
		___NOT_IMPLEMENTED___
	elif (ty is trans3d):
		return offsetTransformation(a, base)
	else:
		___ERROR___


#-- classes -----------------------------------------------

#-------- ここからコメントアウト -----------------------
"""
# python complex を使うこと
#-- complex

_DEFAULT_RE = 0.0
_DEFAULT_IM = 0.0
_DEFAULT_C = (_DEFAULT_RE, _DEFAULT_IM)

class complex():
	_classname = 'nkj.math.complex'

	def __init__(self, c=None):
		if (c is None):
			self.set()
		else:
			self.set(c)

	def __str__(self):
		return self.getStr()

	def __not__(self):
		return complex(self.re, -self.im)

	def __add__(self, second):
		return complex(self.re + second.re, self.im + second.im)

	def __sub__(self, second):
		return complex(self.re - second.re, self.im - second.im)

	def __mul__(self, second): # 複素共役を掛け算
		ldprint(["self:   ", str(self)])
		ldprint(["second: ", str(second)])
		return self.re * second.re + self.im * second.im

	def __inv__(self): # '~'
		return self.normalized()

	def __getitem__(self, i):
		if (i == 0):
			return self.getRe()
		elif (i == 1):
			return self.getIm()
		else:
			return ValueError

	def __setitem__(self, i, second):
		if (i == 0):
			self.setRe(second)
		elif (i == 1):
			self.setIm(second)
		else:
			None

	# classname

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	# get, set

	def get(self):
		return self.getComplex()

	def set(self, c=None):
		if (c is None):
			self.setComplex()
		else:
			self.setComplex(c)

	def getReal(self):
		return self._re

	def setReal(self, re):
		self._re = re

	def getRe(self):
		return self.getReal()

	def setRe(self, re):
		self.setReal(re)

	def getR(self):
		return self.getReal()

	def setR(self, re):
		self.setReal(re)

	@property
	def real(self):
		return self.getReal()

	@real.setter
	def real(self, re):
		self.setReal(re)

	@property
	def re(self):
		return self.getReal()

	@re.setter
	def re(self, re_):
		self.setReal(re_)

	@property
	def r(self):
		return self.getReal()

	@r.setter
	def r(self, re):
		self.setReal(re)

	def getImaginary(self):
		return self._im

	def setImaginary(self, im):
		self._im = im

	def getIm(self):
		return self.getImaginary()

	def setIm(self, im):
		self.setImaginary(im)

	def getI(self):
		return self.getImaginary()

	def setI(self, im):
		self.setImaginary(im)

	@property
	def imaginary(self):
		return self.getImaginary()

	@imaginary.setter
	def imaginary(self, im):
		self.setImaginary(im)

	@property
	def im(self):
		return self.getImaginary()

	@im.setter
	def im(self, im_):
		self.setImaginary(im_)

	@property
	def i(self):
		return self.getImaginary()

	@i.setter
	def i(self, im):
		self.setImaginary(im)

	def getComplex(self):
		return self

	def setComplex(self, c=None):
		if (c is None):
			self.setComplex(_DEFAULT_C)
		elif (isinstance(c, complex)):
			self.setRe(c.re)
			self.setIm(c.im)
		elif (isinstance(c, list) or isinstance(c, tuple)):
			self.setRe(c[0])
			self.setIm(c[1])
		else:
			__ERROR__

	@property
	def complex(self):
		return self.getComplex()

	@complex.setter
	def complex(self, c):
		self.setComplex(c)

	@property
	def val(self):
		return self.getComplex()

	@val.setter
	def val(self, c):
		self.setComplex(c)

	# conjugate

	@property
	def conjugated(self):
		return complex(self.re, -self.im)

	@property
	def conj(self):
		return self.conjugated

	# norm

	@property
	def norm(self):
		return sqrt(sq(self.re) + sq(self.im))

	@property
	def normalized(self):
		norm = self.norm
		if (norm == 0.0):
			return ValueError
		else:
			return complex(self.re / norm, self.im / norm)

	@property
	def phase(self): # 戻り値の範囲は [-pi, pi]
		return np.arctan2(self.im, self.re)

	# string

	def getStr(self):
		return '{0:.6f}{1:+.6f}j'.format(self.re, self.im)

	@property
	def str(self):
		return self.getStr()

	def getDataStr(self):
		return '{0:.12f}, {1:.12f}'.format(self.re, self.im)

	def setDataStr(self, s):
		sl = s.replace('(', '').replace(')', '').split(',')
		if (len(sl) != 2):
			__ERROR__
		d = list(map(float, sl))
		self.re = d[0]
		self.im = d[1]

	@property
	def datastr(self):
		return self.getDataStr()

	@datastr.setter
	def datastr(self, s):
		self.setDataStr(s)

	def getPrintStr(self, title=None):
		s = ''
		if (title is not None):
			s += '-- {} --\n'.format(title)
		s += self.getStr()
		if (title is not None):
			s += '\n--'
		return s

	@property
	def printstr(self):
		return self.getPrintStr()

	def print(self, title=None):
		print(self.getPrintStr(title), flush=True)

	def load(self, filename):
		with open(filename, 'r') as f:
			self.setDataStr(f.read())

	def save(self, filename):
		with open(filename, 'w') as f:
			f.write(self.getDataStr())
"""
#-------- ここまでコメントアウト -----------------------


#-- angle

_DEFAULT_ANGLE = 0.0   # degree

class angle_cls():
	_classname = 'nkj.math.angle'

	def __init__(self, r=None):
		ldprint('--> nkj.math.angle._init_()')
		if (r is None):
			self.set()
		else:
			self.set(r)
		ldprint2('val: {0} [rad] ({1} [deg])'.format(self.getRad(), self.getDeg()))
		ldprint('<-- nkj.math.angle._init_()')

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	# get, set

	def get(self):
		return self.getAngle()

	def set(self, r=None):
		if (r is None):
			self.setDeg(_DEFAULT_ANGLE)
		elif (isinstance(r, float)):
			self.setAngle(r)
		else:
			__ERROR__

	# angle

	def getAngle(self):
		return self.getRad()

	def setAngle(self, r):
		self.setRad(r)

	def getRad(self):
		return self._r

	def setRad(self, r):
		self._r = r

	@property
	def rad(self):
		return self.getRad()

	@rad.setter
	def rad(self, a):
		self.setRad(a)

	def getDeg(self):
		return rad2deg(self.getRad())

	def setDeg(self, a):
		self.setRad(deg2rad(a))

	@property
	def deg(self):
		return self.getDeg()

	@deg.setter
	def deg(self, a):
		self.setDeg(a)

	# cos, sin

	@property
	def cos(self):
		return np.cos(self.getRad())

	@property
	def sin(self):
		return np.sin(self.getRad())

	@property
	def c(self):
		return self.cos

	@property
	def s(self):
		return self.sin

	# string

	def getStr(self):
		return '{:.12f}'.format(self.getDeg())

	def setStr(self, s):
		self.setDeg(float(s))

	@property
	def str(self):
		return self.getStr()

	@str.setter
	def str(self, s):
		self.setStr(s)

	def getDataStr(self):
		return '{:.12f}'.format(self.getDeg())

	@property
	def datastr(self):
		return self.getDataStr()

	# print

	def getPrintString(self, title=None):
		s = ''
		if (title is not None):
			s += '{}: '.format(title)
		s += '{0:.6f} deg ({1:.6f} rad)'.format(self.getDeg(), self.getRad())
		if (title is not None):
			s += '\n'
		return s

	def getPrintStr(self, title=None):
		return self.getPrintString(title)

	@property
	def printstr(self):
		return self.getPrintStr()

	@property
	def pstr(self):
		return self.getPrintStr()

	def print(self, title=None):
		print(self.getPrintStr(title), end='', flush=True)

	# load, save

	def load(self, filename):
		with open(filename, 'r') as f:
			self.setDataStr(f.read())

	def save(self, filename):
		with open(filename, 'w') as f:
			f.write(self.getDataStr())

class angle(angle_cls):
	pass


#-- array

class array_cls(np.ndarray):
	_classname = 'nkj.math.array_cls'

	def __new__(cls, shape, dtype='float32'):
		return super().__new__(cls, shape=shape, dtype=dtype)  # __new__() で必ずインスタンスを return すること．

	def __init__(self):
		super().__init__()

	def __str__(self):
		return self.getStr()

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def get(self):
		return self

	def set(self, a=None):
		ldprint('--> nkj.math.array.set()')
		ldprint2('type: {}'.format(type(a)))
		if (a is None):
			pass
		elif (isinstance(a, np.ndarray) or isinstance(a, array_cls) or
		      isinstance(a, vec_cls) or isinstance(a, vec2d) or isinstance(a, vec3d) or
		      isinstance(a, mat_cls) or isinstance(a, mat2x2) or isinstance(a, mat3x3) or isinstance(a, mat4x4) or
		      isinstance(a, mat2x3) or isinstance(a, mat3x4)):
			self.setArray(a)
		elif (isinstance(a, list) or isinstance(a, tuple)):
			self.setList(a)
		elif (isinstance(a, string)):
			self.setStr(a)
		else:
			__ERROR__
		ldprint('<-- nkj.math.array.set()')

	def getStr(self):
		rows, columns = self.shape
		s = ''
		for j in range(rows):
			for i in range(columns):
				if (i != 0 or j != 0):
					s += ', '
				s += '{}'.format(self[j, i])
		return s

	def setStr(self, s:str):
		ldprint('--> nkj.math.array.setStr()')
		ldprint2(s)
		ldprint2(s.split(','))
		l = list(map(float, s.split(',')))
		print(l)
		if (len(l) != self.size):
			__ERROR__
		ii = 0
		rows, columns = self.shape
		for j in range(rows):
			for i in range(columns):
				self[j, i] = l[ii]
				ii += 1
		ldprint('<-- nkj.math.array.setStr()')

	@property
	def str(self):
		return self.getStr()

	@str.setter
	def str(self, s):
		self.setStr(s)

	def getDataStr(self):
		rows, columns = self.shape
		s = ''
		for j in range(rows):
			for i in range(columns):
				if (i != 0 or j != 0):
					s += ', '
				s += '{:.12f}'.format(self[j, i])
		return s

	def setDataStr(self, s):
		ldprint('--> nkj.math.array.setDataStr()')
		ldprint('datastr: {}'.format(s))
		rows, columns = self.shape
		data = list(map(float, s.replace('(', '').replace(')', '').split(',')))
		ldprint('list[{0}]: {1}'.format(len(data), data))
		ii = 0
		for j in range(rows):
			for i in range(columns):
				self[j, i] = data[ii]
				ii += 1
		ldprint('<-- nkj.math.array.setDataStr()')

	@property
	def datastr(self):
		return self.getDataStr()

	@datastr.setter
	def datastr(self, s):
		self.setDataStr(s)

	def getArray(self):
		return np.array(self)

	def setArray(self, a):
		a = np.array(a)
		rows, columns = a.shape
		for j in range(rows):
			for i in range(columns):
				self[j, i] = a[j, i]

	@property
	def array(self):
		return self.getArray()

	@array.setter
	def array(self, a):
		self.setArray(a)

	@property
	def arr(self):
		return self.array

	@arr.setter
	def arr(self, a):
		self.array = a

	def getList(self):
		return list(self)

	def setList(self, l):
		ldprint('--> nkj.math.array.setList()')
		ldprint2('type: {0}'.format(type(l)))
		if (not isinstance(l, list) and not isinstance(l, tuple)):
			__ERROR__
		ndim = self.ndim
		rows, columns = self.shape
		ldprint2('row, columns: {0}, {1}'.format(rows, columns))
		ldprint2('list: {}'.format(l))
		if (columns == 1):
			for j in range(rows):
				self[j, 0] = l[j]
		else:
			for j in range(rows):
				for i in range(columns):
					ldprint2('(j, i): {0}, {1}'.format(j, i))
					ldprint2('l[{0}][{1}]: {2}'.format(j, i, l[j][i]))
					self[j, i] = l[j][i]
		ldprint('<-- nkj.math.array.setList()')

	@property
	def list(self):
		return self.getList()

	@list.setter
	def list(self, l):
		self.setList(l)

	def getPrintString(self, title=None):
		s = ''
		if (title is not None):
			s += '--- {} ---\n'.format(title)
		rows, columns = self.shape
		for j in range(rows):
			for i in range(columns):
				if (i != 0):
					s += ', '
				s += '{0:16.12f}'.format(self[j, i])
			if (j < rows - 1):
				s += '\n'
		if (title is not None):
			s += '\n---'
		return s

	def getPrintStr(self, title=None):
		return self.getPrintString(title)

	@property
	def printstr(self):
		return self.getPrintStr()

	@property
	def pstr(self):
		return self.getPrintStr()

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)

	# load, save

	def load(self, filename):
		with open(filename, 'r') as f:
			self.setDataStr(f.read())

	def save(self, filename):
		with open(filename, 'w') as f:
			f.write(self.getDataStr())

class array(array_cls):
	pass


#-- vector

class vec_cls(array_cls):
	_classname = 'nkj.math.vec'

	@classmethod
	def getClassName(cls):
		return cls._classname

	@property
	def x(self):
		return self[0][0]

	@x.setter
	def x(self, x_):
		self[0][0] = x_

	@property
	def y(self):
		return self[1][0]

	@y.setter
	def y(self, y_):
		self[1][0] = y_

	@property
	def z(self):
		return self[2][0]

	@z.setter
	def z(self, z_):
		self[2][0] = z_

	@property
	def w(self):
		return self[3][0]

	@w.setter
	def w(self, w_):
		self[3][0] = w_

	def inverse(self):
		rows, columns = self.shape
		if (columns != 1):
			__ERROR__
		for i in range(rows):
			self[i] *= -1

	def getInversed(self):  # for override
		return None

	@property
	def inversed(self):
		return self.getInversed()

	@property
	def inv(self):
		return self.inversed

	@property
	def i(self):
		return self.inversed

class vec(vec_cls):
	pass


_DEFAULT_VEC2D = [[0.0], [0.0]]
_DEFAULT_VEC3D = [[0.0], [0.0], [0.0]]
_DEFAULT_VEC4D = [[0.0], [0.0], [0.0], [0.0]]

class vec2d(vec_cls):
	_classname = 'nkj.math.vec2d'

	def __new__(cls, v=None):
		self = super().__new__(cls, shape=(2, 1), dtype='float32')  # 初期化するときは、生成したインスタンスを self に代入してインスタンス関数を呼び出す．
		self.set(_DEFAULT_VEC2D if (v is None) else self.set(v))
		return self  # 必ず、self を return すること

	def __init__(self, v=None):
		super().__init__()
		self.set(_DEFAULT_VEC2D if (v is None) else self.set(v))

	@classmethod
	def getClassName(cls):
		return cls._classname

	def getInversed(self):
		iv = copy.deepcopy(self)
		for i in range(2):
			iv[i][0] *= -1
		return iv

	def getHomogeneous(self):
		hv = vec3d()
		for i in range(2):
			hv[i, 0] = self[i, 0]
		hv[2, 0] = 1.0
		return hv

	def setHomogeneous(self, hv):
		for i in range(2):
			self[i, 0] = hv[i, 0]

	@property
	def homogeneous(self):
		return self.getHomogeneous()

	@homogeneous.setter
	def homogeneous(self, hv):
		self.setHomogeneous(hv)

	@property
	def hom(self):
		return self.homogeneous

	@hom.setter
	def hom(self, hv):
		self.homogeneous = hv

	@property
	def h(self):
		return self.homogeneous

	@h.setter
	def h(self, hv):
		self.homogeneous = hv

class vec2D(vec2d):
	pass


class vec3d(vec_cls):
	_classname = 'nkj.math.vec3d'

	def __new__(cls, v=None):
		self = super().__new__(cls, shape=(3, 1), dtype='float32')
		self.set(_DEFAULT_VEC3D if (v is None) else self.set(v))
		return self

	def __init__(self, v=None):
		super().__init__()
		self.set(_DEFAULT_VEC3D if (v is None) else self.set(v))

	@classmethod
	def getClassName(cls):
		return cls._classname

	def getInversed(self):
		iv = copy.deepcopy(self)
		for i in range(3):
			iv[i][0] *= -1
		return iv

	def getHomogeneous(self):
		hv = vec4d()
		for i in range(3):
			hv[i, 0] = self[i, 0]
		hv[3, 0] = 1.0
		return hv

	def setHomogeneous(self, hv):
		for i in range(3):
			self[i, 0] = hv[i, 0]

	@property
	def homogeneous(self):
		return self.getHomogeneous()

	@homogeneous.setter
	def homogeneous(self, hv):
		self.setHomogeneous(hv)

	@property
	def hom(self):
		return self.homogeneous

	@hom.setter
	def hom(self, hv):
		self.homogeneous = hv

	@property
	def h(self):
		return self.homogeneous

	@h.setter
	def h(self, hv):
		self.homogeneous = hv

	def getInhomogeneous(self):
		ihv = vec2d()
		for i in range(2):
			ihv[i, 0] = self[i, 0]
		return ihv

	def setInhomogeneous(self, hv):
		for i in range(2):
			self[i, 0] = hv[i, 0]
		self[2, 0] = 1.0

	@property
	def inhomogeneous(self):
		return self.getInhomogeneous()

	@inhomogeneous.setter
	def inhomogeneous(self, ihv):
		self.setInhomogeneous(ihv)

	@property
	def inhom(self):
		return self.inhomogeneous

	@inhom.setter
	def inhom(self, ihv):
		self.inhomogeneous = ihv

	@property
	def ih(self):
		return self.inhomogeneous

	@ih.setter
	def ih(self, hv):
		self.inhomogeneous = hv

class vec3D(vec3d):
	pass


class vec4d(vec_cls):
	_classname = 'nkj.math.vec4d'

	def __new__(cls, v=None):
		self = super().__new__(cls, shape=(4, 1), dtype='float32')
		self.set(_DEFAULT_VEC4D if (v is None) else self.set(v))
		return self

	def __init__(self, v=None):
		super().__init__()
		self.set(_DEFAULT_VEC4D if (v is None) else self.set(v))

	@classmethod
	def getClassName(cls):
		return cls._classname

	def getInversed(self):
		iv = copy.deepcopy(self)
		for i in range(4):
			iv[i][0] *= -1
		return iv

	def getInhomogeneous(self):
		ihv = vec3d()
		for i in range(3):
			ihv[i, 0] = self[i, 0]
		return ihv

	def setInhomogeneous(self, hv):
		for i in range(3):
			self[i, 0] = hv[i, 0]
		self[3, 0] = 1.0

	@property
	def inhomogeneous(self):
		return self.getInhomogeneous()

	@inhomogeneous.setter
	def inhomogeneous(self, ihv):
		self.setInhomogeneous(ihv)

	@property
	def inhom(self):
		return self.inhomogeneous

	@inhom.setter
	def inhom(self, ihv):
		self.inhomogeneous = ihv

	@property
	def ih(self):
		return self.inhomogeneous

	@ih.setter
	def ih(self, hv):
		self.inhomogeneous = hv

class vec4D(vec4d):
	pass


#-- matrix

class mat_cls(array_cls):
	_classname = 'nkj.math.mat'

	@classmethod
	def getClassName(cls):
		return cls._classname

	def getInversed(self):
		return np.linalg.inv(self)

	@property
	def inversed(self):
		return self.getInversed()

	@property
	def inv(self):
		return self.inversed

	@property
	def i(self):
		return self.inversed

	def inverse(self):
		self.set(self.getInversed())

class mat(mat_cls):
	pass


_DEFAULT_MAT2X2 = [[1.0, 0.0], [0.0, 1.0]]
_DEFAULT_MAT2X3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
_DEFAULT_MAT3X3 = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]
_DEFAULT_MAT3X4 = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0]]
_DEFAULT_MAT4X4 = [[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]

class mat2x2(mat_cls):
	_classname = 'nkj.math.mat2x2'

	def __new__(cls, m=None):
		self = super().__new__(cls, shape=(2, 2), dtype='float32')  # __new__() で必ずインスタンスを return すること．
		self.set(_DEFAULT_MAT2X2 if (m is None) else self.set(m))
		return self

	def __init__(self, m=None):
		super().__init__()
		self.set(_DEFAULT_MAT2X2 if (m is None) else self.set(m))

	@classmethod
	def getClassName(cls):
		return cls._classname

	def __matmul__(self, a):
		if (isinstance(a, mat2x2)):
			return mat2x2(np.array(self) @ np.array(a))
		else:
			ldprint0(np.array(self) @ np.array(a))
			ldprint0('class: {}'.format(a.__class__))
			return a.__class__(np.array(self) @ np.array(a))

	def __rmatmul__(self, a):
		if (isinstance(a, vec2d)):
			return vec2d(np.array(self) @ np.array(a))
		else:
			return mat2x2(np.array(a) @ np.array(self))

	def identity(self):
		return self.set(np.identity(2))


class mat2x3(mat_cls):
	_classname = 'nkj.math.mat2x3'

	def __new__(cls, m=None):
		self = super().__new__(cls, shape=(2, 3), dtype='float32')
		self.set(_DEFAULT_MAT2X3 if (m is None) else self.set(m))
		return self

	def __init__(self, m=None):
		super().__init__()
		self.set(_DEFAULT_MAT2X3 if (m is None) else self.set(m))

	@classmethod
	def getClassName(cls):
		return cls._classname

	def __matmul__(self, a):
		if (isinstance(a, vec2d)):
			return vec2d(np.array(self) @ np.array(a.hom))
		elif (isinstance(a, vec3d)):
			return vec2d(np.array(self) @ np.array(a)).hom
		else:
			return mat2x3(np.array(self) @ np.array(a))

	def __rmatmul__(self, a):
		if (isinstance(a, vec2d)):
			return vec2d(np.array(self) @ np.array(a.hom))
		elif (isinstance(a, vec3d)):
			return vec2d(np.array(self) @ np.array(a)).hom
		else:
			return mat2x3(np.array(a) @ np.array(self))

	def identity(self):
		return self.set(_DEFAULT_MAT2X3)


class mat3x3(mat_cls):
	_classname = 'nkj.math.mat3x3'

	def __new__(cls, m=None):
		self = super().__new__(cls, shape=(3, 3), dtype='float32')
		self.set(_DEFAULT_MAT3X3 if (m is None) else self.set(m))
		return self

	def __init__(self, m=None):
		super().__init__()
		self.set(_DEFAULT_MAT3X3 if (m is None) else self.set(m))

	@classmethod
	def getClassName(cls):
		return cls._classname

	def __matmul__(self, a):
		if (isinstance(a, vec3d)):
			return vec3d(np.array(self) @ np.array(a))
		else:
			return mat3x3(np.array(self) @ np.array(a))

	def __rmatmul__(self, a):
		if (isinstance(a, vec3d)):
			return vec3d(np.array(self) @ np.array(a))
		else:
			return mat3x3(np.array(a) @ np.array(self))

	def identity(self):
		return self.set(np.identity(3))


class mat3x4(mat_cls):
	_classname = 'nkj.math.mat3x4'

	def __new__(cls, m=None):
		self = super().__new__(cls, shape=(3, 4), dtype='float32')
		self.set(_DEFAULT_MAT3X4 if (m is None) else self.set(m))
		return self

	def __init__(self, m=None):
		super().__init__()
		self.set(_DEFAULT_MAT3X4 if (m is None) else self.set(m))

	@classmethod
	def getClassName(cls):
		return cls._classname

	def __matmul__(self, a):
		if (isinstance(a, vec3d)):
			return vec3d(np.array(self) @ np.array(a.hom))
		elif (isinstance(a, vec4d)):
			return vec3d(np.array(self) @ np.array(a)).hom
		else:
			return mat3x4(np.array(self) @ np.array(a))

	def __rmatmul__(self, a):
		if (isinstance(a, vec3d)):
			return vec3d(np.array(self) @ np.array(a.hom))
		elif (isinstance(a, vec4d)):
			return vec3d(np.array(self) @ np.array(a)).hom
		else:
			return mat3x4(np.array(a) @ np.array(self))

	def identity(self):
		return self.set(_DEFAULT_MAT3X4)


class mat4x4(mat_cls):
	_classname = 'nkj.math.mat4x4'

	def __new__(cls, m=None):
		self = super().__new__(cls, shape=(4, 4), dtype='float32')
		self.set(_DEFAULT_MAT4X4 if (m is None) else self.set(m))
		return self

	def __init__(self, m=None):
		super().__init__()
		self.set(_DEFAULT_MAT4X4 if (m is None) else self.set(m))

	@classmethod
	def getClassName(cls):
		return cls._classname

	def __matmul__(self, a):
		if (isinstance(a, vec4d)):
			return vec4d(np.array(self) @ np.array(a))
		else:
			return mat4x4(np.array(self) @ np.array(a))

	def __rmatmul__(self, a):
		if (isinstance(a, vec4d)):
			return vec4d(np.array(self) @ np.array(a))
		else:
			return mat4x4(np.array(a) @ np.array(self))

	def identity(self):
		return self.set(np.identity(4))


#--- geometry

#-- rotation

_DEFAULT_ROT2D = 0.0   # degree
_DEFAULT_RQUAT = np.array([1.0, 0.0, 0.0, 0.0])   # (x, y, z, w)
_DEFAULT_ROT3D = _DEFAULT_RQUAT
_DEFAULT_TRANS3D = np.array([0.0, 0.0, 0.0])
_DEFAULT_CS3D = [_DEFAULT_ROT3D, _DEFAULT_TRANS3D]

class rot2d(angle_cls):
	_classname = 'nkj.math.rot2d'

	def __init__(self, r=None):
		super().__init__()
		if (r is None):
			self.set()
		else:
			self.set(r)

	def set(self, r=None):
		if (r is None):
			self._r = _DEFAULT_ROT2D
		elif (isinstance(r, float)):
			self._r = r
		else:
			__ERROR__

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	@property
	def mat2x2(self):
		return np.array([[self.cos, -self.sin], [self.sin, self.cos]])

	@property
	def matrix(self):
		return self.mat2x2

	@property
	def mat(self):
		return self.matrix

	@property
	def m(self):
		return self.matrix

	def getInversed(self):
		return copy.deepcopy(self).inverse()

	@property
	def inversed(self):
		return self.getInversed()

	@property
	def inv(self):
		return self.inversed

	@property
	def i(self):
		return self.inversed

	def inverse(self):
		self._r *= -1.0

class rot2D(rot2d):
	pass

class r2d(rot2d):
	pass

class r2D(r2d):
	pass

class csrot2d(rot2d):
	pass

class csrot2D(csrot2d):
	pass

class csr2d(rot2d):
	pass

class csr2D(csr2d):
	pass


class rot3d():
	_classname = 'nkj.math.rot3d'

	def __init__(self, a=None, flag=None, axis=None):
		if (a is None):
			self.set(_DEFAULT_ROT3D)
		else:
			self.set(a, flag, axis)

	def __str__(self):
		return self.getStr()

	# operators

	def __mul__(self, second):
		return self.getMultipliedLocal(second)

	def __rmul__(self, first):
		return self.getMultipliedGlobal(first)

	def __matmul__(self, second):
		return self.__mul__(second)

	def __rmatmul__(self, first):
		return self.__rmul__(first)

	def __invert__(self):
		return self.getInversed()

	# classname

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	# get, set

	def get(self):
		return self.array()

	def set(self, a=None, flag=None, axis=None):
		ldprint('--> nkj.math.rot3d.set()')
		if (a is None):
			self.setQuaternion()  # default setting
			__ERROR__
		elif (isinstance(a, rot3d)):
			self.setR(a._r)
		elif (isinstance(a, R)):
			self.setR(a)
		elif (isinstance(a, list) or isinstance(a, tuple)):
			dim = ndim(a)
			if (dim == 1):
				sh = shape(a)
				if (sh == (4,)):
					if (flag is None or flag == 'quaternion' or flag == 'quat'):
						self._r = R.from_quat(self._array_np2r(a)) # quaternion
					elif (flag == 'R.quaternion' or flag == 'rquat'):
						self._r = R.from_quat(copy.copy(a))
					else:
						___ERROR___
				elif (sh == (3,)):
					if (flag is None or flag == 'rotationalvector' or flag == 'rotvec'):
						self._r = R.from_rotvec(copy.copy(a))
					elif (flag == 'directioncosines' or flag == 'dircos'):
						if (axis is None):
							axis = np.array([0, 0, 1])
						x = vecnormalize(copy.copy(a))
						axis = vecnormalize(axis)
						raxis = np.cross(axis, x)
						angle = vecangle(axis, x)
						rvec = angle * raxis
						self.set(rvec, 'rotvec')
					elif (flag == 'directionangles' or flag == 'dirang'):
						r = [np.cos(a[0]), np.cos(a[1]), np.cos(a[2])]
						self.set(r, 'dircos')
					elif (flag == 'euler_zyx'):
						self._r = R.from_euler('zyx', copy.copy(a)) # extrinsic rotation
					elif (flag == 'euler_ZYX'):
						self._r = R.from_euler('ZYX', copy.copy(a)) # intrinsic rotation
					elif (flag == 'euler_xyx'):
						self._r = R.from_euler('xyx', copy.copy(a))
					elif (flag == 'euler_XYX'):
						self._r = R.from_euler('XYX', copy.copy(a))
					else:
						___ERROR___
				elif (sh == (2,)):
					if (flag is None or flag == 'anglevec' or flag == 'angleaxis'):
						angle = a[0]
						if (not is_scalar(angle)):
							___ERROR___
						vec = a[1]
						if (shape(vec) == (3,)):
							rvec = angle * vecnormalize(np.array(vec))
							self.set(rvec, 'rotvec')
						else:
							___ERROR___
					else:
						___ERROR___
				else:
					___ERROR___
			elif (dim == 2):
				sh = shape(a)
				if (sh == (3, 3)):
					if (flag is None or flag == 'matrix' or flag == 'mat'):
						self._r = R.from_matrix(copy.copy(a))
					else:
						___ERROR___
				else:
					___ERROR___
			else:
				___ERROR___
		elif (isinstance(a, np.ndarray)):
			dim = a.ndim
			if (dim == 1):
				sh = a.shape
				if (sh == (4,)):
					if (flag is None or flag == 'quaternion' or flag == 'quat'):
						self._r = R.from_quat(self._array_np2r(a))
					elif (flag == 'R.quaternion' or flag == 'rquat'):
						self._r = R.from_quat(copy.copy(a))
					else:
						___ERROR___
				elif (sh == (3,)):
					if (flag is None or flag == 'rotationalvector' or flag == 'rotvec'):
						self._r = R.from_rotvec(copy.copy(a))
					elif (flag == 'euler_zyx'):
						self._r = R.from_euler('zyx', copy.copy(a)) # extrinsic rotation
					elif (flag == 'euler_ZYX'):
						self._r = R.from_euler('ZYX', copy.copy(a)) # intrinsic rotation
					elif (flag == 'euler_xyx'):
						self._r = R.from_euler('xyx', copy.copy(a))
					elif (flag == 'euler_XYX'):
						self._r = R.from_euler('XYX', copy.copy(a))
					else:
						___ERROR___
				elif (sh == (2,)):
					if (flag is None or flag == 'anglevec' or flag == 'angleaxis'):
						angle = a[0]
						if (not is_scalar(angle)):
							___ERROR___
						vec = a[1]
						if (shape(vec) == (3,)):
							rvec = angle * vecnormalize(np.array(vec))
							self.set(rvec, 'rotvec')
						else:
							___ERROR___
					else:
						___ERROR___
				else:
					___ERROR___
			elif (dim == 2):
				sh = a.shape
				if (sh == (3, 3)):
					self._r = R.from_matrix(copy.deepcopy(a)) # 3x3 matrix
				elif (sh == (4, 4)):
					self._r = R.from_matrix(_mat_4x4to3x3(a)) # 4x4 matrix
				else:
					___ERROR___
			else:
				___ERROR___
		else:
			___ERROR___
		ldprint('<-- nkj.math.rot3d.set()')

	# R

	def getR(self):
		return self._r

	def setR(self, r):
		if (r is None):
			__ERROR__
		if (not isinstance(r, R)):
			__ERROR__
		self._r = copy.deepcopy(r)

	@property
	def R(self):
		return self.getR()

	@R.setter
	def R(self, second):
		self.setR(second)

	@property
	def r(self):
		return self.getR()

	@r.setter
	def r(self, second):
		self.setR(second)

	# scipy.R quaternion (x, y, z, w)

	def getRQuaternion(self):
		return self.getR().as_quat()

	def setRQuaternion(self, q=None):
		self.setR(R.from_quat(_DEFAULT_RQUAT if (q is None) else q))

	def getRQuat(self):
		return self.getQuaternion()

	def setRQuat(self, q):
		self.setQuaternion(q)

	@property
	def rquaternion(self):
		return self.getRQuaternion()

	@rquaternion.setter
	def rquaternion(self, q):
		self.setRQuaternion(q)

	@property
	def rquat(self):
		return self.rquaternion

	@rquat.setter
	def rquat(self, q):
		self.rquaternion = q

	@property
	def rq(self):
		return self.rquaternion

	@rq.setter
	def rq(self, q_):
		self.rquaternion = q_

	# numpy quaternion array (w, x, y, z)

	def _normalize(self, a):
		a = list(a)
		mag = np.sqrt(a[0]**2 + a[1]**2 + a[2]**2 + a[3]**2)
		return a if (mag == 0.0) else a / mag

	def _array_np2r(self, a):
		a = self._normalize(a)
		return [a[1], a[2], a[3], a[0]] # (w, x, y, z) to (x, y, z, w)

	def _array_r2np(self, a):
		a = self._normalize(a)
		return np.array([a[3], a[0], a[1], a[2]]) # (x, y, z, w) to (w, x, y, z)

	def getNumpyQuaternion(self):
		return self._array_r2np(self.getRQuaternion())

	def setNumpyQuaternion(self, q=None):
		self.setRQuaternion(_DEFAULT_RQUAT if (q is None) else self._array_np2r(np.array(q)))

	def getNumpyQuat(self):
		return self.getNumpyQuaternion()

	def setNumpyQuat(self, a):
		self.setNumpyQuaternion(a)

	def getNpQuaternion(self):
		return self.getNumpyQuaternion()

	def setNpQuaternion(self, a):
		self.setNumpyQuaternion(a)

	def getNpQuat(self):
		return self.getNumpyQuaternion()

	def setNpQuat(self, a):
		self.setNumpyQuaternion(a)

	@property
	def numpyquaternion(self):
		return self.getNumpyQuaternion()

	@numpyquaternion.setter
	def numpyquaternion(self, q):
		self.setNumpyQuaternion(q)

	@property
	def numpyquat(self):
		return self.numpyquaternion

	@numpyquat.setter
	def numpyquat(self, q):
		self.numpyquaternion = q

	@property
	def npquaternion(self):
		return self.numpyquaternion

	@npquaternion.setter
	def npquaternion(self, q):
		self.numpyquaternion = q

	@property
	def npquat(self):
		return self.numpyquaternion

	@npquat.setter
	def npquat(self, q):
		self.numpyquaternion = q

	@property
	def npq(self):
		return self.numpyquaternion

	@npq.setter
	def npq(self, q):
		self.numpyquaternion = q

	# quaternion (= numpy quaternion) (w, x, y, z)

	def getQuaternion(self):
		return self.getNumpyQuaternion()

	def setQuaternion(self, q):
		self.setNumpyQuaternion(q)

	def getQuat(self):
		return self.getQuaternion()

	def setQuat(self, q):
		self.setQuaternion(q)

	@property
	def quaternion(self):
		return self.getQuaternion()

	@quaternion.setter
	def quaternion(self, q):
		self.setQuaternion(q)

	@property
	def quat(self):
		return self.quaternion

	@quat.setter
	def quat(self, q):
		self.quaternion = q

	@property
	def q(self):
		return self.quaternion

	@q.setter
	def q(self, q_):
		self.quaternion = q_

	@property
	def qw(self):
		return self.quaternion[0]

	@property
	def qx(self):
		return self.quaternion[1]

	@property
	def qy(self):
		return self.quaternion[2]

	@property
	def qz(self):
		return self.quaternion[3]

	# matrix

	def getMat3x3(self):
		return mat3x3(self._r.as_matrix())

	def setMat3x3(self, m):
		self.set(m)

	@property
	def mat3x3(self):
		return self.getMat3x3()

	@mat3x3.setter
	def mat3x3(self, second):
		self.setMat3x3(second)

	def getMatrix(self):
		return self.getMat3x3()

	def setMatrix(self, m):
		self.setMat3x3(m)

	@property
	def matrix(self):
		return self.getMatrix()

	@matrix.setter
	def matrix(self, second):
		self.setMatrix(second)

	@property
	def mat(self):
		return self.getMatrix()

	@mat.setter
	def mat(self, second):
		self.setMatrix(second)

	@property
	def m(self):
		return self.getMatrix()

	@m.setter
	def m(self, second):
		self.setMatrix(second)

	# rotational vector

	def getRotationalVector(self):
		return self._r.as_rotvec()

	def setRotationalVector(self, rv=None):
		if (rv is None):
			self.set()
		else:
			self.set(rv, 'rotvec')

	@property
	def rotionalvector(self):
		return self.getRotationalVector()

	@rotionalvector.setter
	def rotionalvector(self, rv):
		self.setRotationalVector(rv)

	@property
	def rotationvector(self):
		return self.rotationalvector

	@rotationvector.setter
	def rotationvector(self, rv):
		self.rotationalvector = rv

	@property
	def rotvec(self):
		return self.rotationalvector

	@rotvec.setter
	def rotvec(self, rv):
		self.rotationalvector = rv

	@property
	def rv(self):
		return self.rotationalvector

	@rv.setter
	def rv(self, rv_):
		self.rotationalvector = rv_

	@property
	def rx(self):
		return self.rotvec[0]

	@property
	def ry(self):
		return self.rotvec[1]

	@property
	def rz(self):
		return self.rotvec[2]

	# rotational angle/axis

	def getRotationalAngle(self):
		return self.R.magnitude()

	def getRotationAngle(self):
		return self.getRotationalAngle()

	def getRotAngle(self):
		return self.getRotationalAngle()

	def getAngle(self):
		return self.getRotationalAngle()

	@property
	def rotationalangle(self):
		return self.getRotationalAngle()

	@property
	def rotationangle(self):
		return self.rotationalangle

	@property
	def rotangle(self):
		return self.rotationalangle

	@property
	def angle(self):
		return self.getAngle()

	def getRotationalAxis(self):
		return vecnormalize(self.R.as_rotvec())

	def getRotationAxis(self):
		return self.RotationalAxis()

	def getRotAxis(self):
		return self.RotationalAxis()

	def getAxis(self):
		return self.RotationalAxis()

	@property
	def rotationalaxis(self):
		return self.getRotationalAxis()

	@property
	def rotationaxis(self):
		return self.rotationalaxis

	@property
	def rotaxis(self):
		return self.rotationalaxis

	@property
	def axis(self):
		return self.getAxis()

	# Modified Rodrigues Parameters (MRPs)

	def getMRP(self):
		return self._r.as_mrp()

	def setMRP(self, mrp):
		self.set(mrp, 'mrp')

	@property
	def mrp(self):
		return self.getMRP()

	@mrp.setter
	def mrp(self, mrp_):
		self.setMRP(mrp_)

	# Euler angles

	def getEulerAngles(self, flag=None):
		if (flag is None):
			return self._r.as_euler()
		else:
			return self._r.as_euler(flag)

	def getEuler(self, flag=None):
		return self.getEulerAngles(flag)

	def EulerAngles(self, flag=None):
		return self.getEulerAngles(flag)

	def Euler(self, flag=None):
		return self.EulerAngles(flag)

	@property
	def eulerangles(self):
		return self.getEulerAngles()

	@property
	def euler(self):
		return self.eulerangles

	# invert

	def getInversed(self):
		return rot3d(self._r.inv())

	@property
	def inversed(self):
		return self.getInversed()

	@property
	def inv(self):
		return self.inversed

	@property
	def i(self):
		return self.inversed

	def inverse(self):
		return self.set(self.inversed)

	# operations

	def getMultipliedScalar(self, value):
		return rot3d(value * self.as_rotvec(), 'rotvec')

	def getMultipliedLocal(self, second):
		ldprint(["--> getMultipliedLocal()"])
		if (isinstance(second, rot3d)):
			return rot3d(self._r @ second._r)
		elif (isinstance(second, R)):
			return rot3d(self._r @ second)
		elif (isinstance(second, list) or isinstance(second, tuple)):
			if (ndim(second) == 2):
				if (shape(second) == (3, 3)):
					return self.getMultipliedLocal(rot3d(second))
				else:
					___ERROR___
			else:
				___ERROR___
		elif (isinstance(second, np.ndarray)):
			if (second.dim == 2):
				if (second.shape == (3, 3)):
					return self.getMultipliedLocal(rot3d(second))
				else:
					___ERROR___
			else:
				___ERROR___
		elif (is_scalar(second)):
			return getMultipliedScalar(second)
		else:
			___ERROR___

	def multipliedLocal(self, second):
		return self.getMultipliedLocal(second)

	def getMultipliedGlobal(self, first):
		if (isinstance(first, rot3d)):
			return rot3d(first._r @ self._r)
		elif (type(first) is R):
			return rot3d(first @ self._r)
		elif (isinstance(first, list) or isinstance(first, tuple)):
			if (ndim(first) == 2):
				if (shape(first) == (3, 3)):
					return self.getMultipliedGlobal(rot3d(first))
				else:
					___ERROR___
			else:
				___ERROR___
		elif (isinstance(first, np.ndarray)):
			if (first.dim == 2):
				if (first.shape == (3, 3)):
					return self.getMultipliedGlobal(rot3d(first))
				else:
					___ERROR___
			else:
				___ERROR___
		elif (is_scalar(first)):
			return getMultipliedScalar(first)
		else:
			___ERROR___

	def multipliedGlobal(self, second):
		return self.getMultipliedGlobal(second)

	def getRotatedLocal(self, r, flag=None):
		return self.getMultiplinedLocal(rot3d(r, flag))

	def rotatedLocal(self, r, flag=None):
		return self.getRotatedLocal(r, flag)

	def getRotatedGlobal(self, r, flag=None):
		return self.getMultiplinedGlobal(rot3d(r, flag))

	def rotatedGlobal(self, second):
		return self.getRotatedGlobal(second)

	# string

	def getStr(self):
		return self.getPrintString()

	@property
	def str(self):
		return self.getStr()

	def getDataStr(self):
		q = self.quat
		w = q[0]; x = q[1]; y = q[2]; z = q[3]
		c = w
		s = np.sqrt(x**2 + y**2 + z**2)
		angle = 2.0 * np.arctan2(s, c)
		if (s == 0.0):
			rotaxis = (x, y, z)
		else:
			rotaxis = (x / s, y / s, z / s)
		return '{0:.12f}, {1:.12f}, {2:.12f}, {3:.12f}'.format(angle, rotaxis[0], rotaxis[1], rotaxis[2])

	@property
	def datastr(self):
		return self.getDataStr()

	# print

	def getPrintString(self, title=None):
		if (title is None):
			mesg = ''
		else:
			mesg = '{0}: '.format(title)
		q = self.quat
		w = q[0]; x = q[1]; y = q[2]; z = q[3]
		c = w
		s = np.sqrt(x**2 + y**2 + z**2)
		angle = 2.0 * np.arctan2(s, c)
		if (s == 0.0):
			rotaxis = (x, y, z)
		else:
			rotaxis = (x / s, y / s, z / s)
		mesg += 'angle: {0:.6f} deg, '.format(rad2deg(angle))
		mesg += 'axis: ({0:.12f}, {1:.12f}, {2:.12f})'.format(rotaxis[0], rotaxis[1], rotaxis[2])
		return mesg

	def getPrintStr(self, title=None):
		return self.getPrintString(title)

	@property
	def printstr(self):
		return self.getPrintString()

	@property
	def pstr(self):
		return self.printstr

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)

class rot3D(rot3d):
	pass

class r3d(rot3d):
	pass

class r3D(r3d):
	pass

class csrot3d(rot3d):
	pass

class csrot3D(csrot3d):
	pass

class csr3d(rot3d):
	pass

class csr3D(csr3d):
	pass


#-- quaternion

class quat_cls(rot3d):
	_classname = 'nkj.math.quat'

	def __init__(self, q=None):
		self.set(None if (q is None) else q)

	@classmethod
	def getClassName(cls):
		return cls._classname

	def get(self):
		return self.getQuaternion()

	def set(self, q=None):
		self.setQuaternion(None if (q is None) else q)

	# string

	def getStr(self):
		return self.getPrintString()

	def getDataStr(self):
		q = self.quat
		w = q[0]; x = q[1]; y = q[2]; z = q[3]
		return '{0:.12f}, {1:.12f}, {2:.12f}, {3:.12f}'.format(w, x, y, z)

	# print

	def getPrintString(self, title=None):
		if (title is None):
			s = ''
		else:
			s = '{0}: '.format(title)
		q = self.quat
		w = q[0]; x = q[1]; y = q[2]; z = q[3]
		s += '({0:.12f}, {1:.12f}, {2:.12f}, {3:.12f})'.format(w, x, y, z)
		return s

class quat(quat_cls):
	pass


#-- translation

class trans2d(vec2d):
	_classname = 'nkj.math.trans2d'

	@classmethod
	def getClassName(cls):
		return cls._classname

	def getPrintString(self, title=None):
		if (title is None):
			s = ''
		else:
			s = '{0}: '.format(title)
		t = self
		s += '{0:.12f}, {1:.12f}'.format(t[0][0], t[1][0])
		return s

class trans2D(trans2d):
	pass

class t2d(trans2d):
	pass

class t2D(t2d):
	pass

class cstrans2d(trans2d):
	pass

class cstrans2D(cstrans2d):
	pass

class cst2d(trans2d):
	pass

class cst2D(csr2d):
	pass


class trans3d(vec3d):
	_classname = 'nkj.math.trans3d'

	@classmethod
	def getClassName(cls):
		return cls._classname

	def getPrintString(self, title=None):
		if (title is None):
			s = ''
		else:
			s = '{0}: '.format(title)
		t = self
		s += '{0:.12f}, {1:.12f}, {2:.12f}'.format(t[0][0], t[1][0], t[2][0])
		return s

class trans3D(trans3d):
	pass

class t3d(trans3d):
	pass

class t3D(t3d):
	pass

class cstrans3d(trans3d):
	pass

class cstrans3D(cstrans3d):
	pass

class cst3d(trans3d):
	pass

class cst3D(csr3d):
	pass


#-- coordinate system transform

class cs2d():
	_classname = 'nkj.math.cs2d'

	def __init__(self, cs=None):
		if (cs is None):
			self.set()
		else:
			self.set(cs)

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def set(self, cs=None):
		if (cs is None):
			self.setRotation()
			self.setTranslation()
		elif (isinstance(cs, list) or isinstance(cs, tuple)):
			self.setRotation(cs[0])
			self.setTranslation(cs[1])
		else:
			__ERROR__

	def getRotation(self):
		return self._r

	def setRotation(self, r=None):
		self._r = rot2d() if (r is None) else rot2d(r)

	def getRot(self):
		return self.getRotation()

	def setRot(self, r):
		return self.setRotation(r)

	@property
	def rotation(self):
		return self.getRotation()

	@rotation.setter
	def rotation(self, r):
		self.setRotation(r)

	@property
	def rot(self):
		return self.rotation

	@rot.setter
	def rot(self, r):
		self.rotation = r

	@property
	def r(self):
		return self.rotation

	@r.setter
	def r(self, r_):
		self.rotation = r_

	def getTranslation(self):
		return self._t

	def setTranslation(self, t=None):
		self._t = trans2d() if (t is None) else trans2d(t)

	@property
	def translation(self):
		return self.getTranslation()

	@translation.setter
	def translation(self, t):
		self.setTranslation(t)

	@property
	def trans(self):
		return self.translation

	@trans.setter
	def trans(self, t):
		self.translation = t

	@property
	def t(self):
		return self.translation

	@t.setter
	def t(self, t_):
		self.translation = t_

	def getMat3x3(self):
		m = mat3x3()
		for j in range(2):
			for i in range(2):
				m[j, i] = self.r.m[j, i]
		m[0, 2] = self.t[0][0]; m[1, 2] = self.t[1][0]
		m[2, 0] = 0.0; m[2, 1] = 0.0; m[2, 2] = 1.0
		return m

	def setMat3x3(self, m):
		for j in range(3):
			for i in range(3):
				self.r[j, i] = m[j, i]

	@property
	def mat3x3(self):
		return self.getMat3x3()

	@mat3x3.setter
	def mat3x3(self, m):
		self.setMat3x3(m)

	@property
	def matrix(self):
		return self.mat3x3

	@matrix.setter
	def matrix(self, m):
		self.mat3x3 = m

	@property
	def mat(self):
		return self.matrix

	@mat.setter
	def mat(self, m):
		self.matrix = m

	@property
	def m(self):
		return self.matrix

	@m.setter
	def m(self, m_):
		self.matrix = m_

	# string

	def getStr(self):
		s = self._r.getDataStr()
		s += ', '
		s += self._t.getDataStr()
		return s

	def str(self):
		return self.getStr()

	def getDataStr(self):
		s = self._r.getDataStr()
		s += ', '
		s += self._t.getDataStr()
		return s

	@property
	def datastr(self):
		return self.getDataStr()

	# print

	def getPrintString(self, title=None):
		if (title is None):
			mesg = ''
		else:
			mesg = '{0}: '.format(title)
		r = self._r
		t = self._t
		mesg += 'r:({0}), t:({1})'.format(r.getPrintString(), t.getPrintString())
		return mesg

	def getPrintStr(self, title=None):
		return self.getPrintString(title)

	@property
	def printstr(self):
		return self.getPrintString()

	@property
	def pstr(self):
		return self.printstr

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)


class cs3d():
	_classname = 'nkj.math.cs3d'

	def __init__(self, a=None, flag=None):
		if (a is None):
			self.set()
		else:
			self.set(a, flag)

	def __str__(self, title=None):
		return self.getPrintString(title)

	def __matmul__(self, second):
		return self.getMultipliedGlobal(second)

	def __rmatmul__(self, first):
		return self.getMultipliedLocal(first)

	if (ENABLE_MULOPERATOR_FOR_CSTRANS3D_CLASS):
		def __mul__(self, second):
			return self.__matmul__(second)

		def __rmul__(self, first):
			return self.__rmatmul__(first)

	def __invert__(self):
		return self.getInversed()

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def set(self, a=None, flag=None):
		ldprint(['--> set({0}, \'{1}\')'.format(a, flag)])
		if (a is None):
			self._r = rot3d()
			self._t = trans3d()
		elif (isinstance(a, cs3d)):
			self._r = a._r
			self._t = a._t
			if (flag is not None):
				if (flag != 'cs3d'):
					___ERROR___
		elif (isinstance(a, list) or isinstance(a, tuple)):
			sh = shape(a)
			if (sh == (2,) or sh == (2, 3)):
				r = a[0]
				t = a[1]
				ldprint("r: {0}".format(r))
				ldprint("t: {0}".format(t))
				self._r = rot3d(r, flag)
				self._t = trans3d(t)
			else:
				___ERROR___
		elif (isinstance(a, mat4x4)):
			self.setMat4x4(a)
		elif (isinstance(a, np.ndarray)):
			sh = a.shape
			if (sh == (3, 3)):
				self._r = rot3d(np.array([[a[0, 0], a[0, 1], a[0, 2]],
				                          [a[1, 0], a[1, 1], a[1, 2]],
				                          [a[2, 0], a[2, 1], a[2, 2]]]))
			elif (sh == (3, 4) or sh == (4, 4)):
				self._r = rot3d(np.array([[a[0, 0], a[0, 1], a[0, 2]],
				                          [a[1, 0], a[1, 1], a[1, 2]],
				                          [a[2, 0], a[2, 1], a[2, 2]]]))
				self._t = trans3d(np.array([a[0, 3], a[1, 3], a[2, 3]]))
		else:
			___ERROR___

	# operations

	def getMultipliedScalar(self, value):
		r = value * self._r.rotvec
		t = value * self._t
		return cs3d([r.quat, t])

	def multipliedScalar(self, value):
		return self.getMultipliedScalar(value)

	def getMultipliedGlobal(self, second):
		ty = type(second)
		if (ty is csrot3d):
			return cs3d(self.matrix @ to4x4(second.getMatrix()))
		elif (ty is cs3d):
			return cs3d(self.matrix @ second.getMatrix())
		elif (ty is list or ty is tuple):
			if (ndim(second) == 2):
				m = second
				if (shape(m) == (3, 3)):
					return self.getMultipliedGlobal(csrot3d(m))
				elif (shape(m) == (4, 4)):
					return self.getMultipliedGlobal(cs3d(m))
				else:
					___ERROR___
			elif (ndim(second) == 1): # vector
				v = second
				return self.getMultipliedGlobal(np.array(v, dtype=np.float32))
			else:
				___ERROR___
		elif (ty is np.ndarray):
			if (second.ndim == 2):
				m = second
				if (m.shape == (3, 3)):
					return self.getMultipliedGlobal(csrot3d(m))
				elif (m.shape == (4, 4)):
					return self.getMultipliedGlobal(cs3d(m))
				else:
					___ERROR___
			elif (second.ndim == 1): # vector
				v = second
				if (v.shape == (3,)):
					return tovec3(self.getMultipliedGlobal(tovec4(v)))
				elif (v.shape == (4,)):
					m = self.matrix
					return m @ v
				else:
					___NOT_IMPLEMENTED___
			else:
				___ERROR___
		elif (is_scalar(second)):
			return getMultipliedScalar(second)
		elif (is_geometric(second)):
			return second.getMultiplied(self)
		else:
			___ERROR___

	def multipliedGlobal(self, second):
		return getMultipliedGlobal(second)

	def getMultipliedLocal(self, first):
		ty = type(first)
		if (ty is csrot3d):
			return cs3d(to4x4(first.getMatrix()) @ self.matrix)
		elif (ty is cs3d):
			return cs3d(first.getMatrix() @ self.matrix)
		elif (ty is list or ty is tuple):
			if (ndim(first) == 2):
				m = first
				if (shape(m) == (3, 3)):
					return self.getMultipliedLocal(csrot3d(m))
				elif (shape(m) == (4, 4)):
					return self.getMultipliedLocal(cs3d(m))
				else:
					___ERROR___
			elif (ndim(first) == 1): # vector
				v = first
				return self.getMultipliedLocal(np.array(v, dtype=np.float32))
			else:
				___ERROR___
		elif (ty is np.ndarray):
			if (first.ndim == 2):
				m = first
				if (m.shape == (3, 3)):
					return self.getMultipliedLocal(csrot3d(m))
				elif (m.shape == (4, 4)):
					return self.getMultipliedLocal(cs3d(m))
				else:
					___ERROR___
			elif (first.ndim == 1): # vector
				v = first
				return self.getMultipliedGlobal(v) # The same value is returned.
			else:
				___ERROR___
		elif (is_scalar(secon)):
			return getMultipliedScalar(secon)
		elif (is_geometric(secon)):
			return first.getMultiplied(self)
		else:
			___ERROR___

	def multipliedLocal(self, first):
		return getMultipliedLocal(first)

	# rotation

	def getRotation(self):
		return self._r

	def setRotation(self, r=None):
		self._r = rot3d() if (r is None) else rot3d(r)

	def getRot(self):
		return self.getRotation()

	def setRot(self, r):
		return self.setRotation(r)

	def getR(self):
		return self.getRotation()

	def setR(self, r):
		return self.setRotation(r)

	@property
	def rotation(self):
		return self.getRotation()

	@rotation.setter
	def rotation(self, r):
		self.setRotation(r)

	@property
	def rot(self):
		return self.rotation

	@rot.setter
	def rot(self, r):
		self.rotation = r

	@property
	def r(self):
		return self.rotation

	@r.setter
	def r(self, r_):
		self.rotation = r_

	# translation

	def getTranslation(self):
		return self._t

	def setTranslation(self, t=None):
		self._t = trans2d() if (t is None) else trans2d(t)

	def getTrans(self):
		return self.getTranslation()

	def setTrans(self, t):
		self.setTranslation(t)

	def getT(self):
		return self.getTranslation()

	def setT(self, t):
		self.setTranslation(t)

	@property
	def translation(self):
		return self.getTranslation()

	@translation.setter
	def translation(self, t):
		self.setTranslation(t)

	@property
	def trans(self):
		return self.translation

	@trans.setter
	def trans(self, t):
		self.translation = t

	@property
	def t(self):
		return self.translation

	@t.setter
	def t(self, t_):
		self.translation = t_

	def getOrigin(self):
		return self.getTranslation()

	def setOrigin(self, o):
		self.setOrigin(o)

	@property
	def origin(self):
		return self.getOrigin()

	@origin.setter
	def origin(self, second):
		self.setOrigin(second)

	@property
	def orig(self):
		return self.origin

	@orig.setter
	def orig(self, o):
		self.origin = o

	@property
	def o(self):
		return self.origin

	@o.setter
	def o(self, o_):
		self.origin = o_

	# R

	@property
	def R(self):
		return self._r.R

	@R.setter
	def R(self, second):
		self._r.set(R)

	# quaternion

	@property
	def rquatarray(self):
		return self._r.rquatarray

	@rquatarray.setter
	def rquatarray(self, second):
		self._r.set(second)

	@property
	def rquat(self):
		return self.rquatarray

	@rquat.setter
	def rquat(self, second):
		self.set(second)

	@property
	def npquatarray(self):
		return self._r.npquatarray

	def getQuat(self):
		return self._r.quat

	def setQuat(self, second):
		self.set(second, 'quaternion')

	@property
	def quat(self):
		return self.getQuat()

	@quat.setter
	def quat(self, second):
		self.setQuat(second)

	@property
	def q(self):
		return self.quat

	@q.setter
	def q(self, second):
		self.quat = second

	# rotational vector

	def getRotationalVector(self):
		pass

	def getRotvec(self):
		return self._r.as_rotvec()

	@property
	def rotvec(self):
		return self.getRotvec()

	@property
	def rvec(self):
		return self.getRotvec()

	def setRotvec(self, second):
		self.set(second, 'rotvec')

	@rotvec.setter
	def rotvec(self, second):
		self.setRotvec(second)

	@rvec.setter
	def rvec(self, second):
		self.setRotvec(second)

	# rotational matrix

	def getRotationalMatrix(self):
		return self._r.mat3x3

	def setRotationalMatrix(self, second):
		self.set(second)

	def getRotationMatrix(self):
		return self.getRotationalMatrix()

	def setRotationMatrix(self, second):
		self.setRotationalMatrix(second)

	@property
	def rotationalmatrix(self):
		return self.getRotationalMatrix()

	@rotationalmatrix.setter
	def rotationalmatrix(self, second):
		self.setRotationalMatrix(second)

	@property
	def rotmat(self):
		return self.getRotationalMatrix()

	@rotmat.setter
	def rotmat(self, second):
		self.setRotationalMatrix(second)

	@property
	def rm(self):
		return self.getRotationalMatrix()

	@rm.setter
	def rm(self, second):
		self.setRotationalMatrix(second)

	# translational vector

	def getTranslationalVector(self):
		return self.getTranslation()

	def setTranslationalVector(self, v):
		self.setTranslation(v)

	def getTranslationVector(self):
		return self.getTranslationalVector()

	def setTranslationVector(self, v):
		self.setTranslationalVector(v)

	@property
	def translationalvector(self):
		return self.getTranslationalVector()

	@translationalvector.setter
	def translationalvector(self, v):
		self.setTranslationalVector(v)

	@property
	def translationvector(self):
		return self.translationalvector

	@translationvector.setter
	def translationvector(self, v):
		self.translationalvector = v

	@property
	def transvec(self):
		return self.translationalvector

	@transvec.setter
	def transvec(self, v):
		self.translationalvector = v

	@property
	def tv(self):
		return self.translationalvector

	@tv.setter
	def tv(self, v):
		self.translationalvector = v

	# matrix

	def getMat4x4(self):
		m = mat4x4()
		for j in range(3):
			for i in range(3):
				m[j, i] = self.rm[j, i]
		m[0, 3] = self.tv[0]; m[1, 3] = self.tv[1]; m[2, 3] = self.tv[2]
		m[3, 0] = 0.0; m[3, 1] = 0.0; m[3, 2] = 0.0; m[3, 3] = 1.0
		return m

	def setMat4x4(self, m):
		for j in range(4):
			for i in range(4):
				self.r[j, i] = m[j, i]

	@property
	def mat4x4(self):
		return self.getMat4x4()

	@mat4x4.setter
	def mat4x4(self, m):
		self.setMat4x4(m)

	def getMatrix(self):
		return self.getMat4x4()

	def setMatrix(self, m):
		self.setMat4x4(m)

	@property
	def matrix(self):
		return self.mat4x4

	@matrix.setter
	def matrix(self, m):
		self.mat4x4 = m

	@property
	def mat(self):
		return self.matrix

	@mat.setter
	def mat(self, m):
		self.matrix = m

	@property
	def m(self):
		return self.matrix

	@m.setter
	def m(self, m_):
		self.matrix = m_

	# rotational axes

	def getAxes(self):
		rm = self.getRotationalMatrix()
		xaxis = rm[:, 0]
		yaxis = rm[:, 1]
		zaxis = rm[:, 2]
		return xaxis, yaxis, zaxis

	def setAxes(self, xaxis, yaxis, zaxis):
		rm = np.zeros((3, 3), dtype=np.float32)
		rm[:, 0] = xaxis
		rm[:, 1] = yaxis
		rm[:, 2] = zaxis
		ldprint(f'xaxis: {xaxis}')
		ldprint(f'yaxis: {yaxis}')
		ldprint(f'zaxis: {zaxis}')
		ldprint(f'{rm}')
		self.setRotationalMatrix(rm)

	@property
	def axes(self):
		return self.getAxes()

	@axes.setter
	def axes(self, axes):
		ldprint(f'xaxis: {axes[0]}')
		ldprint(f'yaxis: {axes[1]}')
		ldprint(f'zaxis: {axes[2]}')
		self.setAxes(axes[0], axes[1], axes[2])

	def getXaxis(self):
		return self.getRotMatrix()[:, 0]

	def getYaxis(self):
		return self.getRotMatrix()[:, 1]

	def getZaxis(self):
		return self.getRotMatrix()[:, 2]

	@property
	def xaxis(self):
		return getXaxis()

	@property
	def yaxis(self):
		return getYaxis()

	@property
	def zaxis(self):
		return getZaxis()

	# invert

	def getInversed(self):
		return cs3d(np.linalg.inv(self.matrix))

	@property
	def inversed(self):
		return self.getInversed()

	@property
	def inv(self):
		return self.getInversed()

	@property
	def i(self):
		return self.getInversed()

	def inverse(self):
		self.set(self.getInversed())

	# rotate

	def getRotatedLocal(self, a, flag=None):
		return self.getMultipliedLocal(csrot3d(a, flag))

	def getRotatedGlobal(self, a, flag=None):
		return self.getMultipliedGlobal(to4x4(csrot3d(a, flag).getMatrix()))

	def rotateLocal(self, a, flag=None):
		self.set(self.getRotatedLocal(a, flag))

	def rotateGlobal(self, a, flag=None):
		self.set(self.getRotatedGlobal(a, flag))

	def rotate_local(self, a, flag=None):
		self.rotateLocal(a, flag)

	def rotate_global(self, a, flag=None):
		self.rotateGlobal(a, flag)

	def rotate(self, a, flag=None):
		self.rotate_local(a, flag)

	# translate

	def getTranslatedLocal(self, a):
		t = copy.deepcopy(self)
		t.translateLocal(a)
		return t

	def getTranslatedGlobal(self, a):
		t = copy.deepcopy(self)
		t.translateGlobal(a)
		return t

	def translateLocal(self, a):
		dprint2('--> {0}.translateLocal()'.format(self.getClassName()))
		dprint2('a:    {0}'.format(a))
		dprint2('vec4: {0}'.format(tovec4(a)))
		dprint2('-- m --\n{0}\n--\n'.format(self.getMatrix()))
		dprint2('dot:  {0}'.format(self.getMatrix().dot(tovec4(a))))
		self.setTranslation(self.getTranslation() + tovec3(self.getMatrix().dot(tovec4(a))))
		dprint2('<-- {0}.translateLocal()'.format(self.getClassName()))

	def translateGlobal(self, a):
		self.setTranslation(self.getTranslation() + tovec3(a))

	def translate_local(self, a):
		self.translateLocal(self, a)

	def translate_global(self, a):
		self.translateGlobal(self, a)

	def translate(self, a):
		self.translate_local(a, flag)

	# string

	def getStr(self):
		s = self._r.getDataStr()
		s += ', '
		s += self._t.getDataStr()
		return s

	def str(self):
		return self.getStr()

	def getDataStr(self):
		s = self._r.getDataStr()
		s += ', '
		s += self._t.getDataStr()
		return s

	@property
	def datastr(self):
		return self.getDataStr()

	# print

	def getPrintString(self, title=None):
		if (title is None):
			mesg = ''
		else:
			mesg = '{0}: '.format(title)
		r = self._r
		t = self._t
		mesg += 'r:({0}), t:({1})'.format(r.getPrintString(), t.getPrintString())
		return mesg

	def getPrintStr(self, title=None):
		return self.getPrintString(title)

	@property
	def printstr(self):
		return self.getPrintString()

	@property
	def pstr(self):
		return self.printstr

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)

class cs3D(cs3d):
	pass


#-- geometrical primitives

class point2d(vec2d):
	_classname = 'nkj.math.point2d'

	def __init__(self, p=None):
		super().__init__(p)

	@classmethod
	def getClassName(cls):
		return cls._classname


class point3d(vec3d):
	_classname = 'nkj.math.point3d'

	def __init__(self, p=None):
		super().__init__(p)

	@classmethod
	def getClassName(cls):
		return cls._classname


#-- line

_DEFAULT_LINE2D = np.array([[0.0, 0.0], [1.0, 0.0]]).T  # orig:(0.0, 0.0), second:(1.0, 0.0) -> [[0.0], [[1.0], -> [[0.0, 1.0],
                                                        #                                        [0.0]]  [0.0]]     [0.0, 0.0]]
_DEFAULT_LINE3D = np.array([[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]).T

class line_cls(array_cls):
	_classname = 'nkj.math.line'
	_componentclass = None

	@classmethod
	def getClassName(cls):
		return cls._classname

	# component class

	@classmethod
	def getComponentClass(cls):
		return cls._componentclass

	@classmethod
	@property
	def componentclass(cls):
		return cls.getComponentClass()

	# point

	def getPoint(self, index=None):
		if (index is None):
			index = 0
		rows, columns = self.shape
		if (rows != 2):
			__ERROR__
		if (index < 0 or index > 1):
			__ERROR__
		pl = []
		for i in range(columns):
			pl.append(self[i][index])
		ldprint2('point (list): {}'.format(pl))
		return self.componentclass(pl)

	@property
	def point0(self):
		return self.getPoint(0)

	@property
	def point1(self):
		return self.getPoint(1)

	@property
	def p0(self):
		return self.point0

	@property
	def p1(self):
		return self.point1

	@property
	def origin(self):
		return self.getPoint(0)

	@property
	def orig(self):
		return self.origin

	@property
	def vector(self):
		return (self.point1 - self.point0)

	@property
	def vec(self):
		return self.vector

	# print

	def getPrintString(self, title=None):
		if (title is None):
			s = ''
		else:
			s = '{0}: '.format(title)
		rows, columns = self.shape
		if (rows != 2):
			__ERROR__
		s += '('
		for i in range(columns):
			if (i != 0):
				s += ', '
			s += '{:.12f}'.format(self[i][0])
		s += '), ('
		for i in range(columns):
			if (i != 0):
				s += ', '
			s += '{:.12f}'.format(self[i][1])
		s += ')'
		return s

class line(line_cls):
	pass


class line2d(line_cls):
	_classname = 'nkj.math.line2d'
	_componentclass = point2d

	def __new__(cls, l=None):
		self = super().__new__(cls, shape=(2, 2), dtype='float32')
		self.set(_DEFAULT_LINE2D if (l is None) else self.set(l))
		return self

	def __init__(self, l=None):
		self.set(_DEFAULT_LINE2D if (l is None) else self.set(l))

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	def getComponentClass(cls):
		return cls._componentclass


class line3d(line_cls):
	_classname = 'nkj.math.line3d'
	_componentclass = point3d

	def __new__(cls, l=None):
		self = super().__new__(cls, shape=(3, 2), dtype='float32')
		self.set(_DEFAULT_LINE3D if (l is None) else self.set(l))
		return self

	def __init__(self, l=None):
		self.set(_DEFAULT_LINE3D if (l is None) else self.set(l))

	def __str__(self, title=None):
		return self.getPrintStr(title)

	def __rmatmul__(self, first):
		return self.getMultiplied(first)

	if (ENABLE_MULOPERATOR_FOR_LINE3D_CLASS):
		def __rmul__(self, first):
			return self.__rmatmul__(first)

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	def getComponentClass(cls):
		return cls._componentclass

	# array

	def getArray(self):
		return self._pt

	@property
	def array(self):
		return self.getArray()

	@array.setter
	def array(self, second):
		self.set(second)

	def get(self):
		return self.array()

	def getPoint(self, index=None):
		if (index is None):
			return getPoints()
		else:
			return self._pt[index]

	@property
	def point0(self):
		return self.getPoint(0)

	@property
	def point1(self):
		return self.getPoint(1)

	@property
	def p0(self):
		return self.getPoint(0)

	@property
	def p1(self):
		return self.getPoint(1)

	def getPoints(self):
		return self.array()

	@property
	def points(self):
		return self.getPoints()

	def getOrigin(self):
		return self._pt[0]

	@property
	def origin(self):
		return self.getOrigin()

	@property
	def orig(self):
		return self.getOrigin()

	def getVector(self):
		return self._pt[1] - self._pt[0]

	@property
	def vector(self):
		return self.getVector()

	@property
	def vec(self):
		return self.getVector()

	@property
	def v(self):
		return self.getVector()

	def getLength(self):
		return np.linalg.norm(self.getVector())

	@property
	def length(self):
		return self.getLength()

	@property
	def len(self):
		return self.getLength()

	@property
	def l(self):
		return self.getLength()

	def getDirection(self):
		return vecnormalize(self.getVector())

	@property
	def direction(self):
		return self.getDirection()

	@property
	def direct(self):
		return self.getDirection()

	def set(self, p1, p2=None):
		if (p2 is None):
			if (type(p1) is list or type(p1) is tuple):
				if (len(p1) == 2):
					p2 = p1[1]
					p1 = p1[0]
				else:
				 	___ERROR___
			else:
			 	___ERROR___
		if (type(p1) is np.ndarray):
			pass
		elif (type(p1) is list or type(p1) is tuple):
			p1 = np.array(p1)
		else:
			___ERROR___
		if (type(p2) is np.ndarray):
			pass
		elif (type(p2) is list or type(p2) is tuple):
			p2 = np.array(p2)
		else:
			___ERROR___
		self._pt = [p1, p2]

	def setPoints(self, pts):
		self._pt = pts

	@points.setter
	def points(self, pts):
		self.setPoints(pts)

	def setPoint(self, index, pt):
		self._pt[index] = pt

	def setPoint0(self, p):
		self.setPoint(0, pt)

	def setPoint1(self, p):
		self.setPoint(1, pt)

	@point0.setter
	def point0(self, pt):
		self.setPoint0(pt)

	@point1.setter
	def point1(self, pt):
		self.setPoint1(pt)

	@p0.setter
	def p0(self, pt):
		self.setPoint0(pt)

	@p1.setter
	def p1(self, pt):
		self.setPoint1(pt)

	def setOrigin(self, p):
		self.setPoint0(p)

	@origin.setter
	def origin(self, p):
		self.setOrigin(p)

	@orig.setter
	def orig(self, p):
		self.setOrigin(p)

	def setVector(self, v):
		self._pt[1] = self._pt[0] + v

	@vector.setter
	def vector(self, v):
		self.setVector(v)

	@vec.setter
	def vec(self, v):
		self.setVector(v)

	@v.setter
	def v(self, vec):
		self.setVector(v)

	def setLength(self, len):
		self.setVector(len * self.getDirection())

	@length.setter
	def length(self, len):
		self.setLength(len)

	@len.setter
	def len(self, len):
		self.setLength(len)

	@l.setter
	def l(self, len):
		self.setLength(len)

	def getMultiplied(self, r):
		if (type(r) is csrot3d):
			return self.getMultiplied(r.getMatrix())
		elif (type(r) is cstrans3d):
			return self.getMultiplied(r.getMatrix())
		elif (type(r) is list or type(r) is tuple):
			return self.getMultiplied(np.array(r))
		elif (type(r) is np.ndarray):
			if (r.ndim == 2):
				if (r.shape == (3, 3)):
					p0 = r @ self._pt[0]
					p1 = r @ self._pt[1]
					return line3d(p0, p1)
				elif (r.shape == (4, 4)):
					p0 = vec3(r @ vec4(self._pt[0]))
					p1 = vec3(r @ vec4(self._pt[1]))
					return line3d(p0, p1)
				else:
					___ERROR___
			else:
				___ERROR___
		else:
			___ERROR___

	def multiplied(self, r):
		return self.getMultiplied(r)

	def getRotated(self, r):
		if (type(r) is csrot3d):
			return self.getMultiplied(r.getMatrix())
		elif (type(r) is cstrans3d):
			return self.getMultiplied(r.getMatrix())
		elif (type(r) is list or type(r) is tuple):
			return self.getMultiplied(np.array(r))
		elif (type(r) is np.ndarray):
			if (r.shape == (3, 3)):
				p0 = r @ self._p[0]
				p1 = r @ self._p[1]
				return line3d(p0, p1)
			elif (r.shape == (4, 4)):
				r = to3x3(r)
				p0 = r @ self._p[0]
				p1 = r @ self._p[1]
				return line3d(p0, p1)
			else:
				___ERROR___
		else:
			___ERROR___

	def rotated(self, r):
		return getRotated(r)

	def getTranslated(self, t):
		if (type(t) is cstrans3d):
			return self.getTranslated(t.getTranslation())
		elif (type(t) is list or type(t) is tuple):
			return self.getTranslated(np.array(t))
		elif (type(t) is np.ndarray):
			p0 = self._p[0] + t
			p1 = self._p[1] + t
			return line3d(p0, p1)
		else:
			___ERROR___

	def translated(self, t):
			return self.getTranslated(t)

	def getTransformed(self, t):
		return self.getMultiplied(t)

	def transformed(self, t):
		return self.getTransformed(t)

	def getPrintStr(self, title=None):
		if (title is None):
			mesg = ''
		else:
			mesg = title + ': '
		p0 = self._pt[0]
		p1 = self._pt[1]
		mesg += "({0: .3f}, {1: .3f}, {2: .3f}) - ({3: .3f}, {4: .3f}, {5: .3f})".format(p0[0], p0[1], p0[2], p1[0], p1[1], p1[2])
		return mesg

	@property
	def printstr(self):
		return self.getPrintStr()

	@property
	def str(self):
		return self.getPrintStr()

	def print(self, title=None):
		print(self.getPrintStr(title))

	def getDataStr(self):
		return '{0:21.12f}, {1:21.12f}, {2:21.12f}, {3:21.12f}, {4:21.12f}, {5:21.12f}\n'.format(
		self._pt[0][0], self._pt[0][1], self._pt[0][2],
		self._pt[1][0], self._pt[1][1], self._pt[1][2])

	@property
	def datastr(self):
		return self.getDataStr()

	def setDataStr(self, s):
		s = s.split(',')
		for i in range(len(s)):
			s[i] = float(s[i].strip())
		self.set([(s[0], s[1], s[2]), (s[3], s[4], s[5])])

	@datastr.setter
	def datastr(self, s):
		return setDataStr(s)

	def load(self, filename):
		with open(filename, 'r') as f:
			self.setDataStr(f.read())

	def save(self, filename):
		with open(filename, 'w') as f:
			f.write(self.getDataStr())

#----------------- ここからコメントアウト -----------------------------
"""
class line3d:
	_classname = 'nkj.math.line3d'

	def __init__(self, p1=None, p2=None):
		if (p1 is None and p2 is None):
			p1 = _DEFAULT_LINE3D_POINT1
			p2 = _DEFAULT_LINE3D_POINT2
		self.set(p1, p2)

	def __str__(self, title=None):
		return self.getPrintStr(title)

	def __rmatmul__(self, first):
		return self.getMultiplied(first)

	if (ENABLE_MULOPERATOR_FOR_LINE3D_CLASS):
		def __rmul__(self, first):
			return self.__rmatmul__(first)

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	@property
	def classname(cls):
		return cls.getClassName()

	def getArray(self):
		return self._pt

	@property
	def array(self):
		return self.getArray()

	@array.setter
	def array(self, second):
		self.set(second)

	def get(self):
		return self.array()

	def getPoint(self, index=None):
		if (index is None):
			return getPoints()
		else:
			return self._pt[index]

	@property
	def point0(self):
		return self.getPoint(0)

	@property
	def point1(self):
		return self.getPoint(1)

	@property
	def p0(self):
		return self.getPoint(0)

	@property
	def p1(self):
		return self.getPoint(1)

	def getPoints(self):
		return self.array()

	@property
	def points(self):
		return self.getPoints()

	def getOrigin(self):
		return self._pt[0]

	@property
	def origin(self):
		return self.getOrigin()

	@property
	def orig(self):
		return self.getOrigin()

	def getVector(self):
		return self._pt[1] - self._pt[0]

	@property
	def vector(self):
		return self.getVector()

	@property
	def vec(self):
		return self.getVector()

	@property
	def v(self):
		return self.getVector()

	def getLength(self):
		return np.linalg.norm(self.getVector())

	@property
	def length(self):
		return self.getLength()

	@property
	def len(self):
		return self.getLength()

	@property
	def l(self):
		return self.getLength()

	def getDirection(self):
		return vecnormalize(self.getVector())

	@property
	def direction(self):
		return self.getDirection()

	@property
	def direct(self):
		return self.getDirection()

	def set(self, p1, p2=None):
		if (p2 is None):
			if (type(p1) is list or type(p1) is tuple):
				if (len(p1) == 2):
					p2 = p1[1]
					p1 = p1[0]
				else:
				 	___ERROR___
			else:
			 	___ERROR___
		if (type(p1) is np.ndarray):
			pass
		elif (type(p1) is list or type(p1) is tuple):
			p1 = np.array(p1)
		else:
			___ERROR___
		if (type(p2) is np.ndarray):
			pass
		elif (type(p2) is list or type(p2) is tuple):
			p2 = np.array(p2)
		else:
			___ERROR___
		self._pt = [p1, p2]

	def setPoints(self, pts):
		self._pt = pts

	@points.setter
	def points(self, pts):
		self.setPoints(pts)

	def setPoint(self, index, pt):
		self._pt[index] = pt

	def setPoint0(self, p):
		self.setPoint(0, pt)

	def setPoint1(self, p):
		self.setPoint(1, pt)

	@point0.setter
	def point0(self, pt):
		self.setPoint0(pt)

	@point1.setter
	def point1(self, pt):
		self.setPoint1(pt)

	@p0.setter
	def p0(self, pt):
		self.setPoint0(pt)

	@p1.setter
	def p1(self, pt):
		self.setPoint1(pt)

	def setOrigin(self, p):
		self.setPoint0(p)

	@origin.setter
	def origin(self, p):
		self.setOrigin(p)

	@orig.setter
	def orig(self, p):
		self.setOrigin(p)

	def setVector(self, v):
		self._pt[1] = self._pt[0] + v

	@vector.setter
	def vector(self, v):
		self.setVector(v)

	@vec.setter
	def vec(self, v):
		self.setVector(v)

	@v.setter
	def v(self, vec):
		self.setVector(v)

	def setLength(self, len):
		self.setVector(len * self.getDirection())

	@length.setter
	def length(self, len):
		self.setLength(len)

	@len.setter
	def len(self, len):
		self.setLength(len)

	@l.setter
	def l(self, len):
		self.setLength(len)

	def getMultiplied(self, r):
		if (type(r) is csrot3d):
			return self.getMultiplied(r.getMatrix())
		elif (type(r) is cstrans3d):
			return self.getMultiplied(r.getMatrix())
		elif (type(r) is list or type(r) is tuple):
			return self.getMultiplied(np.array(r))
		elif (type(r) is np.ndarray):
			if (r.ndim == 2):
				if (r.shape == (3, 3)):
					p0 = r @ self._pt[0]
					p1 = r @ self._pt[1]
					return line3d(p0, p1)
				elif (r.shape == (4, 4)):
					p0 = vec3(r @ vec4(self._pt[0]))
					p1 = vec3(r @ vec4(self._pt[1]))
					return line3d(p0, p1)
				else:
					___ERROR___
			else:
				___ERROR___
		else:
			___ERROR___

	def multiplied(self, r):
		return self.getMultiplied(r)

	def getRotated(self, r):
		if (type(r) is csrot3d):
			return self.getMultiplied(r.getMatrix())
		elif (type(r) is cstrans3d):
			return self.getMultiplied(r.getMatrix())
		elif (type(r) is list or type(r) is tuple):
			return self.getMultiplied(np.array(r))
		elif (type(r) is np.ndarray):
			if (r.shape == (3, 3)):
				p0 = r @ self._p[0]
				p1 = r @ self._p[1]
				return line3d(p0, p1)
			elif (r.shape == (4, 4)):
				r = to3x3(r)
				p0 = r @ self._p[0]
				p1 = r @ self._p[1]
				return line3d(p0, p1)
			else:
				___ERROR___
		else:
			___ERROR___

	def rotated(self, r):
		return getRotated(r)

	def getTranslated(self, t):
		if (type(t) is cstrans3d):
			return self.getTranslated(t.getTranslation())
		elif (type(t) is list or type(t) is tuple):
			return self.getTranslated(np.array(t))
		elif (type(t) is np.ndarray):
			p0 = self._p[0] + t
			p1 = self._p[1] + t
			return line3d(p0, p1)
		else:
			___ERROR___

	def translated(self, t):
			return self.getTranslated(t)

	def getTransformed(self, t):
		return self.getMultiplied(t)

	def transformed(self, t):
		return self.getTransformed(t)

	def getPrintStr(self, title=None):
		if (title is None):
			mesg = ''
		else:
			mesg = title + ': '
		p0 = self._pt[0]
		p1 = self._pt[1]
		mesg += "({0: .3f}, {1: .3f}, {2: .3f}) - ({3: .3f}, {4: .3f}, {5: .3f})".format(p0[0], p0[1], p0[2], p1[0], p1[1], p1[2])
		return mesg

	@property
	def printstr(self):
		return self.getPrintStr()

	@property
	def str(self):
		return self.getPrintStr()

	def print(self, title=None):
		print(self.getPrintStr(title))

	def getDataStr(self):
		return '{0:21.12f}, {1:21.12f}, {2:21.12f}, {3:21.12f}, {4:21.12f}, {5:21.12f}\n'.format(
		self._pt[0][0], self._pt[0][1], self._pt[0][2],
		self._pt[1][0], self._pt[1][1], self._pt[1][2])

	@property
	def datastr(self):
		return self.getDataStr()

	def setDataStr(self, s):
		s = s.split(',')
		for i in range(len(s)):
			s[i] = float(s[i].strip())
		self.set([(s[0], s[1], s[2]), (s[3], s[4], s[5])])

	@datastr.setter
	def datastr(self, s):
		return setDataStr(s)

	def load(self, filename):
		with open(filename, 'r') as f:
			self.setDataStr(f.read())

	def save(self, filename):
		with open(filename, 'w') as f:
			f.write(self.getDataStr())
"""
#----------------- ここまでコメントアウト -----------------------------


_DEFAULT_PLANE3D_ORIGIN = [0.0, 0.0, 0.0]
_DEFAULT_PLANE3D_NORMAL = [0.0, 0.0, 1.0]

class plane3d(line3d):
	_classname = 'nkj.math.plane3d'
	_componentclass = point3d

	def __init__(self, origin=None, normal=None):
		if (origin is None and normal is None):
			origin = _DEFAULT_PLANE3D_ORIGIN
			normal = _DEFAULT_PLANE3D_NORMAL
		self.set(origin, normal)
	
	def __str__(self, title=None):
		return self.getPrintStr(title)

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	def getComponentClass(cls):
		return cls._componentclass

	def getOrigin(self):
		return self._origin

	@property
	def origin(self):
		return self.getOrigin()

	@property
	def orig(self):
		return self.getOrigin()

	def getNormal(self):
		return self._normal

	@property
	def normal(self):
		return self.getNormal()

	@property
	def n(self):
		return self.getNormal()

	def getVector(self):
		return self.getNormal()

	@property
	def vector(self):
		return self.getNormal()

	@property
	def v(self):
		return self.getNormal()

	def set(self, origin, normal=None):
		if (normal is None):
			if (type(origin) is list or type(origin) is tuple):
				if (len(origin) == 2):
					normal = origin[1]
					origin = origin[0]
				else:
				 	___ERROR___
			else:
			 	___ERROR___
		if (type(origin) is np.ndarray):
			pass
		elif (type(origin) is list or type(origin) is tuple):
			origin = np.array(origin)
		else:
			___ERROR___
		if (type(normal) is np.ndarray):
			pass
		elif (type(normal) is list or type(normal) is tuple):
			normal = np.array(normal)
		else:
			___ERROR___
		self._origin = origin
		self._normal = vecnormalize(normal)

	def setOrigin(self, origin):
		self._origin = origin

	@origin.setter
	def origin(self, origin):
		self.setOrigin(origin)

	@orig.setter
	def orig(self, origin):
		self.setOrigin(origin)

	def setNormal(self, normal):
		self._normal = normal

	@normal.setter
	def normal(self, n):
		self.setNormal(n)

	@n.setter
	def n(self, normal):
		self.setNormal(normal)

	def getMultiplied(self, r):
		if (type(r) is csrot3d):
			return self.getMultiplied(r.getMatrix())
		elif (type(r) is cstrans3d):
			return self.getMultiplied(r.getMatrix())
		elif (type(r) is list or type(r) is tuple):
			return self.getMultiplied(np.array(r))
		elif (type(r) is np.ndarray):
			if (r.ndim == 2):
				if (r.shape == (3, 3)):
					origin = r @ self._origin
					normal = r @ self._normal
					return plane3d(origin, normal)
				elif (r.shape == (4, 4)):
					origin = vec3(r @ vec4(self._origin))
					normal = to3x3(r) @ self._normal
					return plane3d(origin, normal)
				else:
					___ERROR___
			else:
				___ERROR___
		else:
			___ERROR___

	def multiplied(self, r):
		return self.getMultiplied(r)

	def getRotated(self, r):
		if (type(r) is csrot3d):
			return self.getMultiplied(r.getMatrix())
		elif (type(r) is cstrans3d):
			return self.getMultiplied(r.getMatrix())
		elif (type(r) is list or type(r) is tuple):
			return self.getMultiplied(np.array(r))
		elif (type(r) is np.ndarray):
			if (r.shape == (3, 3)):
				normal = r @ self._normal
				return plane3d(self._origin, normal)
			elif (r.shape == (4, 4)):
				m = to3x3(r)
				normal = m @ self._normal
				return plane3d(self._origin, normal)
			else:
				___ERROR___
		else:
			___ERROR___

	def rotated(self, r):
		return getRotated(r)

	def getTranslated(self, t):
		if (type(t) is cstrans3d):
			return self.getTranslated(t.getTranslation())
		elif (type(t) is list or type(t) is tuple):
			return self.getTranslated(np.array(t))
		elif (type(t) is np.ndarray):
			origin = self._origin + t
			return plane3d(origin, self._normal)
		else:
			___ERROR___

	def translated(self, t):
			return self.getTranslated(t)

	def getTransformed(self, t):
		return self.getMultiplied(t)

	def transformed(self, t):
		return self.getTransformed(t)

	def getPrintStr(self, title=None):
		if (title is None):
			mesg = ''
		else:
			mesg = title + ': '
		mesg += "Origin: ({0: .3f}, {1: .3f}, {2: .3f}), Normal: ({3: .3f}, {4: .3f}, {5: .3f})".format(self._origin[0], self._origin[1], self._origin[2], self._normal[0], self._normal[1], self._normal[2])
		return mesg

	@property
	def printstr(self):
		return self.getPrintStr()

	@property
	def str(self):
		return self.getPrintStr()

	def print(self, title=None):
		print(self.getPrintStr(title))

	def getDataStr(self):
		return '{0:21.12f}, {1:21.12f}, {2:21.12f}, {3:21.12f}, {4:21.12f}, {5:21.12f}\n'.format(
		self._origin[0], self._origin[1], self._origin[2], self._normal[0], self._normal[1], self._normal[2])

	@property
	def datastr(self):
		return self.getDataStr()

	def setDataStr(self, s):
		s = s.split(',')
		for i in range(len(s)):
			s[i] = float(s[i].strip())
		self.set([(s[0], s[1], s[2]), (s[3], s[4], s[5])])

	@datastr.setter
	def datastr(self, s):
		return setDataStr(s)

	def load(self, filename):
		with open(filename, 'r') as f:
			self.setDataStr(f.read())

	def save(self, filename):
		with open(filename, 'w') as f:
			f.write(self.getDataStr())


#-- list -------------------------------------------------------------

class list_cls(list):
	_classname = 'nkj.math.list'
	_componentclass = None

	def __init__(self, l=None):
		super().__init__()
		self.set(None if (l is None) else l)

	def __str__(self):
		return self.getStr()

	# classname

	@classmethod
	def getClassName(cls):
		return cls._classname

	# component class

	@classmethod
	def getComponentClass(cls):
		return _componentclass

	@classmethod
	def getCompClass(cls):
		return cls.getComponentClass()

	@classmethod
	@property
	def componentclass(cls):
		return cls.getComponentClass()

	@classmethod
	@property
	def compclass(cls):
		return cls.componentclass

	@classmethod
	def getComponentType(cls):
		return cls.getComponentClass()

	@classmethod
	def getCompType(cls):
		return cls.getComponentType()

	@classmethod
	@property
	def componenttype(cls):
		return cls.getComponentType()

	@classmethod
	@property
	def comptype(cls):
		return cls.componenttype

	# get, set

	def get(self, index=None):
		return self if (index is None) else self[index]

	def set(self, l=None):
		super().clear()
		if (l is None):
			pass
		elif (isinstance(l, list) or isinstance(l, tuple)):
			self.extend(list(l))
		else: # リストでなく、要素が入力された
			self.append(l)

	# list length

	def getListLength(self):
		return len(self)

	def getLength(self):
		return self.getListLength()

	@property
	def listlength(self):
		return self.getListLength()

	@property
	def length(self):
		return self.getListLength()

	@property
	def len(self):
		return self.getListLength()

	@property
	def l(self):
		return self.getListLength()

	# array

	def getArray(self):
		outarray = []
		for i in range(len(self)):
			outarray.append(self[i].getArray())
		return np.array(outarray, dtype=np.float32)

	@property
	def array(self):
		return self.getArray()

	# list

	def getList(self):
		outlist = []
		for i in range(len(self)):
			outlist.append(copy.deepcopy(self[i]))
		return outlist

	@property
	def list(self):
		return self.getList()

	# list operations

	def append(self, x):
		ldprint('--> nkj.math.primlist.append()')
		if (x is None):
			__ERROR__
		elif (isinstance(x, self.componentclass)):
			ldprint2('class: {}'.format(self.componentclass))
			ldprint2('type:  {}'.format(type(x)))
			super().append(copy.deepcopy(x))
		elif (isinstance(x, list) or isinstance(x, tuple) or isinstance(x, np.ndarray)):
			super().append(self.componentclass(x))
		else:
			___ERROR___
		ldprint('<-- nkj.math.primlist.append()')

	def extend(self, l):
		if (l is None):
			__ERROR__
		elif (isinstance(l, list) or isinstance(l, tuple)):
			for x in l:
				self.append(copy.deepcopy(x))
		else:
			___ERROR___

	# string

	def getStr(self):
		listlen = self.getListLength()
		s = ''
		for i in range(listlen):
			s += '{0}'.format(self[i].getStr())
			if (i < listlen - 1):
				s += '\n'
		return s

	@property
	def str(self):
		return self.getStr()

	def getDataStr(self):
		listlen = self.getListLength()
		s = ''
		for i in range(listlen):
			s += '{0}'.format(self[i].getDataStr())
			if (i < listlen - 1):
				s += '; '
		return s

	@property
	def datastr(self):
		return self.getDataStr()

	# print

	def getPrintString(self, title=None):
		if (title is None):
			s = '-- [{0}] --\n'.format(listlen)
		else:
			s = '-- {0}[{1}] --\n'.format(title, self.getListLength())
		s += self.getStr()
		s += '\n--'
		return s

	def getPrintStr(self, title=None):
		return self.getPrintString(title)

	@property
	def printstr(self):
		return self.getPrintStr()

	def print(self, title=None):
		print(self.getPrintString(title), flush=True)

	# load, save

	def load(self, filename):
		if (self.componentclass is None):
			__ERROR__
		x = self.componentclass()
		with open(filename, 'r') as f:
			s = f.read()
			s = s.strip()
			s = s.split('\n')
			self.clear()
			for linestr in s:
				x.setDataStr(linestr)
				self.append(copy.deepcopy(x))

	def save(self, filename):
		with open(filename, 'w') as f:
			for i in range(self.getListLength()):
				x = self[i]
				if (is_geometric(x)):
					f.write(x.getDataStr())
				else:
					f.write('{0}\n'.format(x))

class nlist(list_cls):
	pass

class primlist(list_cls):
	pass


#-- primitive list

"""
class point2dlist(primlist):
	_classname = 'nkj.math.point2dlist'
	_componentclass = point2d

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	def getComponentClass(cls):
		return cls._componentclass


class line2dlist(primlist):
	_classname = 'nkj.math.line2dlist'
	_componentclass = line2d

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	def getComponentClass(cls):
		return _componentclass
"""


class point3dlist(primlist):
	_classname = 'nkj.math.point3dlist'
	_componentclass = point3d

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	def getComponentClass(cls):
		return cls._componentclass

class pointlist(point3dlist):
	pass


class line3dlist(primlist):
	_classname = 'nkj.math.line3dlist'
	_componentclass = line3d

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	def getComponentClass(cls):
		return _componentclass

class linelist(line3dlist):
	pass


class plane3dlist(primlist):
	_classname = 'nkj.math.plane3dlist'
	_componentclass = plane3d

	@classmethod
	def getClassName(cls):
		return cls._classname

	@classmethod
	def getComponentClass(cls):
		return _componentclass

class planelist(plane3dlist):
	pass


#-- main

if (__name__ == '__main__'):
	import nkj.str as ns

	ns.lib_debuglevel(_LIB_DEBUGLEVEL)

	if (False):
		print("===== angle =====")


	if (True):
		print("\n===== complex =====")

		c = complex(1, 2)
		print('classname: \'{}\''.format(c.classname))
		print(c)

		print(c.normalized())
		print(normalized(c))

		print(c.conjugated())
		print(conjugated(c))

		c[0] = 10
		c[1] = 20
		print(c)

		c2 = complex(1, 3)
		print(c2)
		print(c * c2)

	if (False):
		print("===== quaternion =====")


	if (False):
		print("===== csrot3d =====")

		theta = 90 # degrees
		v = np.array([0, 0, 1])

		theta = theta / 180 * np.pi # degrees to rad
		hftheta = theta / 2
		c = np.cos(hftheta)
		s = np.sin(hftheta)
		r3 = csrot3d([c, s * v[0], s * v[1], s * v[2]])

		print("r3.w:  {0}".format(r3.w))
		print("r3.x:  {0}".format(r3.x))
		print("r3.y:  {0}".format(r3.y))
		print("r3.z:  {0}".format(r3.z))

		print("r3.rx: {0}".format(r3.rx))
		print("r3.ry: {0}".format(r3.ry))
		print("r3.rz: {0}".format(r3.rz))

		print("quat:    {0}".format(r3.quat))
		print("np.quat: {0}".format(r3.npquat))
		print("np.quat: {0} (array)".format(r3.npquatarray))
		print("R.quat:  {0}".format(r3.rquat))
		print("R.quat:  {0} (array)".format(r3.rquatarray))

		print("--- csrot3d.matrix ---")
		print(r3.matrix)
		print("---")


	if (False):
		print("===== cstrans3d =====")

		theta = 90.0 # degrees
		rv = np.array([0, 0, 1])
		tv = np.array([2, 3, 4])

		theta = theta / 180.0 * np.pi # deg 2 rad
		hftheta = theta / 2.0
		c = np.cos(hftheta)
		s = np.sin(hftheta)

		t = cstrans3d([np.array([c, s * rv[0], s * rv[1], s * rv[2]]), tv])
		t.print("cstrans3d")
		print("--- matrix ---")
		print(t.matrix)
		print("---")
		print("--- rotmat ---")
		print(t.rotmat)
		print("---")
		print("translation vector: {0}".format(t.trans))

		t_i = t.inv
		t_i.print("inversed")
		print("--- inversed matrix ---")
		print(t_i.matrix)
		print("---")

		t2 = t @ t_i
		print("--- matrix ---")
		print(t2.matrix)
		print("---")
		mat4x4(t2).print('test matrix')

		t3 = t_i @ t
		print("--- matrix ---")
		print(t3.matrix)
		print("---")
		mat4x4(t3).print('test matrix')


	if (False):
		print("===== matrix =====")

		a = np.array([[1, 0], [0, 2]])
		print(a)
		print(type(a))

		m = mat4x4()
		print("class name: ", str_bracket(m.getClassName()))
		print("type:       ", type(m))
		print("dimension:  ", m.dim())
		print("size:       ", m.size())
		m.print("m")
		print("--- m.array() ---")
		print(m.array())
		print("---")

		m.array()[0][1] = 3.0
		print(m)

		m2 = mat4x4()

		print(m @ m2)

		m3 = m @ m2
		print(m3)

		m3.getInversed().print('inversed')

		m3.print('original')

		m4 = mat4x4(m3.get())
		m4.print('m4')

		"""
		m5 = mat4x4(np.array([deg2rad(30), 0, 0, 1]))
		m5.print('m5')
		"""

		(~m3).print('invert')

		(~m3 * m3).print('validation')
		(~m3 @ m3).print('validation')

		m3.inverse()
		m3.print('inverse')

		m3.identity()
		m3.print('identity')

	if (False):
		print("===== sigmoid =====")
		import matplotlib.pyplot as plt

		x = np.arange(-10, 10, 0.1)
		ta = 1.0
		x0 = 2.5
		#y = sigmoid(x, tau=tau, x0=x0)
		y = sigmoid(x, x0=x0)
		plt.plot(x, y)
		plt.show()


	if (False):
		print("===== log ticks =====")

		ticks = logticks(0.01, 2.0)
		print(ticks)


	if (False):
		print("===== vec3d =====")

		print(vec3d())

		v = vec3d(np.array([1, 0, 0]))
		print(v)

		v0 = vec3d(np.array([0, 1, 0]))

		print("angle: {0} degrees".format(rad2deg(angle(v0, v))))


	if (True):
		print("===== point3d =====")

		print(point3d())

		p = point3d(np.array([1, 1, 2]))
		print(p)


	if (False):
		print("===== line3d =====")

		print(line3d())

		l = line3d(np.array([0, 0, 0]), np.array([0, 0, 100]))
		l.print('line3d')
		print('origin: {0}'.format(l.getOrigin()))
		print('length: {0}'.format(l.getLength()))
		print('vector: {0}'.format(l.getVector()))
		print('direction: {0}'.format(l.getDirection()))

		l2 = line3d([[1, 1, 1], [2, 2, 2]])
		l2.print('line3d 2')

		theta = deg2rad(90)
		t = cstrans3d()
		ver = 1
		if (ver == 1):
			t.rotateGlobal([deg2rad(45), (0, 1, 0)], 'angleaxis')
			t.rotateGlobal([deg2rad(theta), (0, 0, 1)], 'angleaxis')
		elif (ver == 2):
			t.rotateGlobal([deg2rad(45), (np.cos(theta), np.sin(theta), 0)], 'angleaxis')
		else:
			___ERROR___
		t.print('transformation')
		#l2 = l.transformed(t)
		l2 = t @ l
		l2.print('line3d (transformed)')

		l2.save('testdata/test.line')
		l2.load('testdata/test.line')
		l2.print('reload')

		#-- direction cosine test

		xlist = []
		zlist = []
		philist = []
		thetalist = []
		for zdeg in range(-90, 91, 5):
			ztheta = deg2rad(zdeg)
			for xdeg in range(-90, 91, 5):
				xtheta = deg2rad(xdeg)
				dprint('ztheta:{0:.3f}, xtheta:{1:.3f}'.format(rad2deg(ztheta), rad2deg(xtheta)))
				phi = np.sqrt(ztheta**2 + xtheta**2)
				if (phi > np.pi / 2):
					phi = np.pi - phi
				dprint('phi:{0:.3f}'.format(rad2deg(phi)))
				c_phi = np.cos(phi)
				s_phi = np.sin(phi)
				theta = np.arctan2(ztheta, xtheta)
				c = s_phi * np.cos(theta)
				s = s_phi * np.sin(theta)
				dprint([c, c_phi, s])
				r = csrot3d([c, c_phi, s], 'dircos', [0, 1, 0])
				#r.print('direction cosine')
				xlist.append(xdeg)
				zlist.append(zdeg)
				philist.append(rad2deg(phi))
				thetalist.append(theta)
		xlist = np.array(xlist)
		zlist = np.array(zlist)
		philist = np.array(philist)
		thetalist = np.array(thetalist)

		ticks = int(np.sqrt(len(xlist)))
		xlist = xlist.reshape(ticks, ticks)
		zlist = zlist.reshape(ticks, ticks)
		philist = philist.reshape(ticks, ticks)
		thetalist = thetalist.reshape(ticks, ticks)
		dprint('xlist[{0}]: {1}'.format(len(xlist), xlist))
		dprint('zlist[{0}]: {1}'.format(len(zlist), zlist))
		dprint('philist[{0}]: {1}'.format(len(philist), philist))

		from matplotlib import pyplot as plt

		plt.pcolor(xlist, zlist, philist, cmap='inferno', vmin=0, vmax=90)
		""" #--- colormaps
		plt.pcolor(xlist, zlist, philist, cmap='plasma', vmin=0, vmax=90)
		plt.pcolor(xlist, zlist, philist, cmap='bwr', vmin=0, vmax=90)
		plt.pcolor(xlist, zlist, philist, cmap='coolwarm', vmin=0, vmax=90)
		plt.pcolor(xlist, zlist, philist, cmap='seismic', vmin=0, vmax=90)
		plt.pcolor(xlist, zlist, philist, cmap='RdYlBu_r', vmin=0, vmax=90)
		plt.pcolor(xlist, zlist, thetalist)
		"""
		plt.xticks([-90, -60, -30, 0, 30, 60, 90], fontsize=15)
		plt.yticks([-90, -60, -30, 0, 30, 60, 90], fontsize=15)
		plt.xlabel('Angle of x direction cosine', fontsize=18)
		plt.ylabel('Angle of z direction cosine', fontsize=18)
		plt.tight_layout()   # フォントサイズを変更したとき、図で文字が見切れないように調整する。
		colorbar_ticks = np.linspace(0, 90, 7, endpoint=True)
		if (True):
			cb = plt.colorbar(ticks=colorbar_ticks)
			for t in cb.ax.get_yticklabels():
				t.set_fontsize(12)
		else:
			plt.colorbar(ticks=colorbar_ticks)
		plt.savefig('testdata/test.png')
		plt.show()


	if (False):
		print("===== plane3d =====")

		pl = plane3d(np.array([0, 0, 0]), np.array([0, 0, 100]))
		pl.print('plane3d')

		pl2 = plane3d([np.array([0, 0, 0]), np.array([0, 10, 0])])
		pl2.print('plane3d 2')

		pl3 = plane3d([[0, 0, 0], [1, 1, 0]])
		pl3.print('plane3d 3')

		print('{0} degree'.format(rad2deg(angle(pl, pl2))))
		print('{0} degree'.format(rad2deg(angle(pl2, pl3))))

		theta = deg2rad(45)
		phi = deg2rad(45)
		print('theta:{0:.3f}, phi:{1:.3f}'.format(rad2deg(theta), rad2deg(phi)))
		t = cstrans3d()
		ver = 2
		if (ver == 1):
			t.rotateGlobal([phi, (np.cos(theta), np.sin(theta), 0)], 'angleaxis')
		elif (ver == 2):
			t.rotateGlobal([phi, (1, 0, 0)], 'angleaxis')
			t.rotateGlobal([theta, (0, 0, 1)], 'angleaxis')
		else:
			___ERROR___
		t.translateGlobal([10, 10, 0])
		t.print('transformation')
		pl2 = t @ pl
		pl2.print('plane3d (transformed)')

		pl2.save('testdata/test.plane')
		pl2.load('testdata/test.plane')
		pl2.print('reload')


	if (False):
		print("===== primlist =====")

		ls = primlist()
		ls.print('primlist')

		ls.append('test')
		ls.append('test2')
		ls.print('primlist')

		ls.set(['test3'])
		ls.print('primlist (test 3)')

		ls.clear()
		ls.print('primlist')

		ls.clear()
		ls.append([1, 2, 3])  # リストを一要素として追加
		ls.extend([3, 4, 5])  # 要素をリストで追加
		ls.save('testdata/test.list')
		ls.load('testdata/test.list')
		ls.print('primlist')


	"""
	if (False):
		print("===== vec3dlist =====")

		ls = vec3dlist()
		ls.append([0, 1, 2])
		ls.append([3, 4, 5])
		ls.extend([[6, 7, 8], [9, 10, 11]])
		ls.print('vec3dlist')
		ls.save('testdata/test.pts')
		ls.load('testdata/test.pts')
		ls.print('vec3dlist')
	"""

	if (False):
		print("===== point3dlist =====")

		ls = point3dlist()
		ls.append([0, 1, 2])
		ls.append([3, 4, 5])
		ls.extend([[6, 7, 8], [9, 10, 11]])
		ls.print('point3dlist')
		ls.save('testdata/test.pts')
		ls.load('testdata/test.pts')
		ls.print('point3dlist')


	if (False):
		print("===== line3dlist =====")

		ls = line3dlist()
		ls.append(line3d([0, 1, 2], [0, 1, 0]))
		ls.append(line3d([3, 4, 5], [3, 4, 0]))
		ls.print('line3dlist')
		ls.save('testdata/test.lines')
		ls.load('testdata/test.lines')
		ls.print('line3dlist')


	if (False):
		print("===== plane3dlist =====")

		ls = plane3dlist()
		ls.append(plane3d([0, 1, 2], [0, 1, 0]))
		ls.append(plane3d([3, 4, 5], [3, 4, 0]))
		ls.extend(copy(ls))
		ls.print('plane3dlist')
		ls.save('testdata/test.planes')
		ls.load('testdata/test.planes')
		ls.print('plane3dlist')
