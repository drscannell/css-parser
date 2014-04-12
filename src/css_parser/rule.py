import css_structure
import re
import stylesheet_reader

class Rule(css_structure.CssStructure):
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
		txt = ''.join([str(t) for t in self.selector_tokens])
		return re.sub('\s+', ' ', txt).strip()

	def get_declarations(self, query=None):
		if query:
			return self._get_declarations_by_query(query)
		return self.declarations

	def remove_declaration(self, decl):
		i = self.declarations.index(decl)
		self.declarations.pop(i)
		decl.remove()

	def append_declaration(self, new, existing=None):
		if existing:
			self._insert_decl_after(new, existing)
		else:
			last = self.declarations[-1]
			lasttoken = last.get_tokens()[-1]
			i = self.tokens.index(lasttoken) + 1
			for t in reversed(new.get_tokens()):
				self.tokens.insert(i, t)
			self.declarations.append(new)

	def get_mediaquery(self):
		return self.mediaquery

	def to_string(self):
		tokens = [t for t in self.tokens]
		if self.mediaquery:
			m = self.mediaquery
			tokens = m.get_starttokens() + tokens + m.get_endtokens()
		return ''.join([str(t) for t in tokens])

	# ------------- private -------------

	def _get_declarations_by_query(self, query):
		matches = []
		for declaration in self.declarations:
			if declaration.get_property().strip() == query.strip():
				matches.append(declaration)
		return matches

	def _insert_decl_after(self, new, existing):
		self._insert_tokens_after(new, existing)
		i = self.declarations.index(existing)
		self.declarations.insert(i, new)





