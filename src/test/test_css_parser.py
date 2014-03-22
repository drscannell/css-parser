import os
import re
from css_parser import CssTokenizer

class TokenizerTest:
	def __init__(self,txt,expected):
		self.txt = txt
		self.expected = expected
		self.tokens = CssTokenizer.tokenize(self.txt)
	def test(self):
		assert [t.tokentype for t in self.tokens] == self.expected

def read_tokenizer_file(filename):
	src = os.path.dirname(os.path.realpath(__file__))
	path = os.path.join(src,filename)
	f = open(path, 'r')
	txt = f.read()
	f.close()
	pattern = re.compile(r'^(.*)\^__EXPECTED\n(.*)\$__EXPECTED.*$', re.DOTALL)
	m = pattern.match(txt)
	if m:
		return m.group(1), parse_list(m.group(2))
	else:
		raise Exception('could not parse test file')

def parse_list(txt):
	items = []
	for item in txt.split('\n'):
		if item.strip() != '':
			items.append(item)
	return items


class TestCases:


	def test_tokenize(self):
		args = [
			read_tokenizer_file('test_01.txt'),
			read_tokenizer_file('test_02.txt')
				]

		for args_tuple in args:
			yield self.check_tokenize, args_tuple
	
	def check_tokenize(self, arg_tuple):
		txt, expected = arg_tuple
		test = TokenizerTest(txt, expected)
		print 'input: %s' % (txt)
		print 'expected: %s' % (expected)
		print 'observed: %s' % ([t.tokentype for t in test.tokens])
		test.test()

