from css_parser import CssTokenizer

class TokenizerTest:
	def __init__(self,txt,expected):
		self.txt = txt
		self.expected = expected
		self.tokens = CssTokenizer.tokenize(self.txt)
	def test(self):
		assert [t.tokentype for t in self.tokens] == self.expected

class TestCases:
	def test_tokenize(self):
		args = [
			('/* comment*/',
				['/*','txt','*/']),
			('/* comment*/\nspan{margin:0;}',
				['/*','txt','*/','selector',
				'{','prop','val','}'])
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

