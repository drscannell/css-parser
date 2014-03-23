import re

class Rule:
	def __init__(self, tokens=[]):
		self.tokens = tokens
		self.selector_tokens = []
		self.declarations = []
		self.mediaquery = None
	
	def set_selector_tokens(self, tokens):
		self.selector_tokens = tokens
	
	def set_declarations(self, declarations):
		self.declarations = declarations
	
	def set_mediaquery(self, mediaquery):
		self.mediaquery = mediaquery
	
	def get_tokens(self):
		return self.tokens

	def get_selector(self):
		return self.stringify_tokens(self.selector_tokens)

	def get_declarations(self):
		return self.declarations

	def get_mediaquery(self):
		return self.mediaquery

	def stringify_tokens(self, tokens):
		txt = ''.join([str(t) for t in tokens])
		return re.sub('\s+', ' ', txt).strip()

