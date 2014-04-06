import os
import re
from css_parser.tokenizer import Tokenizer
from css_parser.stylesheet import StyleSheet
from css_parser.stylesheet_reader import StyleSheetReader
from css_parser.rulefactory import RuleFactory

class TestCases:

	# ----------------------------------------

	def test_insert_rule_before(self):
		tests = [
				{'input': 'body{margin:0;}',
				 'existing_index': 0,
				 'to_insert': 'p{text-indent:1em;}',
				 'expected_num_rules': 2,
				 'expected_string': 'p{text-indent:1em;}body{margin:0;}'},
				{'input': 'body{margin:0;}/* comment */',
				 'existing_index': 0,
				 'to_insert': 'p{text-indent:1em;}',
				 'expected_num_rules': 2,
				 'expected_string': 'p{text-indent:1em;}body{margin:0;}/* comment */'},
				# two rules with comment between
				{'input': 'body{margin:0;}' \
						'/* comment */' \
						'div{padding:0;}',
				 'existing_index': 1,
				 'to_insert': 'p{text-indent:1em;}',
				 'expected_num_rules': 3,
				 'expected_string': 'body{margin:0;}' \
						 '/* comment */' \
						 'p{text-indent:1em;}div{padding:0;}'},
				# insert before media query
				{'input': '/* media query */' \
						'@media amzn-mobi {' \
						'	div{padding:0;}' \
						'}',
				 'existing_index': 0,
				 'to_insert': 'p{text-indent:1em;}',
				 'expected_num_rules': 2,
				 'expected_string': '/* media query */' \
						'p{text-indent:1em;}@media amzn-mobi {' \
						'	div{padding:0;}' \
						'}'},
				# insert before media query
				{'input': '/* media query */' \
						'@media amzn-mobi {' \
						'	div{padding:0;}' \
						'	p{padding:0;}' \
						'}',
				 'existing_index': 1,
				 'to_insert': 'p{text-indent:1em;}',
				 'expected_num_rules': 3,
				 'expected_string': '/* media query */' \
						'p{text-indent:1em;}@media amzn-mobi {' \
						'	div{padding:0;}' \
						'	p{padding:0;}' \
						'}'}


				]

		for test in tests:
			yield self.check_insert_rule_before, test
	
	def check_insert_rule_before(self, test):
		stylesheet = StyleSheetReader.read_string(test['input'])
		print 'num rules: %i' % (len(stylesheet.rules))
		new_rule_tokens = Tokenizer.tokenize_string(test['to_insert'])
		new_rule = RuleFactory.construct(new_rule_tokens)
		existing_rule = stylesheet.get_rules()[test['existing_index']]
		stylesheet.insert_rule_before(new_rule, existing_rule)
		observed_num_rules = len(stylesheet.get_rules())
		observed_string = str(stylesheet)
		for k in test:
			print '%s: %s' % (k, test[k])
		print 'observed_num_rules: %s' % (observed_num_rules)
		print 'observed_string: %s' % (observed_string)
		assert observed_num_rules == test['expected_num_rules']
		assert observed_string == test['expected_string']

	# ----------------------------------------
