import css_structure
import re
import stylesheet_reader
import stylesheet_writer

class StyleSheet(css_structure.CssStructure):

	def __init__(self):
		self.mediaqueries = []
		self.rules = []
		self.tokens = []
	
	# ------------- factory methods -------------

	@classmethod
	def from_string(cls, text):
		return stylesheet_reader.StyleSheetReader.read_string(text)

	@classmethod
	def from_file(cls, filepath):
		return stylesheet_reader.StyleSheetReader.read_filepath(filepath)
	
	# ------------- public -------------

	def set_tokens(self, tokens):
		self.tokens = tokens
	
	def set_mediaqueries(self, mediaqueries):
		self.mediaqueries = mediaqueries
	
	def add_token(self, token):
		self.tokens.append(token)

	def set_rules(self, rules):
		self.rules = rules
	
	def remove_rule(self, rule):
		i = self.rules.index(rule)
		self.rules.pop(i)
		firsttoken = rule.get_tokens()[0]
		numtokens = len(rule.get_tokens())
		i = self.tokens.index(firsttoken)
		for x in xrange(0, numtokens):
			self.tokens.pop(i)

	def get_rules(self, query=None):
		if query:
			return self._get_rules_by_query(query)
		return self.rules

	def prepend_rule(self, newrule, existingrule=None):
		if existingrule:
			self._insert_rule_before(newrule, existingrule)
		else:
			self.tokens = newrule.get_tokens() + self.tokens
			self.rules.insert(0, newrule)

	def append_rule(self, newrule, existingrule=None):
		if existingrule:
			self._insert_rule_after(newrule, existingrule)
		else:
			self.tokens += newrule.get_tokens()
			self.rules.append(newrule)
	
	def to_string(self):
		return str(self)

	def to_file(self, filepath):
		stylesheet_writer.StyleSheetWriter.write_filepath(self, filepath)

	# ------------- private -------------

	def _insert_rule_before(self, new, existing):
		insertbefore = existing
		if new.get_mediaquery() != existing.get_mediaquery():
			insertbefore = existing.get_mediaquery()
		self._insert_tokens_before(new, insertbefore)
		i = self.rules.index(existing)
		self.rules.insert(i, new)
	
	def _insert_rule_after(self, newrule, existingrule):
		insertafter = existingrule
		if newrule.get_mediaquery() != existingrule.get_mediaquery():
			insertafter = existingrule.get_mediaquery()
		self._insert_tokens_after(newrule, insertafter)
		i = self.rules.index(existingrule)
		self.rules.insert(i, newrule)
	
	def _get_rules_by_query(self, query):
		query = re.sub(r'\s+', ' ', query)
		matches = []
		for rule in self.rules:
			if self._query_rule(query, rule):
				matches.append(rule)
		return matches

	def _query_rule(self, query, rule):
		for selector in self._split_selector(rule.get_selector()):
			if query == selector:
				return True
		return False

	def _split_selector(self, selector):
		return [s.strip() for s in selector.split(',')]
	
