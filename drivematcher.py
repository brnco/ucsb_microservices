#!/usr/bin/env python
import os

def match(path):
	if path.startswith("/") or path.startswith("\\"):
		path = path[1:]
	path.replace("\\","/")	
	if not os.name == 'posix': #if windows
		if "microservices-logs" in path:
			drive = "S:/"
		else:
			drive = "R:/"
		realpath = os.path.join(drive,path)
	else: #if mac/ unix
		if "microservices-logs" in path:
			drive = "/Volumes/special/DeptShare/special"
		else:
			drive = "/Volumes/special"
		realpath = os.path.join(drive,path)
	return realpath

def desktop():
	try:
		desktop = os.path.join(os.environ["HOME"], "Desktop")
	except:
		desktop = os.path.join(os.environ["USERPROFILE"], "Desktop")
	return desktop