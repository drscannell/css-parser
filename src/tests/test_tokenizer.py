import os
import re
from css_parser.tokenizer import Tokenizer

class TokenizerTest:
	def __init__(self,txt,expected):
		self.txt = txt
		self.expected = expected
		self.tokens = Tokenizer.tokenize_string(self.txt)
	def test(self):
		assert [t.tokentype for t in self.tokens] == self.expected

def read_tokenizer_file(filename):
	src = os.path.dirname(os.path.realpath(__file__))
	path = os.path.join(src,'tokenizer_test_files/',filename)
	f = open(path, 'r')
	txt = f.read()
	f.close()
	pattern = re.compile(r'^(.*)\n\^__EXPECTED\n(.*)\$__EXPECTED.*$', re.DOTALL)
	m = pattern.match(txt)
	if m:
		return TokenizerTest(m.group(1), parse_list(m.group(2)))
	else:
		raise Exception('could not parse test file')

def parse_list(txt):
	txt = re.sub(r'\s+', ',', txt)
	items = []
	for item in txt.split(','):
		if item.strip() != '':
			items.append(item)
	return items


class TestCases:

	def test_tokenize(self):
		
		testfiles = [
			'test_01_comments.txt',
			'test_02_trailing_whitespace.txt',
			'test_03_single_line_rules.txt',
			'test_04_multi_line_rules.txt',
			'test_05_commented_rule.txt',
			'test_06_comment_in_selector.txt',
			'test_07_comment_after_declaration.txt',
			'test_08_comment_after_blockstart.txt',
			'test_09_commented_declaration.txt',
			'test_10_comment_in_value.txt',
			'test_11_comment_in_property.txt',
			'test_12_multiline_declarations.txt',
			'test_13_pseudoselector.txt',
			'test_14_singlequotes.txt',
			'test_15_doublequotes.txt',
			'test_16_mediaquery.txt',
			'test_17_fontface.txt']

		for filename in testfiles:
			yield self.check_tokenize, filename
	
	def check_tokenize(self, filename):
		test = read_tokenizer_file(filename)
		print 'test file: %s' % (filename)
		print 'input: %s' % (test.txt)
		print 'expected: %s' % (test.expected)
		print '\nobserved: %s' % ([t.tokentype for t in test.tokens])
		test.test()

	def test_add_linenumbers(self):
		txt = 'body{\nmargin:0;\n}'
		tokens = Tokenizer.tokenize_string(txt)
		assert tokens[0].get_linenumber() == 1
		assert tokens[len(tokens)-1].get_linenumber() == 3


