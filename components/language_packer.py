import json

class language_pack:
	contents = None
	def __init__(self, path):
		with open(path, "rb") as f:
			content = f.read().decode("utf-8")
		split_content = content.split('"""')
		content = ""
		for i in range(len(split_content)):
			if i%2: #if not even
				content += split_content[i].replace("\n", "\\n")
			else:
				content += split_content[i]
			if i!=len(split_content)-1:
				content += '"'
		self.content = json.loads(content)
	def __getitem__(self, item):
		return self.content[item]

