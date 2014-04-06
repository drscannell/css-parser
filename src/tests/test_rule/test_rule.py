from css_parser.rule import Rule

class TestCases:

	# ----------------------------------------

	def test_from_string(self):
		tests = [
				# one rule
				{'input': 'body{margin:0;}',
				 'expected': 'body{margin:0;}'
					},
				# one rule, space around
				{'input': ' p.indent {margin:0;} ',
				 'expected': 'p.indent {margin:0;}'
					},
				# one rule, multilined
				{'input': 'p.indent {' \
						'	margin:0;' \
						'}',
				 'expected': 'p.indent {' \
						'	margin:0;' \
						'}'
					},
				# one rule, media-queried
				{'input': '@media all {' \
						'	p { margin:0;}' \
						'}',
				 'expected': '@media all {' \
						'p { margin:0;}' \
						'}'
					}

				]

		for test in tests:
			yield self.check_from_string, test
	
	def check_from_string(self, test):
		rule = Rule.from_string(test['input'])
		observed = rule.to_string()
		for k in test:
			print '%s: %s' % (k, test[k])
		print 'observed: %s' % (observed)
		assert observed == test['expected']

	# ----------------------------------------

	def test_from_string_multiple_rules(self):
		tests = [
				# two rules
				{'input': 'body{margin:0;} p {padding:0 }',
				 'expected': ['body{margin:0;}', 'p {padding:0 }']
					},
				# two rules, media-queried
				{'input': '@media all {' \
						'	p { margin:0;}' \
						'	span { margin:0;}' \
						'}',
				 'expected': ['@media all {p { margin:0;}}', 
					 '@media all {span { margin:0;}}']
					}
				]

		for test in tests:
			yield self.check_from_string_multiple_rules, test
	
	def check_from_string_multiple_rules(self, test):
		rules = Rule.from_string(test['input'])
		observed = [r.to_string() for r in rules]
		for k in test:
			print '%s: %s' % (k, test[k])
		print 'observed: %s' % (observed)
		assert observed == test['expected']

	# ----------------------------------------



