import parser

class StyleSheetReader:

	@classmethod
	def read_string(cls, txt):
		return parser.Parser.parse_string(txt)

	@classmethod
	def read_filepath(cls, filepath):
		f = open(filepath, 'r')
		txt = f.read()
		f.close()
		return cls.read_string(txt)

