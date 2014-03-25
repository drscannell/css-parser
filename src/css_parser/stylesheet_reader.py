from parser import Parser

class StyleSheetReader:

	@classmethod
	def read_string(cls, txt):
		return Parser.parse_string(txt)

	@classmethod
	def read_filepath(cls, filepath):
		f = open(filepath, 'r')
		txt = f.read()
		f.close()
		return read_string(txt)

