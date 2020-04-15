from .constants import *
from os import path
from .helpers import *
import sys
from .classes import *

#global variables

def useradd(params,s):
	(username,password) = params.split(" ");

	if(s.cu == None):
		if(username != "root"):
			dualLog(
				"No user was logged in but non-root user creation was attempted\n" +
				"\tAborting program.\n");
			executionEnd(s);
			sys.exit();

	if(s.cu != None and s.cu != "root"):
		dualLog("Only root may issue useradd command.\n");
		return;

	#if the account doesnt exist...
	if(not (username in s.users)):
		#add username and password to the accounts file
		with open(ACCOUNTSFILE,"a") as f:
			f.write("{} {}\n".format(username,password));

		#add them to the users
		s.users.append(username);
		dualLog("Account '{}' created!\n".format(username));
	#If the account already existed...
	else:
		dualLog("Account '{}' already existed!\n".format(username));

def login(params,s):
	(username,password) = params.split(" ");

	if(s.cu != None):
		dualLog("User '{}' already logged in. Failure to log in user: {}.\n".format(s.cu,username));
		return;

	if(loginAccount(username,password)):
		s.cu = username;
		dualLog("User '{}' logged in.\n".format(username));
	else:
		dualLog("Login authentication failed. Failure to log in user: {}\n".format(username));

def logout(params,s):
	dualLog("User '{}' logged out.\n".format(s.cu));
	s.cu = None;

def groupadd(params,s):
	if(s.cu != "root"):
		dualLog("Group '{}' cannot be created because current user is not root.\n".format(params));
		return;

	if(params == "nil"):
		dualLog("Group cannot have name 'nil'.\n");
		return;

	if not (params in s.groups):
		s.groups[params]=Group(params);
		dualLog("Group '{}' added.\n".format(params));
	else:
		dualLog("Group '{}' cannot be created because it already exists.\n".format(params));

def usergrp(params, s):
	(user,group) = params.split(" ");

	if(s.cu != "root"):
		dualLog("User '{}' cannot add '{}' to group '{}'.\n".format(s.cu,user,group));
		return;

	if(not (user in s.users)):
		dualLog("User '{}' not found!\n".format(user));
		return;

	if(not group in s.groups):
		dualLog("Group '{}' not found!\n".format(group));
		return;

	g = s.groups[group];

	#if they already exist in group...
	if(user in g.users):
		dualLog("User '{}' already in group '{}'.\n".format(user,group));
		return;

	g.users.append(user);
	dualLog("User '{}' added to group '{}'.\n".format(user,group));

def mkfile(params,s):
	filename = params.split(" ")[0];

	if(s.cu == None):
		dualLog("Somebody must be logged in to create a file!\n");
		return;

	if(filename in s.files.keys()):
		dualLog("File '{}' already exists!\n".format(filename));
		return;

	#create file
	with open(path.join(FILEDIR,filename),"w+") as f:
		pass;

	s.files[filename] = File(filename,s.cu);
	dualLog("File '{}' sucessfully created with owner '{}' and default permissions!\n".format(filename,s.cu));

def chmod(params,s):
	(filename,permstr) = params.split(" ",1);

	#if there is no file...
	if(not filename in s.files):
		dualLog("File '{}' does not exist.\n".format(filename));
		return;
	#if there is no one logged in...
	if(s.cu == None):
		dualLog("File '{}'s permissions can not be changed. No user is logged in.\n".format(filename));
		return;
	
	#if the current user isn't the owner or root...
	if(not (s.cu in (s.files[filename].owner,"root")) ):
		dualLog("User '{}' does not have permission to change permissions for file '{}'.\n".format(s.cu,filename));
		return;

	s.files[filename].perm = strToPerm(permstr);
	dualLog("File '{}' permissions successfully changed to '{}' by '{}'.\n".format(filename,permstr,s.cu));

def chown(params,s):
	(f,usr) = params.split(" ");

	#if it is not the root...
	if(s.cu != "root"):
		dualLog("Only root user can change owners");
		return;

	#if the user doesn't exist...
	if(not (usr in s.users)):
		dualLog("User '{}' not found!\n".format(usr));
		return;

	#if the file does not exist...
	if(not f in s.files):
		dualLog("File '{}' not found!\n".format(f));
		return;

	s.files[f].owner = usr;
	dualLog("File '{}' owner successfully changed to '{}'\n".format(f,usr));

