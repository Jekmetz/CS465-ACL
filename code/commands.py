from .constants import *
from os import path
from .helpers import *
import sys

#global variables

def useradd(params,s):
	args = params.split(" ");
	username = args[0];
	password = args[1];
	if(s.cu == None):
		if(username != "root"):
			dualLog(
				"No user was logged in but non-root user creation was attempted\n" +
				"\tAborting program.\n");
			executionEnd();
			sys.exit();
	#if the account exists...
	if(not accountExists(username)):
		#add username and password to the accounts file
		with open(ACCOUNTSFILE,"a") as f:
			f.write("{} {}\n".format(username,password));

def login(params,s):
	args = params.split(" ");
	username = args[0];
	password = args[1];

	if(s.cu != None):
		dualLog("User '{}' already logged in. Failure to log in user: {}.\n".format(s.cu,username));
		return;

	if(loginAccount(username,password)):
		s.cu = username;
	else:
		dualLog("Login authentication failed. Failure to log in user: {}\n".format(username));

def logout(params,s):
	s.cu = None;

def mkdir(params,s):
	print(params);

def end(params,s):
	pass;

cmdList = {
	"useradd" 	: useradd,
	"login" 	: login,
	"logout" 	: logout,
	"mkdir" 	: mkdir,
	"end" 		: end,
};