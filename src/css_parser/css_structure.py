
class CssStructure:

	def _insert_tokens_before(self, tokens, token):
		i = self.tokens.index(token)
		for t in reversed(tokens):
			self.tokens.insert(i, t)
	
	def _insert_tokens_after(self, tokens, token):
		if token == self.tokens[-1]:
			self.tokens += tokens
		else:
			i = self.tokens.index(token) + 1
			for t in reversed(tokens):
				self.tokens.insert(i, t)

