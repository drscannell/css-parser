class Declaration:
	def __init__(self, tokens=[], prop='', val=''):
		self._tokens = tokens
		self._prop = prop
		self._val = val

	def get_tokens(self):
		return self._tokens

	def get_property(self):
		return self._prop

	def get_value(self):
		return self._val
