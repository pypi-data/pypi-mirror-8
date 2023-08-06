"""
Minimal Py2/Py3 compatibility library.
"""
import sys
PY3 = sys.version > '3'


if PY3:
	maketrans = bytes.maketrans
	basestring = str
	zip = zip

	def bytes_to_str(s):
		return s.decode('ascii')

	def str_to_bytes(s):
		return s.encode('ascii')

	def force_str(s):
		if isinstance(s, (bytes, bytearray)):
			return s.decode('ascii')
		else:
			return s

else:
	def bytes_to_str(s):
		return s

	def str_to_bytes(s):
		return s

	def force_str(s):
		return s

	from string import maketrans
	basestring = basestring
	from itertools import izip as zip
