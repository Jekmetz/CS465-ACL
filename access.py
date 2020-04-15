import os
import sys
from os import path
import constants as CONST
from classes.file import File

def main():
	file_genocide();
	if(sys.argv[1] == "manual_control"):
		manual_control();
	else:
		run_commands_file(sys.argv[1]);
	end();

def run_commands_file(file):
	#run every line in file
	with open(file,"r") as f:
		for line in f:
			run_command(line.strip());

def run_command(cmd):
	pass;

def end():
	pass;

def manual_control():
	#allow for manual control of the program
	cmd = "";
	while(cmd != "end"):
		cmd = raw_input("> ");
		run_command(cmd);

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