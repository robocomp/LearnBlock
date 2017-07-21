#take the sys.argv[1] as file path and start parsing it to translate into specificworker.py code

import sys
import time
import getpass

filepath= sys.argv[1]
print(filepath)

code= open(filepath, 'r')
lines= code.readlines()
total_lines = len(lines)

# File flow control
line_number=0

# Line indentation control
inblock= 0
filename= filepath.split('/')[-1]
write_path= "/home/aniq55/robocomp/components/learnbot/learnbot-dsl/"+filename+".py"
target= open(write_path, 'w')

# Write the code generation details in the file
target.write('"""\n')
target.write("This is automatically generated python script\n")
target.write("Author: "+ getpass.getuser() +" (C) 2017, for RoboComp Learnbot\n")
target.write("Generated on: "+ time.asctime( time.gmtime(time.time()))+"\n")
target.write('"""\n\n')

target.write('import sys\n')
target.write('import cv2\n')
target.write('import LearnBotClient\n')
target.write('from functions import *\n')
target.write('import time\n')

target.write('global lbot\n')
target.write('lbot = LearnBotClient.Client(sys.argv)\n')

target.write('lbot.adv, lbot.rot= 0,0\n')

from functions import *


# Functions
def indentor():
	if inblock:
		for x in range(inblock):
			target.write('\t'.rstrip('\n'))

def ignore(line_number):
	line= lines[line_number]
	while lines[line_number].strip() != '```':
		line_number = line_number +1
	return line_number	


# TRANSLATOR CODE
while line_number < total_lines:
	line= lines[line_number]
	line = line.lstrip('\t')		# Removes indentation if any in the DSL code
	words= line.split(' ')
	n= len(words)
	
	# Comments
	if line[0] == '#':
		target.write(line.rstrip('\n'))
		target.write('\n')
	
	# Mathematical and input
	elif '=' in line and 'if' not in words and 'get' not in line:
		indentor()
		target.write(line.rstrip('\n'))		# Mathematical operation or input
		if 'input' in line:	# input command
			target.write('()')
		target.write('\n')

	elif '=' in line and 'get' in line:
		twords= line.split('=')
		x= twords[0]+'=functions.get("'+twords[1].strip()+'")(lbot)'
		indentor()
		target.write(x.rstrip('\n'))	
		target.write('\n')


	# Print statement
	elif words[0] == 'print':
		indentor()
		target.write('print('+line[5:].strip().rstrip('\n')+')')
		target.write('\n')

	# Conditional blocks
	elif words[0] == 'if':
		indentor()
		target.write(' '.join(words[:-1]).rstrip('\n'))
		target.write(':\n')
		inblock+= 1

	elif line.strip()=='else':
		inblock-=1
		indentor()
		target.write(line.rstrip('\n'))
		target.write(':\n')
		inblock+= 1

	elif words[0] == 'else' and words[1] == 'if':
		inblock-=1
		indentor()
		target.write('elif ' + ' '.join(words[2:-1]).rstrip('\n'))
		target.write(':\n')
		inblock+= 1		
		
	# Indentation marker
	elif line.strip() == 'end':
		inblock-=1

	
	elif words[0] == 'repeat' and 'times' in line:	#Loop Type 1
		indentor()
		x = 'for var_'+ str(int(1000000*time.time()))[-8:]  +' in range('+words[1]+'):'
		target.write(x)
		target.write('\n')
		inblock+=1

	elif words[0] == 'repeat' and words[2] == 'from':	#Loop Type 2
		indentor()
		x = 'for '+words[1]+' in range('+words[3]+','+words[5].rstrip('\n')+'):'
		target.write(x)
		target.write('\n')
		inblock+=1

	elif words[0] == 'repeat' and words[2].rstrip('\n') == 'seconds':	#Loop Type 3
		indentor()
		var_name= 'var_'+ str(int(1000000*time.time()))[-8:]
		y= var_name +'= time.time()\n'
		target.write(y)
		y= 'while int(time.time() - '+ var_name +') <'+ str(int(words[1]))+':\n'
		target.write(y)
		inblock+=1

	elif words[0] == 'while':						#Loop Type 4
		indentor()
		x= line.strip()+':'
		target.write(x)
		target.write('\n')
		inblock+=1

	elif line.strip() == 'exitloop':
		indentor()
		target.write('break\n')

	elif line.strip() == '```':
		line_number +=1
		line_number=ignore(line_number)

	elif functions.has_key(words[0].strip()):
		params= []
		t=1
		while t<n:
			params.append(words[t].strip().strip('\n'))
			t=t+1

		l= len(params)
		t=0
		p_string=''
		while t<l:
			p_string= p_string + ','+params[t]
			t=t+1

		x= 'functions.get("'+words[0].strip()+'")(lbot,['+ p_string[1:]+ '])'
		indentor()
		target.write(x)	
		target.write('\n')
	else:
		pass


	line_number += 1

target.write('\n')
target.close()
