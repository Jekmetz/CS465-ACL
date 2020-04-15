class File:

	def __init__(self, _name, _owner):
		self.perm = 0x180;
		self.name = _name;
		self.owner = _owner;
		self.group = None;

	def toString(self):
		out = self.name + ": " + self.owner + " " + ("nil",self.group)[self.group!=None] + " ";
		
		#each of these ternaries say:
		#("x", "-")[self.perm & POS == 0](); 
		#if there is a bit set at POS, set to "x", otherwise "-"
		#owner perm
		out += ("r","-")[self.perm & (1<<8) == 0];
		out += ("w","-")[self.perm & (1<<7) == 0];
		out += ("x","-")[self.perm & (1<<6) == 0];

		out += " "

		#group perm
		out += ("r","-")[self.perm & (1<<5) == 0];
		out += ("w","-")[self.perm & (1<<4) == 0];
		out += ("x","-")[self.perm & (1<<3) == 0];

		out += " "

		#everyone perm
		out += ("r","-")[self.perm & (1<<2) == 0];
		out += ("w","-")[self.perm & (1<<1) == 0];
		out += ("x","-")[self.perm & (1<<0) == 0];
		return out;
