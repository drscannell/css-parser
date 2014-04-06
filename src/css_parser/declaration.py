import tokenizer
import declarationfactory

class Declaration:
	def __init__(self, tokens=[], prop='', val=''):
		self._tokens = tokens
		self._prop = prop
		self._val = val

	@classmethod
	def from_string(cls, text):
		tokens = tokenizer.Tokenizer.tokenize_string(text)
		return declarationfactory.DeclarationFactory.construct(tokens)

	def get_tokens(self):
		return self._tokens

	def get_property(self):
		return self._prop

	def get_value(self):
		return self._val

	def remove(self):
		for t in self.get_tokens():
			t.remove()
	
	def to_string(self):
		return str(self)
	
	def __str__(self):
		return ''.join(self.get_tokens())
