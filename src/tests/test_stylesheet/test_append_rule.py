import os
import re
from css_parser.tokenizer import Tokenizer
from css_parser.stylesheet import StyleSheet
from css_parser.stylesheet_reader import StyleSheetReader
from css_parser.rulefactory import RuleFactory

class TestCases:

	# ----------------------------------------

	def test_append_rule(self):
		tests = [
				# simple one rule
				{'input': 'body{margin:0;}',
				 'to_append': 'p{text-indent:1em;}',
				 'expected_num_rules': 2,
				 'expected_string': 'body{margin:0;}p{text-indent:1em;}'},
				# terminal comment
				{'input': 'body{margin:0;}/* comment */',
				 'to_append': 'p{text-indent:1em;}',
				 'expected_num_rules': 2,
				 'expected_string': 'body{margin:0;}/* comment */p{text-indent:1em;}'},
				# commented out rule
				{'input': 'body {' \
						'	margin:0;' \
						'}' \
						'/*p.indent {' \
						'	text-indent: 1em;' \
						'}*/',
				 'to_append': 'p.nonindent {' \
						 '	text-indent:0;' \
						 '}',
				 'expected_num_rules': 2,
				 'expected_string': 'body {' \
						'	margin:0;' \
						'}' \
						'/*p.indent {' \
						'	text-indent: 1em;' \
						'}*/p.nonindent {' \
						 '	text-indent:0;' \
						 '}'},
				# media query
				{'input': '/* media query */' \
						'body {' \
						'	margin:0;' \
						'}' \
						'@media amzn-kf8 {' \
						'	p.indent {' \
						'		text-indent: 1em;' \
						'	}' \
						'}',
				 'to_append': 'p.nonindent {' \
						 '	text-indent:0;' \
						 '}',
				 'expected_num_rules': 3,
				 'expected_string': '/* media query */' \
						'body {' \
						'	margin:0;' \
						'}' \
						'@media amzn-kf8 {' \
						'	p.indent {' \
						'		text-indent: 1em;' \
						'	}' \
						'}p.nonindent {' \
						 '	text-indent:0;' \
						 '}'}

				]

		for test in tests:
			yield self.check_append_rule, test
	
	def check_append_rule(self, test):
		stylesheet = StyleSheetReader.read_string(test['input'])
		new_rule_tokens = Tokenizer.tokenize_string(test['to_append'])
		new_rule = RuleFactory.construct(new_rule_tokens)
		stylesheet.append_rule(new_rule)
		observed_num_rules = len(stylesheet.get_rules())
		observed_string = str(stylesheet)
		for k in test:
			print '%s: %s' % (k, test[k])
		print 'observed_num_rules: %s' % (observed_num_rules)
		print 'observed_string: %s' % (observed_string)
		assert observed_num_rules == test['expected_num_rules']
		assert observed_string == test['expected_string']

	# ----------------------------------------

