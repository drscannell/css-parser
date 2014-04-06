import os
import re
from css_parser.tokenizer import Tokenizer
from css_parser.stylesheet import StyleSheet
from css_parser.stylesheet_reader import StyleSheetReader
from css_parser.rulefactory import RuleFactory

class TestCases:

	# ----------------------------------------

	def test_insert_rule_after(self):
		tests = [
				{'descrip': 'one rule',
				 'input': 'body{margin:0;}',
				 'existing_index': 0,
				 'to_insert': 'p{text-indent:1em;}',
				 'expected_num_rules': 2,
				 'expected_string': 'body{margin:0;}p{text-indent:1em;}'},

				{'descrip': 'rule then comment',
				 'input': 'body{margin:0;}/* comment */',
				 'existing_index': 0,
				 'to_insert': 'p{text-indent:1em;}',
				 'expected_num_rules': 2,
				 'expected_string': 'body{margin:0;}' \
						 'p{text-indent:1em;}/* comment */'},

				{'descrip': 'two rules with comment between',
				 'input': 'body {' \
						 '	margin:0;' \
						 '}' \
						 '/* comment */' \
						 'div.awesome {' \
						 '	font-family:Helvetica;' \
						 '	margin:0;' \
						 '}',
				 'existing_index': 1,
				 'to_insert': 'p{text-indent:1em;}',
				 'expected_num_rules': 3,
				 'expected_string': 'body {' \
						 '	margin:0;' \
						 '}' \
						 '/* comment */' \
						 'div.awesome {' \
						 '	font-family:Helvetica;' \
						 '	margin:0;' \
						 '}p{text-indent:1em;}'},

				{'descrip': 'media query with two rules',
				 'input': 'body {' \
						 '	margin:0;' \
						 '}' \
						 '@media amzn-kf8 {' \
						 '	div.awesome {' \
						 '		font-family:Helvetica;' \
						 '		margin:0;' \
						 '	}' \
						 '	p.indent{text-indent:0;}' \
						 '}',
				 'existing_index': 1,
				 'to_insert': 'p{text-indent:1em;}',
				 'expected_num_rules': 4,
				 'expected_string': 'body {' \
						 '	margin:0;' \
						 '}' \
						 '@media amzn-kf8 {' \
						 '	div.awesome {' \
						 '		font-family:Helvetica;' \
						 '		margin:0;' \
						 '	}' \
						 '	p.indent{text-indent:0;}' \
						 '}p{text-indent:1em;}'},

				{'descrip': 'media query with three rules',
				 'input': 'body {' \
						 '	margin:0;' \
						 '}' \
						 '@media amzn-kf8 {' \
						 '	div.awesome {' \
						 '		font-family:Helvetica;' \
						 '		margin:0;' \
						 '	}' \
						 '	p.indent{text-indent:0;}' \
						 '	p.indent:after {' \
						 '		content:"hello";' \
						 '		color:  green;' \
						 '	}' \
						 '}',
				 'existing_index': 2,
				 'to_insert': 'p{text-indent:1em;}',
				 'expected_num_rules': 5,
				 'expected_string': 'body {' \
						 '	margin:0;' \
						 '}' \
						 '@media amzn-kf8 {' \
						 '	div.awesome {' \
						 '		font-family:Helvetica;' \
						 '		margin:0;' \
						 '	}' \
						 '	p.indent{text-indent:0;}' \
						 '	p.indent:after {' \
						 '		content:"hello";' \
						 '		color:  green;' \
						 '	}' \
						 '}p{text-indent:1em;}'}
				]

		for test in tests:
			yield self.check_insert_rule_after, test
	
	def check_insert_rule_after(self, test):
		# setup
		stylesheet = StyleSheetReader.read_string(test['input'])
		new_rule_tokens = Tokenizer.tokenize_string(test['to_insert'])
		new_rule = RuleFactory.construct(new_rule_tokens)
		existing_rule = stylesheet.get_rules()[test['existing_index']]
		# test
		stylesheet.append_rule(new_rule, existing_rule)
		observed_num_rules = len(stylesheet.get_rules())
		observed_string = str(stylesheet)
		for k in test:
			print '%s: %s' % (k, test[k])
		print 'observed_num_rules: %s' % (observed_num_rules)
		print 'observed_string: %s' % (observed_string)
		assert observed_num_rules == test['expected_num_rules']
		assert observed_string == test['expected_string']

	# ----------------------------------------

