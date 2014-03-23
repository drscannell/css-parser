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
	
	def get_rules(self):
		return self.rules
	
	def set_mediaqueries(self, mediaqueries):
		self.mediaqueries = mediaqueries
	
	def __str__(self):
		return ''.join([str(t) for t in self.tokens])
