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

	def to_string(self, indent=None):
		if indent:
			return self._to_string_pretty(indent)
		tokens = [t for t in self.tokens]
		if self.mediaquery:
			m = self.mediaquery
			tokens = m.get_starttokens() + tokens + m.get_endtokens()
		return ''.join([str(t) for t in tokens])

	def _to_string_pretty(self, indent):
		self._indent = indent
		pieces = []
		if self.mediaquery:
			pieces += self.mediaquery.get_starttokens()
		pieces += self.tokens
		if self.mediaquery:
			pieces += self.mediaquery.get_endtokens()
		txt =  ''.join([str(p) for p in pieces])
		txt = re.sub(r'\s', '', txt)
		txt = re.sub(r'\{', ' {\n', txt)
		txt = re.sub(r';', ';\n', txt)
		txt = re.sub(r'(\{)(.*)(\n\})', self._indentify, txt, flags=re.DOTALL)
		return txt

	def _indentify(self, match):
		inner = re.sub(r'\n', '\n%s'%(self._indent), match.group(2))
		return match.group(1) + inner + match.group(3)

	def __str__(self):
		return ''.join([str(t) for t in self.tokens])
