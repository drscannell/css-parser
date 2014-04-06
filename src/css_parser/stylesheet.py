import re

class StyleSheet:

	def __init__(self):
		self.mediaqueries = []
		self.rules = []
		self.tokens = []
	
	# ------------- public -------------
	
	def set_tokens(self, tokens):
		self.tokens = tokens
	
	def add_token(self, token):
		self.tokens.append(token)

	def set_rules(self, rules):
		self.rules = rules

	def prepend_rule(self, newrule, existingrule=None):
		if existingrule:
			self.insert_rule_before(newrule, existingrule)
		else:
			self.tokens = newrule.get_tokens() + self.tokens
			self.rules.insert(0, newrule)

	def append_rule(self, newrule, existingrule=None):
		if existingrule:
			self.insert_rule_after(newrule, existingrule)
		else:
			self.tokens += newrule.get_tokens()
			self.rules.append(newrule)

	# ------------- private -------------

	def insert_rule_before(self, newrule, existingrule):
		firsttoken = None
		if newrule.get_mediaquery() != existingrule.get_mediaquery():
			mediaquery = existingrule.get_mediaquery()
			firsttoken = mediaquery.get_starttokens()[0]
		else:
			firsttoken = existingrule.get_tokens()[0]
		self.insert_tokens_before(newrule.get_tokens(), firsttoken)
		i = self.rules.index(existingrule)
		self.rules.insert(i, newrule)
	
	def insert_rule_after(self, newrule, existingrule):
		lasttoken = None
		if newrule.get_mediaquery() != existingrule.get_mediaquery():
			mediaquery = existingrule.get_mediaquery()
			lasttoken = mediaquery.get_endtokens()[-1]
		else:
			existingruletokens = existingrule.get_tokens()
			lasttoken = existingruletokens[len(existingruletokens) - 1]
		self.insert_tokens_after(newrule.get_tokens(), lasttoken)
		i = self.rules.index(existingrule)
		self.rules.insert(i, newrule)
	
	def insert_tokens_before(self, tokens, token):
		i = self.tokens.index(token)
		for t in reversed(tokens):
			self.tokens.insert(i, t)
	
	def insert_tokens_after(self, tokens, token):
		if token == self.tokens[-1]:
			self.tokens += tokens
		else:
			i = self.tokens.index(token) + 1
			for t in reversed(tokens):
				self.tokens.insert(i, t)
	
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
			return self.get_rules_by_query(query)
		return self.rules

	def get_rules_by_query(self, query):
		query = re.sub(r'\s+', ' ', query)
		matches = []
		for rule in self.rules:
			if self.query_rule(query, rule):
				matches.append(rule)
		return matches

	def query_rule(self, query, rule):
		for selector in self.split_selector(rule.get_selector()):
			if query == selector:
				return True
		return False

	def split_selector(self, selector):
		return [s.strip() for s in selector.split(',')]
	
	def set_mediaqueries(self, mediaqueries):
		self.mediaqueries = mediaqueries
	
	def __str__(self):
		return ''.join([str(t) for t in self.tokens])