def chgrp(params,s):
	(filename, group) = params.split(" ");

	if(s.cu == None):
		dualLog("A user must be logged in to perform chgrp.\n");
		return;

	if(not (filename in s.files)):
		dualLog("File '{}' not found!\n".format(filename));
		return;

	if(s.cu != s.files[filename].owner and s.cu != "root"):
		dualLog("Only the current owner, '{}' or 'root' can modify this file.\n".format(s.files[filename].owner));
		return;

	if(not group in s.groups):
		if(group == "nil"):
			s.files[filename].group = None;
			dualLog("group successfully changed!\n");
			return;
		else:
			dualLog("Group '{}' not found!\n".format(group));
		return;

	if not(s.cu in s.groups[group].users) and s.cu != "root":
		dualLog("User '{}' is not in group '{}'.\n".format(s.cu,group));
		return;

	s.files[filename].group = group;
	dualLog("File '{}' group successfully changed to '{}' by '{}'!\n".format(filename,group,s.cu));

def read(params, s):
	filename = params.strip();

	if(s.cu == None):
		dualLog("A user must be logged in to read a file.\n");
		return;

	if(not (filename in s.files)):
		dualLog("File '{}' not found!\n".format(filename));
		return;

	f = s.files[filename];

	canAccess = False;
	#find access permissions
	#owner
	if(s.cu == f.owner):
		#check read on owner
		canAccess = (f.perm & 1<<8);
	#group
	elif(f.group != None and s.cu in s.groups[f.group].users):
		#check read on group
		canAccess = (f.perm & 1<<5);
	#everyone
	else:
		#check read on everyone
		canAccess = (f.perm & 1<<2);

	if(canAccess):
		dualLog("User '{}' reads file '{}' with text:\n".format(s.cu,filename));
		with open(path.join(FILEDIR,filename),"r") as f:
			for line in f:
				dualLog(line);
	else:
		dualLog("User '{}' denied read access to file '{}'.\n".format(s.cu,filename));

def write(params, s):
	(filename,text) = params.split(" ",1);

	if(s.cu == None):
		dualLog("A user must be logged in to read a file.\n");
		return;

	if(not (filename in s.files)):
		dualLog("File '{}' not found!\n".format(filename));
		return;

	f = s.files[filename];

	canAccess = False;
	#find access permissions
	#owner
	if(s.cu == f.owner):
		#check read on owner
		canAccess = (f.perm & 1<<7);
	#group
	elif(f.group != None and s.cu in s.groups[f.group].users):
		#check read on group
		canAccess = (f.perm & 1<<4);
	#everyone
	else:
		#check read on everyone
		canAccess = (f.perm & 1<<1);

	if(canAccess):
		with open(path.join(FILEDIR,filename),"a") as f:
			f.write(text + "\n");
		dualLog("User '{}' wrote to '{}': '{}'\n".format(s.cu,filename,text));
	else:
		dualLog("User '{}' denied write access to file '{}'.\n".format(s.cu,filename));

def execute(params, s):
	filename = params.strip();

	if(s.cu == None):
		dualLog("A user must be logged in to read a file.\n");
		return;

	if(not (filename in s.files)):
		dualLog("File '{}' not found!\n".format(filename));
		return;

	f = s.files[filename];

	canAccess = False;
	#find access permissions
	#owner
	if(s.cu == f.owner):
		#check read on owner
		canAccess = (f.perm & 1<<6);
	#group
	elif(f.group != None and s.cu in s.groups[f.group].users):
		#check read on group
		canAccess = (f.perm & 1<<3);
	#everyone
	else:
		#check read on everyone
		canAccess = (f.perm & 1<<0);

	if(canAccess):
		dualLog("'{}' executed successfully by '{}'\n".format(filename,s.cu));
	else:
		dualLog("User '{}' denied execute access to file '{}'.\n".format(s.cu,filename));

def ls(params,s):
	filename = params.strip();

	if(s.cu == None):
		dualLog("A user must be logged in to use ls command.\n");
		return;

	if(not filename in s.files):
		dualLog("File '{}' does not exist.\n".format(filename));
		return;
	dualLog(s.files[filename].toString() + "\n");

def end(params,s):
	executionEnd(s);

cmdList = {
	"useradd" 	: useradd,
	"login" 	: login,
	"logout" 	: logout,
	"groupadd"	: groupadd,
	"usergrp"	: usergrp,
	"mkfile"	: mkfile,
	"chmod"		: chmod,
	"chown"		: chown,
	"chgrp"		: chgrp,
	"read"		: read,
	"write"		: write,
	"execute"	: execute,
	"ls"		: ls,
	"end" 		: end,
};