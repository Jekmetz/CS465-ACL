This runs in python 3.5.2.
To execute this file, type:

python3 access.py \<input\_file\>

where \<input\_file\> is the name of a test case file in the same directory this README is in. You can replace \<input\_file\> with manual\_control to enter manual control mode.

The program, as per the documentation, assumes that every command is typed in properly so it is not tested for faulty command usage. It does, however, test for commands that don't exist.

To verify the contents of J's test cases (inputs and outputs stored in jtc1 and jtc2), simply type in

python3 access.py jtc1/jtc1INPUT.txt

and the files and outputs directories will populate with the same files and outputs that were copied into jtc1.
replace jtc1 with jtc2 to test the second case.
