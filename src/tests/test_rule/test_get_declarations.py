from css_parser.rule import Rule

class TestCases:

	# ----------------------------------------

	def test_get_declarations(self):
		tests = [
				# one declaration, no query
				{'input': 'body{margin:0;}',
				 'query': None,
				 'expected': ['0']
					},
				# two declarations, no query
				{'input': 'body{' \
						'	margin:0;' \
						'	padding:0;' \
						'}',
				 'query': None,
				 'expected': ['0', '0']
					},
				# two declarations, no query, missing terminal semicolon
				{'input': 'body{' \
						'	margin:0;' \
						'	padding:0' \
						'}',
				 'query': None,
				 'expected': ['0', '0']
					},
				# two declarations, query for one
				{'input': 'body{' \
						'	margin:0;' \
						'	padding:0;' \
						'}',
				 'query': 'margin',
				 'expected': ['0']
					},
				# three declarations, query for two
				{'input': 'body{' \
						'	color  : rgba(0,0,0,0) ;' \
						'	padding:0;' \
						'	color:black' \
						'}',
				 'query': 'color',
				 'expected': ['rgba(0,0,0,0)', 'black']
					}

				]

		for test in tests:
			yield self.check_get_declarations, test
	
	def check_get_declarations(self, test):
		rule = Rule.from_string(test['input'])
		observed = [d.get_value() for d in rule.get_declarations(test['query'])]
		for k in test:
			print '%s: %s' % (k, test[k])
		print 'observed: %s' % (observed)
		assert observed == test['expected']

	# ----------------------------------------

