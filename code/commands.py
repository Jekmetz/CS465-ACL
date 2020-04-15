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
	#if the account doesnt exist...
	if(not (username in s.users)):
		#add username and password to the accounts file
		with open(ACCOUNTSFILE,"a") as f:
			f.write("{} {}\n".format(username,password));

		#add them to the users
		s.users.append(username);
	#If the account already existed...
	else:
		dualLog("Account '{}' already existed!".format(username));

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

	if(not (group in s.groups)):
		dualLog("Group '{}' not found!\n".format(user));
		return;

	s.groups[group].users.append(user);
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
	dualLog("File '{}' sucessfully created!\n".format(filename));

def mkdir(params,s):
	print(params);

def end(params,s):
	executionEnd(s);

cmdList = {
	"useradd" 	: useradd,
	"login" 	: login,
	"logout" 	: logout,
	"groupadd"	: groupadd,
	"usergrp"	: usergrp,
	"mkfile"	: mkfile,
	"mkdir" 	: mkdir,
	"end" 		: end,
};