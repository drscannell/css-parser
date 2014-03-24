from token import Token
from tokenizer import Tokenizer
from stylesheet import StyleSheet
from rule import Rule
from rulefactory import RuleFactory
from declaration import Declaration
from mediaqueryfactory import MediaQueryFactory

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
			buf_rules, buf_mediaqueries, is_spent = cls.parse_token_buffer(buffer)
			rules += buf_rules
			mediaqueries += buf_mediaqueries
			if is_spent:
				buffer = []
		return rules, mediaqueries

	@classmethod
	def parse_token_buffer(cls, tokens):
		rules = []
		mediaqueries = []
		should_discard = False
		types = [t.get_type() for t in tokens]

		if types == [Token.WHITESPACE]:
			should_discard = True
		elif types == [Token.LINEBREAK]:
			should_discard = True
		elif cls.is_comment(tokens):
			should_discard = True
		elif cls.is_mediaquery_block(tokens):
			querystart, queryend, block = cls.distill_mediaquery_block(tokens)
			mediaqueries.append(MediaQueryFactory.construct(querystart, queryend))
			rules, nested_mediaqueries = cls.parse_tokens(block)
			mediaqueries += nested_mediaqueries
		elif cls.is_rule_block(tokens):
			rules.append(RuleFactory.construct(tokens))
			should_discard = True

		return rules, mediaqueries, should_discard

	@classmethod
	def is_comment(cls, tokens):
		types = [t.get_type() for t in tokens]
		if types[0] == Token.COMMENT_START:
			if types[len(types)-1] == Token.COMMENT_END:
				return True
		return False

	@classmethod
	def is_mediaquery_block(cls, tokens):
		starts, ends = cls.count_curly_brackets(tokens)
		if starts == 2 and ends == 2:
			return True
		return False
	
	@classmethod
	def is_rule_block(cls, tokens):
		starts, ends = cls.count_curly_brackets(tokens)
		if starts == 1 and ends == 1:
			return True
		return False

	@classmethod
	def count_curly_brackets(cls, tokens):
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
	def distill_mediaquery_block(cls, tokens):
		querystart = []
		queryend = []
		block = []
		in_querystart = True
		in_block = False
		for token in tokens:
			if in_querystart:
				querystart.append(token)
				if token.get_type() == Token.BLOCK_START:
					in_querystart = False
					in_block = True
			elif in_block:
				if token.get_type() == Token.BLOCK_END:
					starts, ends = cls.count_curly_brackets(block)
					if ends > starts:
						queryend.append(token)
						in_block = False
					else:
						block.append(token)
				else:
					block.append(token)
			else:
				queryend.append(token)
		return querystart, queryend, block
