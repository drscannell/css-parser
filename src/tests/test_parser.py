import os
import re
from css_parser.tokenizer import Tokenizer
from css_parser.parser import Parser

class TestCases:

	def test_num_rules(self):
		tests = [
				('/* comment */', 0),
				('body{margin:0;}', 1),
				('/*body{margin:0;}*/\ndiv{padding:0;}', 1),
				('body{margin:0;}\ndiv{padding:0;}', 2),
				('body{margin:0;}/* comment */div{padding:0;}', 2)
				]

		for test in tests:
			yield self.check_num_rules, test
	
	def check_num_rules(self, test):
		txt, expected = test
		stylesheet = Parser.parse_string(txt)
		rules = stylesheet.get_rules()
		observed = len(rules)
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
