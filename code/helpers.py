from .constants import *
from os import path
import os

def loginAccount(username,password):
	#check list of users and all passwords
	if(path.exists(ACCOUNTSFILE)):
		with open(ACCOUNTSFILE, "r") as f:
			#for every line in f...
			for line in f:
				split = line.strip().split(" ");
				u = split[0];
				p = split[1];
				#if the usernames match...
				if(u == username):
					#if the passwords match...
					if(p == password):
						return True;
					#if the username matched but it was a bad password...
					return False;
	#if no username matched
	return False;

def dualLog(str):
	print(str,end="");
	with open(LOGFILE,"a") as logfile:
		logfile.write(str);

def file_genocide():
	#Go through FILEDIR and OUTPUTDIR and kill it... kill it all
	filelist = os.listdir(FILEDIR);
	for f in filelist:
		os.remove(path.join(FILEDIR,f));
	filelist = os.listdir(OUTPUTDIR);
	for f in filelist:
		os.remove(path.join(OUTPUTDIR,f));

def executionEnd(session):
	#create FILESFILE
	with open(FILESFILE,"w") as f:
		for file in session.files.values():
			#TODO: change to the correct output
			f.write(file.toString() + "\n");

	#create GROUPSFILE
	with open(GROUPSFILE,"w") as f:
		for group in session.groups.values():
			f.write(group.name + ": " + " ".join(group.users) + "\n");

	#TODO: GENERATE WHATEVER OTHER FILES ARE NEEDED