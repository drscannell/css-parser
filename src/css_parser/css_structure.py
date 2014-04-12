
class CssStructure:

	def _insert_tokens_before(self, new, existing):
		tokens = new.get_tokens()
		firsttoken = existing.get_tokens()[0]
		i = self.tokens.index(firsttoken)
		for t in reversed(tokens):
			self.tokens.insert(i, t)
	
	def _insert_tokens_after(self, new, existing):
		tokens = new.get_tokens()
		existingtokens = existing.get_tokens()
		lasttoken = existingtokens[-1]
		if lasttoken == self.tokens[-1]:
			self.tokens += tokens
		else:
			i = self.tokens.index(lasttoken) + 1
			for t in reversed(tokens):
				self.tokens.insert(i, t)

	def __str__(self):
		return ''.join([str(t) for t in self.tokens])

