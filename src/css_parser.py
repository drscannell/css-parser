import re

class Token:
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
		return tokens
				
	commentstart = re.compile(r'(.*)(/\*)', re.DOTALL)
	commentend   = re.compile(r'(.*)(\*/)', re.DOTALL)
	blockstart   = re.compile(r'([^{}]*)(\{)', re.DOTALL)
	blockend     = re.compile(r'(.*)(\})', re.DOTALL)
	declaration  = re.compile(r'([^:;]*):([^;]*);', re.DOTALL)
	
	@classmethod
	def tokenize_buffer(cls, txt):
		tokens = []
		# comment start
		m = cls.commentstart.match(txt)
		if m:
			tokens.append(Token('<content/>', m.group(1)))
			tokens.append(Token('<comment>', m.group(2)))
		# comment end
		m = cls.commentend.match(txt)
		if m:
			tokens.append(Token('<content/>', m.group(1)))
			tokens.append(Token('</comment>', m.group(2)))
		# block start
		m = cls.blockstart.match(txt)
		if m:
			tokens.append(Token('<selector/>', m.group(1)))
			tokens.append(Token('<block>', m.group(2)))
		# block end
		m = cls.blockend.match(txt)
		if m:
			tokens.append(Token('<content/>', m.group(1)))
			tokens.append(Token('</block>', m.group(2)))
		# declaration
		m = cls.declaration.match(txt)
		if m:
			tokens.append(Token('<property/>', m.group(1)))
			tokens.append(Token('<value/>', m.group(2)))
		return tokens




txt = '''/* sample stylesheet */
p.indent {
	text-indent:0em;
	margin: 0 1em 0 1em;
}

div.hooray
{
	font-family: Helvetica, sans-serif;
} /* remember the alamo */

/*
 * and remember
 * to brush your
 * teeth
 */
 '''

print ''
tokens = CssTokenizer.tokenize(txt)
for t in tokens:
	print '%s\t\t%s' % (t.tokentype, t.tokentext)
print ''

