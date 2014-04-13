class MediaQuery:
	
	def __init__(self, starttokens=[], endtokens=[], querytext=''):
		self.starttokens = starttokens
		self.endtokens = endtokens
		self.querytext = querytext
	
	def get_tokens(self):
		""" get all tokens directly associated with media-query

		TODO: This approach leaves me uneasy, as it does not
		convey the gap in the middle where rules would be.
		"""
		return self.get_starttokens() + self.get_endtokens()

	def get_starttokens(self):
		return self.starttokens

	def get_endtokens(self):
		return self.endtokens

	def get_query(self):
		return self.querytext
