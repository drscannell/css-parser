class MediaQuery:
	
	def __init__(self, starttokens=[], endtokens=[], querytext=''):
		self.starttokens = starttokens
		self.endtokens = endtokens
		self.querytext = querytext
	
	def get_starttokens(self):
		return self.starttokens

	def get_endtokens(self):
		return self.endtokens

	def get_query(self):
		return self.querytext
