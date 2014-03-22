import re

class Token:
	
	COMMENT_START = '/*'
	COMMENT_END = '*/'
	SELECTOR = 'selector'
	BLOCK_START = '{'
	BLOCK_END = '}'
	PROPERTY = 'prop'
	VALUE = 'val'
	TXT = 'txt'
	WHITESPACE = 'whitespace'

	def __init__(self, tokentype, tokentext):
		self.tokentype = tokentype
		self.tokentext = tokentext

class CssTokenizer:

	@classmethod
	def tokenize(cls, txt):
		tokens = []
		buffer = []
		for i, char in enumerate(txt):
			buffer.append(char)
			bufstr = ''.join(buffer)
			buftokens= cls.tokenize_buffer(bufstr)
			if len(buftokens) > 0:
				tokens += buftokens
				buffer = []
		# capture untokenized trailing characters
		if len(buffer) > 0:
			tokens += cls.text(''.join(buffer))
		# clean up tokens
		tokens = cls.clear_empty_tokens(tokens)
		tokens = cls.identify_whitespace_tokens(tokens)
		return tokens
				
	@classmethod
	def tokenize_buffer(cls, txt):
		tokens = []
		# comment start
		if cls.comment_start(txt):
			tokens += cls.comment_start(txt)
		elif cls.comment_end(txt):
			tokens += cls.comment_end(txt)
		elif cls.block_start(txt):
			tokens += cls.block_start(txt)
		elif cls.declaration(txt):
			tokens += cls.declaration(txt)
		elif cls.block_end(txt):
			tokens += cls.block_end(txt)
		return tokens

	@classmethod
	def comment_start(cls, txt):
		p = re.compile(r'(\s*)([^\s]*)(\s*)(/\*)', re.DOTALL)
		m = p.match(txt)
		if m:
			return [Token(Token.WHITESPACE, m.group(1)),
					Token(Token.TXT, m.group(2)),
					Token(Token.WHITESPACE, m.group(3)),
					Token(Token.COMMENT_START, m.group(4))]
		else:
			return None
		
	@classmethod
	def comment_end(cls, txt):
		p = re.compile(r'(.*)(\*/)', re.DOTALL)
		m = p.match(txt)
		if m:
			return [Token(Token.TXT, m.group(1)),
					Token(Token.COMMENT_END, m.group(2))]
		else:
			return None

	@classmethod
	def block_start(cls, txt):
		p = re.compile(r'(\s*)([^{}]*?)(\s*)(\{)', re.DOTALL)
		m = p.match(txt)
		if m:
			return [Token(Token.WHITESPACE, m.group(1)),
					Token(Token.TXT, m.group(2)),
					Token(Token.WHITESPACE, m.group(3)),
					Token(Token.BLOCK_START, m.group(4))]
		else:
			return None

	@classmethod
	def block_end(cls, txt):
		'''
		Instead of capturing only preceding whitespace,
		captures anything. If there are syntax errors, 
		the block_end will keep them from polluting 
		subsequent rules.
		'''
		p = re.compile(r'(.*)(\})', re.DOTALL)
		m = p.match(txt)
		if m:
			return [Token(Token.TXT, m.group(1)),
					Token(Token.BLOCK_END, m.group(2))]
		else:
			return None

	@classmethod
	def declaration(cls, txt):
		p = re.compile(r'(\s*)([^:;]*):([^;]*);', re.DOTALL)
		m = p.match(txt)
		if m:
			return [Token(Token.WHITESPACE, m.group(1)),
					Token(Token.PROPERTY, m.group(2)),
					Token(Token.VALUE, m.group(3))]
		else:
			return None
	
	@classmethod
	def text(cls, txt):
		return [Token(Token.TXT, txt)]
	
	@classmethod
	def clear_empty_tokens(cls, tokens):
		to_remove = []
		for token in tokens:
			if token.tokentext == '':
				to_remove.append(token)
		for token in to_remove:
			tokens.remove(token)
		return tokens

	@classmethod
	def identify_whitespace_tokens(cls, tokens):
		for token in tokens:
			if re.match(r'^\s*$', token.tokentext):
				token.tokentype = Token.WHITESPACE
		return tokens
