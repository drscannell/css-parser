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
			else:
				print '||| not tokens: %s |||' % (bufstr)
		return tokens
				
	
	@classmethod
	def tokenize_buffer(cls, txt):
		# comment start
		m = re.match(r'(.*)(/\*)', txt)
		if m:
			return [{
				'txt': m.group(1),
				'type': '<content />'
				},{
				'txt': m.group(2).strip(),
				'type': '<comment>'
				}]
		# comment end
		m = re.match(r'(.*)(\*/)', txt)
		if m:
			return [{
				'txt': m.group(1),
				'type': '<content />'
				},{
				'txt': m.group(2).strip(),
				'type': '</comment>'
				}]
		# block start
		m = re.match(r'([^{}]*)(\{)', txt)
		if m:
			return [{
				'txt': m.group(1).strip(),
				'type': '<selector />'
				},{
				'txt': m.group(2).strip(),
				'type': '<block>'
				}]
		# block end
		m = re.match(r'(.*)(\})', txt)
		if m:
			return [{
				'txt': m.group(1).strip(),
				'type': '<content />'
				},{
				'txt': m.group(2).strip(),
				'type': '</block>'
				}]
		# declaration
		m = re.match(r'([^:;]*):([^;]*);', txt)
		if m:
			return [{
				'txt': m.group(1).strip(),
				'type': '<property />'
				},{
				'txt': m.group(2).strip(),
				'type': '<value />'
				}]
		return []


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
	print '%s\t\t%s' % (t['type'],t['txt'])
print ''

