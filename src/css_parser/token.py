class Token:
	
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

	def __init__(self, tokentype, tokentext):
		self.tokentype = tokentype
		self.tokentext = tokentext


