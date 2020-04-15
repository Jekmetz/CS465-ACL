import os
import sys
from os import path
import code.constants as CONST
from code.classes import *
from code.commands import *
from code.helpers import *

session = Session();

def main():
	file_genocide();
	if(sys.argv[1] == "manual_control"):
		manual_control();
	else:
		run_commands_file(sys.argv[1]);
	executionEnd();

def run_commands_file(file):
	#run every line in file
	with open(file,"r") as f:
		for line in f:
			run_command(line.strip());

def run_command(cmd):
	global session;
	split = cmd.split(" ",1);
	if split[0] in cmdList:
		#use lambda ternary style to be the most efficient
		cmdList[split[0]](
			(lambda: "", lambda: split[1])[len(split) > 1](), 
			session
		);
	else:
		dualLog("Faulty command: {cmd}\n".format(cmd=split[0]));

def manual_control():
	#allow for manual control of the program
	cmd = "";
	while(cmd != "end"):
		cmd = input("> ");
		run_command(cmd);

if __name__ == "__main__":
	main();