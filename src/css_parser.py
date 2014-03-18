import re

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
				
	
	@classmethod
	def tokenize_buffer(cls, txt):
		# block start
		m = re.match(r'([^{}]*)(\{)', txt)
		if m:
			return [{
				'txt': m.group(1).strip(),
				'type': 'selector'
				},{
				'txt': m.group(2).strip(),
				'type': 'blockstart'
				}]
		# block end
		m = re.match(r'\s*(\})', txt)
		if m:
			return [{
				'txt': m.group(1).strip(),
				'type': 'blockend'
				}]
		m = re.match(r'([^:;]*):([^;]*);', txt)
		if m:
			return [{
				'txt': m.group(1).strip(),
				'type': 'decl_property'
				},{
				'txt': m.group(2).strip(),
				'type': 'decl_value'
				}]
		return []


txt = '''p.indent {
	text-indent:0em;
	margin: 0 1em 0 1em;
}'''

print ''
tokens = CssTokenizer.tokenize(txt)
for t in tokens:
	print '%s\t\t%s' % (t['type'],t['txt'])
print ''

