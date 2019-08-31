from json import JSONEncoder

# ====================================================================================
# XJOptions хранит опции для конвертера
# ====================================================================================


class XJOptions:
	def __init__(self):
		self.emptyValue = False
		self.asArray = False
		self.enabledLogs = False
		self.clearLogs = False
		self.removeXML = True
		self.parseXML = True
		self.parseZip = True


class XJOptionsEncoder(JSONEncoder):
	def default(self, o):
			return o.__dict__
