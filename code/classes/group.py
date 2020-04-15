class Group:
	def __init__(self, _name):
		self.name = _name;
		self.users = [];

	def userInGroup(self,search):
		for user in self.users:
			if(search == user):
				return True;
		return False;