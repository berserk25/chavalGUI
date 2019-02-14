import xml.etree.ElementTree as ET

class ResourceFinder:
	def __init__(self, resource_file):
		self.file_path = resource_file
		self.tree = ET.parse(self.file_path)
		self.root = self.tree.getroot()

	def findString(self, name_attrib):
		return self.root.find(".//string[@name='{}']".format(name_attrib)).text
