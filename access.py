import os
import sys
from os import path
import code.constants as CONST
from code.classes import *
from code.commands import *

#global variables
cu="";		#current user
files={};	#file dictionary
groups={};	#group dictionary

def main():
	file_genocide();
	if(sys.argv[1] == "manual_control"):
		manual_control();
	else:
		run_commands_file(sys.argv[1]);

def run_commands_file(file):
	#run every line in file
	with open(file,"r") as f:
		for line in f:
			run_command(line.strip());

def run_command(cmd):
	split = cmd.split(" ",1);
	if split[0] in cmdList:
		#use lambda ternary style to be the most efficient
		cmdList[split[0]]( (lambda: "", lambda: split[1])[len(split) > 1]() );
	else:
		dualLog("Faulty command: {cmd}\n".format(cmd=split[0]));

def manual_control():
	#allow for manual control of the program
	cmd = "";
	while(cmd != "end"):
		cmd = input("> ");
		run_command(cmd);

def dualLog(str):
	print(str,end="");
	with open(CONST.LOGFILE,"a") as logfile:
		logfile.write(str);


def file_genocide():
	#Go through FILEDIR and OUTPUTDIR and kill it... kill it all
	filelist = os.listdir(CONST.FILEDIR);
	for f in filelist:
		os.remove(path.join(CONST.FILEDIR,f));
	filelist = os.listdir(CONST.OUTPUTDIR);
	for f in filelist:
		os.remove(path.join(CONST.OUTPUTDIR,f));

if __name__ == "__main__":
	main();