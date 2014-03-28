class StyleSheet:

	def __init__(self):
		self.mediaqueries = []
		self.rules = []
		self.tokens = []
	
	def set_tokens(self, tokens):
		self.tokens = tokens
	
	def add_token(self, token):
		self.tokens.append(token)

	def set_rules(self, rules):
		self.rules = rules

	def append_rule(self, newrule):
		self.tokens += newrule.get_tokens()
		self.rules.append(newrule)

	def insert_rule_before(self, newrule, existingrule):
		if newrule.get_mediaquery() != existingrule.get_mediaquery():
			raise Exception('not yet implemented: insert before with diff mediaquery')
		firsttoken = existingrule.get_tokens()[0]
		i = self.tokens.index(firsttoken)
		for t in reversed(newrule.get_tokens()):
			self.tokens.insert(i, t)
		self.rules.insert(i, newrule)

	def insert_rule_after(self, newrule, existingrule):
		existingruletokens = existingrule.get_tokens()
		lasttoken = existingruletokens[len(existingruletokens) - 1]
		if lasttoken == self.tokens[-1]:
			self.tokens += newrule.get_tokens()
		else:
			i = self.tokens.index(lasttoken) + 1
			for t in reversed(newrule.get_tokens()):
				self.tokens.insert(i, t)
		i = self.rules.index(existingrule)
		self.rules.insert(i, newrule)
	
	def get_rules(self):
		return self.rules
	
	def set_mediaqueries(self, mediaqueries):
		self.mediaqueries = mediaqueries
	
	def __str__(self):
		return ''.join([str(t) for t in self.tokens])
