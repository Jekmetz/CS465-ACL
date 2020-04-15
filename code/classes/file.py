class File:

	def __init__(self, _name, _owner):
		self.perm = 0;
		self.name = _name;
		self.owner = _owner;
		self.group = None;

	def setPerm(self, _perm):
		perm = _perm;