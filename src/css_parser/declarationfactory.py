from declaration import Declaration

class DeclarationFactory:

	@classmethod
	def construct(cls, tokens):
		declaration = Declaration(tokens)
		return declaration

