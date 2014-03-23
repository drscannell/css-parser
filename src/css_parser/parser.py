from token import Token
from tokenizer import Tokenizer
from stylesheet import StyleSheet
from rule import Rule
from declaration import Declaration
from mediaquery import MediaQuery

class Parser:
	
	@classmethod
	def parse_string(cls, txt):
		tokens = Tokenizer.tokenize_string(txt)
		rules, mediaqueries = cls.parse_tokens(tokens)
		stylesheet = StyleSheet()
		stylesheet.set_tokens(tokens)
		stylesheet.set_rules(rules)
		stylesheet.set_mediaqueries(mediaqueries)
		return stylesheet

	@classmethod
	def parse_tokens(cls, tokens):
		rules = []
		mediaqueries = []
		buffer = []
		for token in tokens:
			buffer.append(token)
			rule, mediaquery, should_discard = cls.parse_buffer(buffer)
			if rule:
				rules.append(rule)
			if mediaquery:
				mediaqueries.append(mediaquery)
			if should_discard:
				buffer = []
		return rules, mediaqueries

	@classmethod
	def parse_buffer(cls, tokens):
		rule = None
		mediaquery = None
		should_discard = False
		types = [t.get_type() for t in tokens]

		if types == [Token.WHITESPACE]:
			should_discard = True
		elif types == [Token.LINEBREAK]:
			should_discard = True
		elif cls.complete_comment(tokens):
			should_discard = True
		elif cls.is_mediaquery_block(tokens):
			raise Exception('not implemented!')
		elif cls.is_rule_block(tokens):
			rule = cls.construct_rule(tokens)
			should_discard = True

		return rule, mediaquery, should_discard

	@classmethod
	def complete_comment(cls, tokens):
		types = [t.get_type() for t in tokens]
		if types[0] == Token.COMMENT_START:
			if types[len(types)-1] == Token.COMMENT_END:
				return True
		return False

	@classmethod
	def is_mediaquery_block(cls, tokens):
		starts, ends = cls.get_block_status(tokens)
		if starts == 2 and ends == 2:
			return True
		return False
	
	@classmethod
	def is_rule_block(cls, tokens):
		starts, ends = cls.get_block_status(tokens)
		if starts == 1 and ends == 1:
			return True
		return False

	@classmethod
	def get_block_status(cls, tokens):
		types = [t.get_type() for t in tokens]
		starts = 0
		ends = 0
		in_comment = False
		for t in types:
			if t == Token.COMMENT_START:
				in_comment = True
			elif t == Token.COMMENT_END:
				in_comment = False
			elif not in_comment and t == Token.BLOCK_START:
				starts += 1
			elif not in_comment and t == Token.BLOCK_END:
				ends += 1
		return starts, ends

	@classmethod
	def construct_rule(cls, tokens):
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



		



