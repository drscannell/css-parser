import os
import re
from css_parser.tokenizer import Tokenizer
from css_parser.parser import Parser

class TestCases:

	def test_num_rules(self):
		tests = [
				('/* comment */', 0),
				('body{margin:0;}', 1),
				('''/*body {
						margin:0;
					}*/
					div {
						padding:0;
					}''', 1),
				('body{margin:0;}\ndiv{padding:0;}', 2),
				('''body {
						margin:0;
					}
				/* comment */
				div{padding:0;}''', 2),
				('''@media screen and (min-width:300px) {
						.page {
							width: 100%;
						}
					}''', 1)

				]

		for test in tests:
			yield self.check_num_rules, test
	
	def check_num_rules(self, test):
		txt, expected = test
		stylesheet = Parser.parse_string(txt)
		rules = stylesheet.get_rules()
		observed = len(rules)
		print 'input: %s' % (txt)
		print 'expected: %i rules' % (expected)
		print 'observed: %i rules' % (observed)
		assert expected == observed

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
		rule = Parser.construct_rule(tokens)
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
		rule = Parser.construct_rule(tokens)
		expected = test['count']
		observed = len(rule.get_declarations())
		print 'input: %s' % (test['txt'])
		print 'expected: %i declarations' % (expected)
		print 'observed: %i declarations' % (observed)
		assert expected == observed

