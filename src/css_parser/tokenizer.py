import re
from token import Token

class Tokenizer:

	@classmethod
	def tokenize_string(cls, txt):
		tokens = []
		buffer = []
		for i, char in enumerate(txt):
			buffer.append(char)
			bufstr = ''.join(buffer)
			buftokens= cls.tokenize_buffer(bufstr)
			if len(buftokens) > 0:
				for t in buftokens:
					if t.tokentext != '':
						tokens.append(t)
				buffer = []
		# capture untokenized trailing characters
		if len(buffer) > 0:
			tokens += cls.text(''.join(buffer))
		# clean up tokens
		tokens = cls.identify_whitespace_tokens(tokens)
		tokens = cls.add_linenumbers(tokens)
		return tokens
				
	@classmethod
	def tokenize_buffer(cls, txt):
		tokens = []
		# comment start
		if cls.linebreak(txt):
			tokens += cls.linebreak(txt)
		elif cls.comment_start(txt):
			tokens += cls.comment_start(txt)
		elif cls.comment_end(txt):
			tokens += cls.comment_end(txt)
		elif cls.block_start(txt):
			tokens += cls.block_start(txt)
		elif cls.colon(txt):
			tokens += cls.colon(txt)
		elif cls.semicolon(txt):
			tokens += cls.semicolon(txt)
		elif cls.singlequote(txt):
			tokens += cls.singlequote(txt)
		elif cls.doublequote(txt):
			tokens += cls.doublequote(txt)
		elif cls.block_end(txt):
			tokens += cls.block_end(txt)
		return tokens

	@classmethod
	def linebreak(cls, txt):
		p = re.compile(r'^([\t ]*)((?:\S.*)?)([\t ]*)(\n)$')
		m = p.match(txt)
		if m:
			return [Token(Token.WHITESPACE, m.group(1)),
					Token(Token.TXT, m.group(2)),
					Token(Token.WHITESPACE, m.group(3)),
					Token(Token.LINEBREAK, m.group(4))]
		else:
			return None


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
	def colon(cls, txt):
		p = re.compile(r'(\s*)([^:;]*?)(\s*)(:)', re.DOTALL)
		m = p.match(txt)
		if m:
			return [Token(Token.WHITESPACE, m.group(1)),
					Token(Token.TXT, m.group(2)),
					Token(Token.WHITESPACE, m.group(3)),
					Token(Token.COLON, m.group(4))]
		else:
			return None

	@classmethod
	def semicolon(cls, txt):
		p = re.compile(r'(\s*)([^:;]*?)(\s*)(;)', re.DOTALL)
		m = p.match(txt)
		if m:
			return [Token(Token.WHITESPACE, m.group(1)),
					Token(Token.TXT, m.group(2)),
					Token(Token.WHITESPACE, m.group(3)),
					Token(Token.SEMICOLON, m.group(4))]
		else:
			return None

	@classmethod
	def singlequote(cls, txt):
		p = re.compile(r'(\s*)([^\']*?)(\s*)(\')', re.DOTALL)
		m = p.match(txt)
		if m:
			return [Token(Token.WHITESPACE, m.group(1)),
					Token(Token.TXT, m.group(2)),
					Token(Token.WHITESPACE, m.group(3)),
					Token(Token.SINGLEQUOTE, m.group(4))]
		else:
			return None

	@classmethod
	def doublequote(cls, txt):
		p = re.compile(r'(\s*)([^"]*?)(\s*)(")', re.DOTALL)
		m = p.match(txt)
		if m:
			return [Token(Token.WHITESPACE, m.group(1)),
					Token(Token.TXT, m.group(2)),
					Token(Token.WHITESPACE, m.group(3)),
					Token(Token.DOUBLEQUOTE, m.group(4))]
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
	def identify_whitespace_tokens(cls, tokens):
		for token in tokens:
			if token.tokentype != 'brk':
				if re.match(r'^[ \t]*$', token.tokentext):
					token.tokentype = Token.WHITESPACE
		return tokens

	@classmethod
	def add_linenumbers(cls, tokens):
		linenumber = 1
		for token in tokens:
			token.set_linenumber(linenumber)
			if token.tokentype == 'brk':
				linenumber += 1
		return tokens

