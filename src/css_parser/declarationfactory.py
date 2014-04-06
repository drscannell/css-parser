from declaration import Declaration
from token import Token

class DeclarationFactory:

	@classmethod
	def construct(cls, tokens):
		proptokens, valtokens = cls.separate_tokens(tokens)
		prop = ''.join([str(t) for t in proptokens]).strip()
		val = ''.join([str(t) for t in valtokens]).strip()
		declaration = Declaration(tokens, prop, val)
		return declaration

	@classmethod
	def separate_tokens(cls, tokens):
		prop = []
		val = []
		in_prop = True
		for token in tokens:
			if token.get_type() == Token.COLON:
				in_prop = False
			elif in_prop:
				prop.append(token)
			elif token.get_type() != Token.SEMICOLON:
				val.append(token)
		return prop, val



