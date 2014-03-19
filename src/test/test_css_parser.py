from css_parser import CssTokenizer

tokens = CssTokenizer.tokenize('/*')
assert len(tokens) == 1
assert tokens[0].tokentype == '<comment>'

class MyTest:
	def __init__(self,txt,expected):
		self.txt = txt
		self.expected = expected
		self.tokens = CssTokenizer.tokenize(self.txt)
	def test(self):
		assert [t.tokentype for t in self.tokens] == self.expected

class TestCases:
	def test_tokenize(self):
		tests = []
		tests.append(MyTest('/* comment*/',
			['<comment>','<content/>','</comment>']))
		tests.append(MyTest('/* comment*/\nspan{margin:0;}',
			['<comment>','<content/>','</comment>','<selector/>',
				'<block>','<property/>','<value/>','</block>']))
		for test in tests:
			yield self.check_tokenize, test
	
	def check_tokenize(self, test):
		print 'input: %s' % (test.txt)
		print 'expected: %s' % (test.expected)
		print 'observed: %s' % ([t.tokentype for t in test.tokens])
		test.test()

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

'''
print ''
tokens = CssTokenizer.tokenize(txt)
for t in tokens:
	print '%s\t\t%s' % (t.tokentype, t.tokentext)
print ''
'''

