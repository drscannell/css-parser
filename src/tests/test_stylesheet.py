import os
import re
from css_parser.tokenizer import Tokenizer
from css_parser.stylesheet import StyleSheet
from css_parser.stylesheet_reader import StyleSheetReader
from css_parser.rulefactory import RuleFactory

class TestCases:

	def test_str_no_modifications(self):
		'''
		If we don't manipulate the stylesheet, is
		the original text being faithfully preserved?
		'''

		inputs = [
				'body {margin:0;}',
				'''body {
					margin:0;
					background:blue;
				}''',
				'''body {
					margin:0;
					background:blue;
				}
				
				@media amzn-kf8 {
					.mobi-hide {
						display:none;
					}
				}'''
				]

		for inp in inputs:
			yield self.check_str, inp
	
	def check_str(self, txt_in):
		tokens = Tokenizer.tokenize_string(txt_in)
		stylesheet = StyleSheet()
		stylesheet.set_tokens(tokens)
		txt_out = str(stylesheet)
		print 'expected:\n%s' % (txt_in)
		print '\nobserved:\n%s' % (txt_out)
		assert txt_in == txt_out

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
		stylesheet = StyleSheetReader.read_string(test['input'])
		new_rule_tokens = Tokenizer.tokenize_string(test['to_insert'])
		new_rule = RuleFactory.construct(new_rule_tokens)
		existing_rule = stylesheet.get_rules()[test['existing_index']]
		stylesheet.insert_rule_after(new_rule, existing_rule)
		observed_num_rules = len(stylesheet.get_rules())
		observed_string = str(stylesheet)
		for k in test:
			print '%s: %s' % (k, test[k])
		print 'observed_num_rules: %s' % (observed_num_rules)
		print 'observed_string: %s' % (observed_string)
		assert observed_num_rules == test['expected_num_rules']
		assert observed_string == test['expected_string']

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

	def test_insert_rule_after_into_mediaquery(self):
		tests = [
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
						 '	}p{text-indent:1em;}' \
						 '	p.indent{text-indent:0;}' \
						 '}'},

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
						 '	p.indent{text-indent:0;}p{text-indent:1em;}' \
						 '	p.indent:after {' \
						 '		content:"hello";' \
						 '		color:  green;' \
						 '	}' \
						 '}'}
				]

		for test in tests:
			yield self.check_insert_rule_after_into_mediaquery, test
	
	def check_insert_rule_after_into_mediaquery(self, test):
		stylesheet = StyleSheetReader.read_string(test['input'])
		new_rule_tokens = Tokenizer.tokenize_string(test['to_insert'])
		existing_rule = stylesheet.get_rules()[test['existing_index']]
		new_rule = RuleFactory.construct(new_rule_tokens)
		new_rule.set_mediaquery(existing_rule.get_mediaquery())
		stylesheet.insert_rule_after(new_rule, existing_rule)
		observed_num_rules = len(stylesheet.get_rules())
		observed_string = str(stylesheet)
		for k in test:
			print '%s: %s' % (k, test[k])
		print 'observed_num_rules: %s' % (observed_num_rules)
		print 'observed_string: %s' % (observed_string)
		assert observed_num_rules == test['expected_num_rules']
		assert observed_string == test['expected_string']

	# ----------------------------------------


	def test_insert_rule_before_into_mediaquery(self):
		tests = [
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
						 '	p{text-indent:1em;}div.awesome {' \
						 '		font-family:Helvetica;' \
						 '		margin:0;' \
						 '	}' \
						 '	p.indent{text-indent:0;}' \
						 '}'},

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
						 '	p{text-indent:1em;}p.indent{text-indent:0;}' \
						 '	p.indent:after {' \
						 '		content:"hello";' \
						 '		color:  green;' \
						 '	}' \
						 '}'}
				]

		for test in tests:
			yield self.check_insert_rule_before_into_mediaquery, test
	
	def check_insert_rule_before_into_mediaquery(self, test):
		stylesheet = StyleSheetReader.read_string(test['input'])
		new_rule_tokens = Tokenizer.tokenize_string(test['to_insert'])
		existing_rule = stylesheet.get_rules()[test['existing_index']]
		new_rule = RuleFactory.construct(new_rule_tokens)
		new_rule.set_mediaquery(existing_rule.get_mediaquery())
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





