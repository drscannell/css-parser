from css_parser.rule import Rule

class TestCases:

	# ----------------------------------------

	def test_pretty_print(self):
		tests = [
				# one rule
				{'input': 'body{margin:0;}',
				 'indent': '\t',
				 'expected': 'body {\n' \
						 '\tmargin:0;\n' \
						 '}'
					},
				# one rule, two declarations
				{'input': 'body {\n' \
						'	margin:0;\n' \
						'	padding:0;\n' \
						'}',
				 'indent': '\t',
				 'expected': 'body {\n' \
						 '\tmargin:0;\n' \
						 '\tpadding:0;\n' \
						 '}'
					},
				# one rule, two declarations and comment
				{'input': 'body {\n' \
						'	margin:0;\n' \
						' /* comment */\n' \
						'	padding:0;\n' \
						'}',
				 'indent': '\t',
				 'expected': 'body {\n' \
						 '\tmargin:0;\n' \
						 '\t/* comment */\n' \
						 '\tpadding:0;\n' \
						 '}'
					}


				]

		for test in tests:
			yield self.check_pretty_print, test
	
	def check_pretty_print(self, test):
		rule = Rule.from_string(test['input'])
		observed = rule.to_string(test['indent'])
		for k in test:
			print '%s: %s' % (k, test[k])
		print 'observed: %s' % (observed)
		assert observed == test['expected']

	# ----------------------------------------
