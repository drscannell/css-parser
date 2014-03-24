from css_parser.tokenizer import Tokenizer
from css_parser.rulefactory import RuleFactory

class TestCases:

	def test_selector_parsing(self):
		tests = [
				{
					'txt':'body{}',
					'selector':'body'
				},
				{
					'txt':'.indent {}',
					'selector':'.indent'
				},
				{
					'txt':'p.nonindent {}',
					'selector':'p.nonindent'
				},
				{
					'txt':'.page > img\n{}',
					'selector':'.page > img'
				},
				{
					'txt':'.page    img\n{}',
					'selector':'.page img'
				},
				{
					'txt':'.box:before  {}',
					'selector':'.box:before'
				}
				]
		for test in tests:
			yield self.check_selector_parsing, test
	
	def check_selector_parsing(self, test):
		tokens = Tokenizer.tokenize_string(test['txt'])
		rule = RuleFactory.construct(tokens)
		expected_selector = test['selector']
		observed_selector = rule.get_selector()
		print 'input: %s' % (test['txt'])
		print 'expected selector: %s' % (expected_selector)
		print 'observed selector: %s' % (observed_selector)
		assert expected_selector == observed_selector

# -------------------------------------------------------


	def test_declaration_count(self):
		tests = [
				{
					'txt':'body{}',
					'count':0
				},
				{
					'txt':'body{margin:0;}',
					'count':1
				},
				{
					'txt':'''p.indent {
						margin:0;
						/*text-indent: 2em; */
						text-indent: 1em;
					}''',
					'count':2
				}

				]
		for test in tests:
			yield self.check_declaration_count, test
	
	def check_declaration_count(self, test):
		tokens = Tokenizer.tokenize_string(test['txt'])
		rule = RuleFactory.construct(tokens)
		expected = test['count']
		observed = len(rule.get_declarations())
		print 'input: %s' % (test['txt'])
		print 'expected: %i declarations' % (expected)
		print 'observed: %i declarations' % (observed)
		assert expected == observed

