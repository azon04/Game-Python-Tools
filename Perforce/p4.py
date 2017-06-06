# p4.py - Ahmad Fauzan Umar @ 2017
# Perforce-python simple library
# Current features :
# - Checkout file
# - Revert file
# - Sync file
# TODO :
#

import os
import subprocess

p4port = 0
p4client = 0
p4user = 0
p4pass = 0

# Settings
enabledLog = False
showOutput = True

def Init(port, client, user, passwd):
	global p4port
	global p4client
	global p4user
	global p4pass

	p4port = port
	p4client = client
	p4user = user
	p4pass = passwd

def CallP4Function(funcName, options, filePath = ""):
	arr = ["p4"]

	if (p4port != 0) :
		arr.extend(["-p", p4port, "-P", p4pass, "-u", p4user, "-c", p4client]);

	arr.append(funcName)

	if options:
		arr.extend(options)

	if filePath != "" :
		arr.append(filePath)

	p = subprocess.Popen(arr)

	p.wait()

def CheckOutFile(pathfile, bAbsolutePath = True):
	if(bAbsolutePath):
		path = pathfile
	else :
		path = os.path.join(os.path.curdir(), pathfile)

	CallP4Function("edit", [], path)


def RevertFile(pathfile, bAbsolutePath=True, bOnlyUnchanged = False):
	if(bAbsolutePath):
		path = pathfile
	else :
		path = os.path.join(os.path.curdir(), pathfile)

	options = []
	if bOnlyUnchanged == True :
		options.append("-a")

	CallP4Function("revert", options, path)

def Sync(pathfile="", bAbsolutePath=True):
	if(bAbsolutePath):
		path = pathfile
	else:
		path = os.path.join(os.path.curdir(), pathfile)

	CallP4Function("sync", [], path)



