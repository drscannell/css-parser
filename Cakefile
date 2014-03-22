{exec} = require 'child_process'

# ------------ helper ------------

runscript = (cmd, callback) ->
	child = exec cmd
	child.stdout.on 'data', (data) -> console.log data.trim()
	child.stderr.on 'data', (data) -> console.log data.trim()
	child.on 'exit', (status) ->
		callback?()

# ------------ subtasks ------------

runTests = (callback) ->
	cmd = 'nosetests'
	runscript cmd, callback

clearPyc = (callback) ->
	cmd = 'find ./src/ -name "*.pyc" -delete'
	runscript cmd, callback

# ------------ command line tasks ------------

task 'test', 'run unit tests via nose', (options) ->
	console.log '\n'
	runTests ->
		clearPyc ->
			'removed python compilation files\n'
	

