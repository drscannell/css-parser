class Token:
	
	LINEBREAK = 'brk'
	COMMENT_START = '/*'
	COMMENT_END = '*/'
	BLOCK_START = '{'
	BLOCK_END = '}'
	COLON = ':'
	SEMICOLON = ';'
	DOUBLEQUOTE = '"'
	SINGLEQUOTE = '\''
	TXT = 'txt'
	WHITESPACE = 'whitespace'
	# deprecated
	SELECTOR = 'selector'
	PROPERTY = 'prop'
	VALUE = 'val'

	def __init__(self, tokentype, tokentext, linenumber=None):
		self.tokentype = tokentype
		self.tokentext = tokentext
		self.linenumber = linenumber
	
	def get_text(self):
		return self.tokentext

	def get_type(self):
		return self.tokentype

	def set_linenumber(self, num):
		self.linenumber = num
	
	def get_linenumber(self):
		return self.linenumber

	def __str__(self):
		return self.get_text()
