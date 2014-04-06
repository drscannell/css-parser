import re
import stylesheet_reader

class Rule:
	def __init__(self, tokens=[]):
		self.tokens = tokens
		self.selector_tokens = []
		self.declarations = []
		self.mediaquery = None

	@classmethod
	def from_string(cls, text):
		stylesheet = stylesheet_reader.StyleSheetReader.read_string(text)
		if len(stylesheet.get_rules()) == 1:
			return stylesheet.get_rules()[0]
		if len(stylesheet.get_rules()) > 1:
			return stylesheet.get_rules()
		return None
	
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

	def get_declarations(self, query=None):
		if query:
			return self._get_declarations_by_query(query)
		return self.declarations

	def _get_declarations_by_query(self, query):
		matches = []
		for declaration in self.declarations:
			if declaration.get_property().strip() == query.strip():
				matches.append(declaration)
		return matches

	def remove_declaration(self, decl):
		i = self.declarations.index(decl)
		self.declarations.pop(i)
		decl.remove()

	def append_declaration(self, newdecl, existingdecl=None):
		if existingdecl:
			raise Exception('not implemented')
		else:
			lastdecl = self.declarations[-1]
			lasttoken = lastdecl.get_tokens()[-1]
			i = self.tokens.index(lasttoken) + 1
			for t in reversed(newdecl.get_tokens()):
				self.tokens.insert(i, t)
			self.declarations.append(newdecl)


	def get_mediaquery(self):
		return self.mediaquery

	def stringify_tokens(self, tokens):
		txt = ''.join([str(t) for t in tokens])
		return re.sub('\s+', ' ', txt).strip()

	def to_string(self):
		tokens = [t for t in self.tokens]
		if self.mediaquery:
			m = self.mediaquery
			tokens = m.get_starttokens() + tokens + m.get_endtokens()
		return ''.join([str(t) for t in tokens])

	def __str__(self):
		return ''.join([str(t) for t in self.tokens])
