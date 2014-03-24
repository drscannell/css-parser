from token import Token
from declaration import Declaration
from rule import Rule

class RuleFactory:

	@classmethod
	def construct(cls, tokens):
		selector, declarations = cls.separate_tokens(tokens)
		rule = Rule(tokens)
		rule.set_selector_tokens(selector)
		rule.set_declarations([cls.construct_declaration(d) for d in declarations])
		return rule
	
	@classmethod
	def construct_declaration(cls, tokens):
		declaration = Declaration(tokens)
		return declaration

		
	@classmethod
	def separate_tokens(cls, tokens):
		selector = []
		declarations = []
		declaration = []
		in_selector = True
		in_comment = False
		for token in tokens:
			if token.get_type() == Token.COMMENT_START:
				in_comment = True
			elif token.get_type() == Token.COMMENT_END:
				in_comment = False

			if token.get_type() == Token.BLOCK_START:
				in_selector = False
			elif in_selector:
				selector.append(token)
			elif not in_comment and token.get_type() == Token.SEMICOLON:
				declaration.append(token)
				declarations.append(declaration)
				declaration = []
			elif not in_comment and token.get_type() == Token.BLOCK_END:
				if cls.is_terminal_declaration(declaration):
					declarations.append(declaration)
				declaration = []
			else:
				declaration.append(token)
		return selector, declarations

	@classmethod
	def is_terminal_declaration(cls, tokens):
		has_prop = False
		has_colon = False
		has_val = False
		for typ in [t.get_type() for t in tokens]:
			if not has_prop:
				if typ == Token.TXT:
					has_prop = True
			elif not has_colon:
				if typ == Token.COLON:
					has_colon = True
			elif not has_val:
				if typ == Token.TXT:
					has_val = True
		if has_prop and has_colon and has_val:
			return True
		return False

